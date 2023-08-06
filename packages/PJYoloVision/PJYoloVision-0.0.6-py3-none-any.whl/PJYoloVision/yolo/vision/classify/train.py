 

import torch
import torchvision

from PJYoloVision.nn.tasks import ClassificationModel, attempt_load_one_weight
from PJYoloVision.yolo import vision


from PJYoloVision.yolo.core.trainer import BaseTrainer
from PJYoloVision.yolo.data import build_classification_dataloader
from PJYoloVision.yolo.utils import DEFAULT_CFG, LOGGER, RANK, colorstr
from PJYoloVision.yolo.utils.torch_utils import is_parallel, strip_optimizer


class ClassificationTrainer(BaseTrainer):

    def __init__(self, cfg=DEFAULT_CFG, overrides=None, *args, **kwargs):
        if overrides is None:
            overrides = {}
        overrides['task'] = 'classify'
        super().__init__(cfg, overrides)

    def set_model_attributes(self, *args, **kwargs):
        self.model.names = self.data['names']

    def get_model(self, cfg=None, weights=None, detail=True, *args, **kwargs):
        model = ClassificationModel(cfg, nc=self.data['nc'], detail=detail and RANK == -1)
        if weights:
            model.load(weights)

        pretrained = False
        for m in model.modules():
            if not pretrained and hasattr(m, 'reset_parameters'):
                m.reset_parameters()
            if isinstance(m, torch.nn.Dropout) and self.args.dropout:
                m.p = self.args.dropout  # set dropout
        for p in model.parameters():
            p.requires_grad = True  # for training

        # Update defaults
        if self.args.imgsz == 640:
            self.args.imgsz = 224

        return model

    def setup_model(self, *args, **kwargs):

        if isinstance(self.model, torch.nn.Module ):  # if model is loaded beforehand. No setup needed
            return

        model = str(self.model)

        if model.endswith('.pt', *args, **kwargs):
            self.model, _ = attempt_load_one_weight(model, device='cpu')
            for p in self.model.parameters():
                p.requires_grad = True  # for training
        elif model.endswith('.yaml', *args, **kwargs):
            self.model = self.get_model(cfg=model)
        elif model in torchvision.models.__dict__:
            pretrained = True
            self.model = torchvision.models.__dict__[model](weights='IMAGENET1K_V1' if pretrained else None)
        else:
            FileNotFoundError(f'ERROR: model={model} not found locally or online. Please check model name.')
        ClassificationModel.reshape_outputs(self.model, self.data['nc'])

        return  # dont return ckpt. Classification doesn't support resume

    def get_dataloader(self, dataset_path, batch_size=16, rank=0, mode='train', *args, **kwargs):
        loader = build_classification_dataloader(path=dataset_path,
                                                 imgsz=self.args.imgsz,
                                                 batch_size=batch_size if mode == 'train' else (batch_size * 2),
                                                 augment=mode == 'train',
                                                 rank=rank,
                                                 workers=self.args.workers)
        # Attach inference transforms
        if mode != 'train':
            if is_parallel(self.model, *args, **kwargs):
                self.model.module.transforms = loader.dataset.torch_transforms
            else:
                self.model.transforms = loader.dataset.torch_transforms
        return loader

    def preprocess_batch(self, batch, *args, **kwargs):
        batch['img'] = batch['img'].to(self.device)
        batch['cls'] = batch['cls'].to(self.device)
        return batch

    def progress_string(self, *args, **kwargs):
        return ('\n' + '%11s' * (4 + len(self.loss_names))) % \
            ('Epoch', 'GPU_mem', *self.loss_names, 'Instances', 'Size')

    def get_validator(self, *args, **kwargs):
        self.loss_names = ['loss']
        return vision.classify.ClassificationValidator(self.test_loader, self.save_dir)

    def criterion(self, preds, batch, *args, **kwargs):
        loss = torch.nn.functional.cross_entropy(preds, batch['cls'], reduction='sum') / self.args.nbs
        loss_items = loss.detach()
        return loss, loss_items

    # def label_loss_items(self, loss_items=None, prefix="train", *args, **kwargs):
    #     """
    #     Returns a loss dict with labelled training loss items tensor
    #     """
    #     # Not needed for classification but necessary for segmentation & detection
    #     keys = [f"{prefix}/{x}" for x in self.loss_names]
    #     if loss_items is not None:
    #         loss_items = [round(float(x), 5) for x in loss_items]  # convert tensors to 5 decimal place floats
    #         return dict(zip(keys, loss_items))
    #     else:
    #         return keys

    def label_loss_items(self, loss_items=None, prefix='train', *args, **kwargs):
        """
        Returns a loss dict with labelled training loss items tensor
        """
        # Not needed for classification but necessary for segmentation & detection
        keys = [f'{prefix}/{x}' for x in self.loss_names]
        if loss_items is None:
            return keys
        loss_items = [round(float(loss_items), 5)]
        return dict(zip(keys, loss_items))

    def resume_training(self, ckpt, *args, **kwargs):
        pass

    def final_eval(self, *args, **kwargs):
        for f in self.last, self.best:
            if f.exists():
                strip_optimizer(f)  # strip optimizers

        LOGGER.info(f"Results saved to {colorstr('bold', self.save_dir)}")


