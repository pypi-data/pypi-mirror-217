import contextlib
import re
import shutil
import sys
from difflib import get_close_matches
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, List, Union

from PJYoloVision.yolo.utils import (DEFAULT_CFG, DEFAULT_CFG_DICT, DEFAULT_CFG_PATH, LOGGER, ROOT, USER_CONFIG_DIR,
                                     IterableSimpleNamespace, __version__, checks, colorstr, yaml_load, yaml_print)

CLI_HELP_MSG = \
    f"""
    NONE 

    """

# Define keys for arg type checks
CFG_FLOAT_KEYS = 'warmup_epochs', 'box', 'cls', 'dfl', 'degrees', 'shear', 'fl_gamma'
CFG_FRACTION_KEYS = ('dropout', 'iou', 'lr0', 'lrf', 'momentum', 'weight_decay', 'warmup_momentum', 'warmup_bias_lr',
                     'label_smoothing', 'hsv_h', 'hsv_s', 'hsv_v', 'translate', 'scale', 'perspective', 'flipud',
                     'fliplr', 'mosaic', 'mixup', 'copy_paste', 'conf', 'iou')  # fractional floats limited to 0.0 - 1.0
CFG_INT_KEYS = ('epochs', 'patience', 'batch', 'workers', 'seed', 'close_mosaic', 'mask_ratio', 'max_det', 'vid_stride',
                'line_thickness', 'workspace', 'nbs', 'save_period')
CFG_BOOL_KEYS = ('save', 'exist_ok', 'detail', 'deterministic', 'single_cls', 'image_weights', 'rect', 'cos_lr',
                 'overlap_mask', 'val', 'save_json', 'save_hybrid', 'half', 'dnn', 'plots', 'show', 'save_txt',
                 'save_conf', 'save_crop', 'hide_labels', 'hide_conf', 'visualize', 'augment', 'agnostic_nms',
                 'retina_masks', 'boxes', 'keras', 'optimize', 'int8', 'dynamic', 'simplify', 'nms', 'v5loader')

# Define valid tasks and modes
MODES = 'train', 'val', 'predict', 'export', 'track', 'benchmark'
TASKS = 'detection', 'segmentation', 'classify'
TASK2DATA = {'detection': 'coco128.yaml', 'segmentation': 'coco128-seg.yaml', 'classify': 'imagenet100'}
TASK2MODEL = {'detection': 'YOLOvisionn.pt', 'segmentation': 'YOLOvisionn-seg.pt', 'classify': 'YOLOvisionn-cls.pt'}


def cfg2dict(cfg, *args, **kwargs):
    """
    Convert a configuration object to a dictionary, whether it is a file path, a string, or a SimpleNamespace object.

    Inputs:
        cfg (str) or (Path) or (SimpleNamespace, *args, **kwargs): Configuration object to be converted to a dictionary.

    Returns:
        cfg (dict): Configuration object in dictionary format.
    """
    if isinstance(cfg, (str, Path)):
        cfg = yaml_load(cfg)  # load dict
    elif isinstance(cfg, SimpleNamespace):
        cfg = vars(cfg)  # convert to dict
    return cfg


def get_cfg(cfg: Union[str, Path, Dict, SimpleNamespace] = DEFAULT_CFG_DICT, overrides: Dict = None, *args, **kwargs):
    cfg = cfg2dict(cfg)

    # Merge overrides
    if overrides:
        overrides = cfg2dict(overrides)
        check_cfg_mismatch(cfg, overrides)
        cfg = {**cfg, **overrides}  # merge cfg and overrides dicts (prefer overrides)

    # Special handling for numeric project/names
    for k in 'project', 'name':
        if k in cfg and isinstance(cfg[k], (int, float)):
            cfg[k] = str(cfg[k])

    # Type and Value checks
    for k, v in cfg.items():
        if v is not None:  # None values may be from optional args
            if k in CFG_FLOAT_KEYS and not isinstance(v, (int, float)):
                raise TypeError(f"'{k}={v}' is of invalid type {type(v).__name__}. "
                                f"Valid '{k}' types are int (i.e. '{k}=0') or float (i.e. '{k}=0.5')")
            elif k in CFG_FRACTION_KEYS:
                if not isinstance(v, (int, float)):
                    raise TypeError(f"'{k}={v}' is of invalid type {type(v).__name__}. "
                                    f"Valid '{k}' types are int (i.e. '{k}=0') or float (i.e. '{k}=0.5')")
                if not (0.0 <= v <= 1.0,):
                    raise ValueError(f"'{k}={v}' is an invalid value. "
                                     f"Valid '{k}' values are between 0.0 and 1.0.")
            elif k in CFG_INT_KEYS and not isinstance(v, int):
                raise TypeError(f"'{k}={v}' is of invalid type {type(v).__name__}. "
                                f"'{k}' must be an int (i.e. '{k}=8')")
            elif k in CFG_BOOL_KEYS and not isinstance(v, bool):
                raise TypeError(f"'{k}={v}' is of invalid type {type(v).__name__}. "
                                f"'{k}' must be a bool (i.e. '{k}=True' or '{k}=False')")

    # Return instance
    return IterableSimpleNamespace(**cfg)


def check_cfg_mismatch(base: Dict, custom: Dict, e=None, *args, **kwargs):
    base, custom = (set(x.keys()) for x in (base, custom))
    mismatched = [x for x in custom if x not in base]
    if mismatched:
        string = ''
        for x in mismatched:
            matches = get_close_matches(x, base)  # key list
            matches = [f'{k}={DEFAULT_CFG_DICT[k]}' if DEFAULT_CFG_DICT.get(k) is not None else k for k in matches]
            match_str = f'Similar arguments are i.e. {matches}.' if matches else ''
            string += f"'{colorstr('red', 'bold', x)}' is not a valid YOLO argument. {match_str}\n"
        raise SyntaxError(string + CLI_HELP_MSG) from e


def merge_equals_args(args: List[str]) -> List[str]:
    new_args = []
    for i, arg in enumerate(args):
        if arg == '=' and 0 < i < len(args) - 1:  # merge ['arg', '=', 'val']
            new_args[-1] += f'={args[i + 1]}'
            del args[i + 1]
        elif arg.endswith('=') and i < len(args) - 1 and '=' not in args[i + 1]:  # merge ['arg=', 'val']
            new_args.append(f'{arg}{args[i + 1]}')
            del args[i + 1]
        elif arg.startswith('=') and i > 0:  # merge ['arg', '=val']
            new_args[-1] += arg
        else:
            new_args.append(arg)
    return new_args


def entrypoint(debug='', *args, **kwargs):
    args = (debug.split(' ') if debug else sys.argv)[1:]
    if not args:  # no arguments passed
        LOGGER.info(CLI_HELP_MSG)
        return

    special = {
        'help': lambda: LOGGER.info(CLI_HELP_MSG),
        'checks': checks.check_yolo,
        'version': lambda: LOGGER.info(__version__),
        'settings': lambda: yaml_print(USER_CONFIG_DIR / 'settings.yaml'),
        'cfg': lambda: yaml_print(DEFAULT_CFG_PATH),
        'copy-cfg': copy_default_cfg}
    full_args_dict = {**DEFAULT_CFG_DICT, **{k: None for k in TASKS}, **{k: None for k in MODES}, **special}

    # Define common mis-uses of special commands, i.e. -h, -help, --help
    special.update({k[0]: v for k, v in special.items()})  # singular
    special.update({k[:-1]: v for k, v in special.items() if len(k) > 1 and k.endswith('s')})  # singular
    special = {**special, **{f'-{k}': v for k, v in special.items()}, **{f'--{k}': v for k, v in special.items()}}

    overrides = {}  # basic overrides, i.e. imgsz=320
    for a in merge_equals_args(args):  # merge spaces around '=' sign
        if a.startswith('--', *args, **kwargs):
            LOGGER.warning(f" Opps Wait  '{a}' does not require leading dashes '--', updating to '{a[2:]}'.")
            a = a[2:]
        if a.endswith(',', *args, **kwargs):
            LOGGER.warning(f" Opps Wait  '{a}' does not require trailing comma ',', updating to '{a[:-1]}'.")
            a = a[:-1]
        if '=' in a:
            try:
                re.sub(r' *= *', '=', a)  # remove spaces around equals sign
                k, v = a.split('=', 1)  # split on first '=' sign
                assert v, f"missing '{k}' value"
                if k == 'cfg':  # custom.yaml passed
                    LOGGER.info(f'Overriding {DEFAULT_CFG_PATH} with {v}')
                    overrides = {k: val for k, val in yaml_load(checks.check_yaml(v)).items() if k != 'cfg'}
                else:
                    if v.lower() == 'none':
                        v = None
                    elif v.lower() == 'true':
                        v = True
                    elif v.lower() == 'false':
                        v = False
                    else:
                        with contextlib.suppress(Exception):
                            v = eval(v)
                    overrides[k] = v
            except (NameError, SyntaxError, ValueError, AssertionError) as e:
                check_cfg_mismatch(full_args_dict, {a: ''}, e)

        elif a in TASKS:
            overrides['task'] = a
        elif a in MODES:
            overrides['mode'] = a
        elif a in special:
            special[a]()
            return
        elif a in DEFAULT_CFG_DICT and isinstance(DEFAULT_CFG_DICT[a], bool):
            overrides[a] = True  # auto-True for default bool args, i.e. 'yolo show' sets show=True
        elif a in DEFAULT_CFG_DICT:
            raise SyntaxError(f"'{colorstr('red', 'bold', a)}' is a valid YOLO argument but is missing an '=' sign "
                              f"to set its value, i.e. try '{a}={DEFAULT_CFG_DICT[a]}'\n{CLI_HELP_MSG}")
        else:
            check_cfg_mismatch(full_args_dict, {a: ''})

    # Check keys
    check_cfg_mismatch(full_args_dict, overrides)

    # Mode
    mode = overrides.get('mode', None)
    if mode is None:
        mode = DEFAULT_CFG.mode or 'predict'
        LOGGER.warning(f" Opps Wait  'mode' is missing. Valid modes are {MODES}. Using default 'mode={mode}'.")
    elif mode not in MODES:
        if mode not in ('checks', checks):
            raise ValueError(f"Invalid 'mode={mode}'. Valid modes are {MODES}.\n{CLI_HELP_MSG}")
        LOGGER.warning(f" Opps Wait  'yolo mode=checks' is deprecated. Use 'yolo checks' instead.")
        checks.check_yolo()
        return

    # Task
    task = overrides.pop('task', None)
    if task:
        if task not in TASKS:
            raise ValueError(f"Invalid 'task={task}'. Valid tasks are {TASKS}.\n{CLI_HELP_MSG}")
        if 'model' not in overrides:
            overrides['model'] = TASK2MODEL[task]

    # Model
    model = overrides.pop('model', DEFAULT_CFG.model)
    if model is None:
        model = 'YOLOvisionn.pt'
        LOGGER.warning(f" Opps Wait  'model' is missing. Using default 'model={model}'.")
    from PJYoloVision.yolo.core.model import YOLO
    overrides['model'] = model
    model = YOLO(model, task=task)
    if isinstance(overrides.get('pretrained'), str):
        model.load(overrides['pretrained'])

    # Task Update
    if task != model.task:
        if task:
            LOGGER.warning(f" Opps Wait  conflicting 'task={task}' passed with 'task={model.task}' model. "
                           f"Ignoring 'task={task}' and updating to 'task={model.task}' to match model.")
        task = model.task

    # Mode
    if mode in ('predict', 'track') and 'source' not in overrides:
        overrides['source'] = DEFAULT_CFG.source or ROOT / 'assets' if (ROOT / 'assets').exists() \
            else LOGGER.warning(f" Opps Wait  'source' is missing. Using default 'source={overrides['source']}'.")
    elif mode in ('train', 'val'):
        if 'data' not in overrides:
            raise ValueError('Data is not found to set data.yaml to model just do \n'
                             'model.overrides["data"] = "data.yaml"')
    elif mode == 'export':
        if 'format' not in overrides:
            overrides['format'] = DEFAULT_CFG.format or 'torchscript'
            LOGGER.warning(f" Opps Wait  'format' is missing. Using default 'format={overrides['format']}'.")

    # Run command in python
    # getattr(model, mode)(**vars(get_cfg(overrides=overrides)))  # default args using default.yaml

    getattr(model, mode)(**overrides)  # default args from model


# Special modes --------------------------------------------------------------------------------------------------------
def copy_default_cfg():
    new_file = Path.cwd() / DEFAULT_CFG_PATH.name.replace('.yaml', '_copy.yaml')
    shutil.copy2(DEFAULT_CFG_PATH, new_file)
