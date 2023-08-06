 

import collections
from copy import deepcopy

from .augment import LetterBox


class MixAndRectDataset:
    """A wrapper of multiple images mixed dataset.

    Args:
        dataset (:obj:`BaseDataset`, *args, **kwargs): The dataset to be mixed.
        transforms (Sequence[dict], *args, **kwargs): config dict to be composed.
    """

    def __init__(self, dataset, *args, **kwargs):
        self.dataset = dataset
        self.imgsz = dataset.imgsz

    def __len__(self, *args, **kwargs):
        return len(self.dataset)

    def __getitem__(self, index, *args, **kwargs):
        labels = deepcopy(self.dataset[index])
        for transform in self.dataset.transforms.tolist():
            # mosaic and mixup
            if hasattr(transform, 'get_indexes', *args, **kwargs):
                indexes = transform.get_indexes(self.dataset)
                if not isinstance(indexes, collections.abc.Sequence, *args, **kwargs):
                    indexes = [indexes]
                mix_labels = [deepcopy(self.dataset[index]) for index in indexes]
                labels['mix_labels'] = mix_labels
            if self.dataset.rect and isinstance(transform, LetterBox, *args, **kwargs):
                transform.new_shape = self.dataset.batch_shapes[self.dataset.batch[index]]
            labels = transform(labels)
            if 'mix_labels' in labels:
                labels.pop('mix_labels')
        return labels
