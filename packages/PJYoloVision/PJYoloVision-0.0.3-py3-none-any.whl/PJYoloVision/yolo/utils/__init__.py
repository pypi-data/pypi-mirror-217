import contextlib
import inspect
import logging.config
import os
import platform
import re
import subprocess
import sys
import tempfile
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace
from typing import Union

import cv2
import numpy as np
import torch
import yaml

from PJYoloVision import __version__

# PyTorch Multi-GPU DDP Constants
RANK = int(os.getenv('RANK', -1))
LOCAL_RANK = int(os.getenv('LOCAL_RANK', -1))  # https://pytorch.org/docs/stable/elastic/run.html
WORLD_SIZE = int(os.getenv('WORLD_SIZE', 1))

# Other Constants
FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # YOLO
DEFAULT_CFG_PATH = ROOT / 'yolo/cfg/default.yaml'
NUM_THREADS = min(8, max(1, os.cpu_count() - 1))  # number of YOLOv5 multiprocessing threads
AUTOINSTALL = str(os.getenv('YOLO_AUTOINSTALL', True)).lower() == 'true'  # global auto-install mode
VERBOSE = str(os.getenv('YOLO_VERBOSE', True)).lower() == 'true'  # global detail mode
TQDM_BAR_FORMAT = '{l_bar}{bar:10}{r_bar}'  # tqdm bar format
LOGGING_NAME = 'PJYoloVision'
MACOS, LINUX, WINDOWS = (platform.system() == x for x in ['Darwin', 'Linux', 'Windows'])  # environment booleans
HELP_MSG = \
    """
    NONE
    """

# Settings
torch.set_printoptions(linewidth=320, precision=4, profile='default')
np.set_printoptions(linewidth=320, formatter={'float_kind': '{:11.5g}'.format})  # format short g, %precision=5
cv2.setNumThreads(0)  # prevent OpenCV from multithreading (incompatible with PyTorch DataLoader)
os.environ['NUMEXPR_MAX_THREADS'] = str(NUM_THREADS)  # NumExpr max threads
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'  # for deterministic training


class SimpleClass:
    """
    PJYoloVision SimpleClass is a base class providing helpful string representation, error reporting, and attribute
    access methods for easier debugging and usage.
    """

    def __str__(self, *args, **kwargs):
        """Return a human-readable string representation of the object."""
        attr = []
        for a in dir(self, *args, **kwargs):
            v = getattr(self, a)
            if not callable(v) and not a.startswith('__', *args, **kwargs):
                if isinstance(v, SimpleClass):
                    # Display only the module and class name for subclasses
                    s = f'{a}: {v.__module__}.{v.__class__.__name__} object'
                else:
                    s = f'{a}: {repr(v)}'
                attr.append(s)
        return f'{self.__module__}.{self.__class__.__name__} object with attributes:\n\n' + '\n'.join(attr)

    def __repr__(self, *args, **kwargs):
        """Return a machine-readable string representation of the object."""
        return self.__str__()

    def __getattr__(self, attr, *args, **kwargs):
        """Custom attribute access error message with helpful information."""
        name = self.__class__.__name__
        raise AttributeError(f"'{name}' object has no attribute '{attr}'. See valid attributes below.\n{self.__doc__}")


class IterableSimpleNamespace(SimpleNamespace):

    def __iter__(self, *args, **kwargs):
        return iter(vars(self).items())

    def __str__(self, *args, **kwargs):
        return '\n'.join(f'{k}={v}' for k, v in vars(self).items())

    def __getattr__(self, attr, *args, **kwargs):
        name = self.__class__.__name__
        raise AttributeError(f"""
            '{name}' object has no attribute '{attr}'. This may be caused by a modified or out of date PJYoloVision
            'default.yaml' file.\nPlease update your code with 'pip install -U PJYoloVision' and if necessary replace
            {DEFAULT_CFG_PATH} with the latest version from
            
            """)

    def get(self, key, default=None, *args, **kwargs):
        """Return the value of the specified key if it exists; otherwise, return the default value."""
        return getattr(self, key, default)


def set_logging(name=LOGGING_NAME, detail=True, *args, **kwargs):
    # sets up logging for the given name
    rank = int(os.getenv('RANK', -1))  # rank in world for Multi-GPU trainings
    level = logging.INFO if detail and rank in (-1, 0) else logging.ERROR
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            name: {
                'format': '%(message)s'}},
        'handlers': {
            name: {
                'class': 'logging.StreamHandler',
                'formatter': name,
                'level': level}},
        'loggers': {
            name: {
                'level': level,
                'handlers': [name],
                'propagate': False}}})


# Set logger
set_logging(LOGGING_NAME, detail=VERBOSE)  # run before defining LOGGER
LOGGER = logging.getLogger(LOGGING_NAME)  # define globally (used in env_train.py, val.py, detection.py, etc.)
if WINDOWS:  # emoji-safe logging
    info_fn, warning_fn = LOGGER.info, LOGGER.warning
    setattr(LOGGER, info_fn.__name__, lambda x: info_fn(emojis(x)))
    setattr(LOGGER, warning_fn.__name__, lambda x: warning_fn(emojis(x)))


def yaml_save(file='data.yaml', data=None, *args, **kwargs):

    file = Path(file)
    if not file.parent.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'w') as f:
        # Dump data to file in YAML format, converting Path objects to strings
        yaml.safe_dump({k: str(v) if isinstance(v, Path) else v
                        for k, v in data.items()},
                       f,
                       sort_keys=False,
                       allow_unicode=True)


def yaml_load(file='data.yaml', append_filename=False, *args, **kwargs):
    """
    Load YAML data from a file.

    Args:
        file (str, optional, *args, **kwargs): File name. Default is 'data.yaml'.
        append_filename (bool): Add the YAML filename to the YAML dictionary. Default is False.

    Returns:
        dict: YAML data and file name.
    """
    with open(file, errors='ignore', encoding='utf-8') as f:
        s = f.read()  # string

        if not s.isprintable():
            s = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+', '', s)

        return {**yaml.safe_load(s), 'yaml_file': str(file)} if append_filename else yaml.safe_load(s)


def yaml_print(yaml_file: Union[str, Path, dict]) -> None:
    yaml_dict = yaml_load(yaml_file) if isinstance(yaml_file, (str, Path)) else yaml_file
    dump = yaml.dump(yaml_dict, sort_keys=False, allow_unicode=True)
    LOGGER.info(f"Printing '{colorstr('bold', 'black', yaml_file)}'\n\n{dump}")


# Default configuration
DEFAULT_CFG_DICT = yaml_load(DEFAULT_CFG_PATH)
for k, v in DEFAULT_CFG_DICT.items():
    if isinstance(v, str) and v.lower() == 'none':
        DEFAULT_CFG_DICT[k] = None
DEFAULT_CFG_KEYS = DEFAULT_CFG_DICT.keys()
DEFAULT_CFG = IterableSimpleNamespace(**DEFAULT_CFG_DICT)


def is_colab():
    return 'COLAB_RELEASE_TAG' in os.environ or 'COLAB_BACKEND_VERSION' in os.environ


def is_kaggle():
    """
    Check if the current script is running inside a Kaggle kernel.

    Returns:
        bool: True if running inside a Kaggle kernel, False otherwise.
    """
    return os.environ.get('PWD') == '/kaggle/working' and os.environ.get('KAGGLE_URL_BASE') == 'https://www.kaggle.com'


def is_jupyter():
    with contextlib.suppress(Exception):
        from IPython import get_ipython
        return get_ipython() is not None
    return False


def is_docker() -> bool:
    file = Path('/proc/self/cgroup')
    if file.exists():
        with open(file) as f:
            return 'docker' in f.read()
    else:
        return False


def is_online() -> bool:
    import socket
    with contextlib.suppress(Exception):
        host = socket.gethostbyname('www.github.com')
        socket.create_connection((host, 80), timeout=2)
        return True
    return False


ONLINE = is_online()


def is_pip_package(filepath: str = __name__) -> bool:
    import importlib.util

    spec = importlib.util.find_spec(filepath)

    return spec is not None and spec.origin is not None


def is_dir_writeable(dir_path: Union[str, Path]) -> bool:
    try:
        with tempfile.TemporaryFile(dir=dir_path):
            pass
        return True
    except OSError:
        return False


def is_pytest_running():
    return ('PYTEST_CURRENT_TEST' in os.environ) or ('pytest' in sys.modules) or ('pytest' in Path(sys.argv[0]).stem)


def is_github_actions_ci() -> bool:
    """
    Determine if the current environment is a GitHub Actions CI Python runner.

    Returns:
        (bool): True if the current environment is a GitHub Actions CI Python runner, False otherwise.
    """
    return 'GITHUB_ACTIONS' in os.environ and 'RUNNER_OS' in os.environ and 'RUNNER_TOOL_CACHE' in os.environ


def is_git_dir():
    """
    Determines whether the current file is part of a git repository.
    If the current file is not part of a git repository, returns None.

    Returns:
        (bool): True if current file is part of a git repository.
    """
    return get_git_dir() is not None


def get_git_dir():
    """
    Determines whether the current file is part of a git repository and if so, returns the repository root directory.
    If the current file is not part of a git repository, returns None.

    Returns:
        (Path) or (None, *args, **kwargs): Git root directory if found or None if not found.
    """
    for d in Path(__file__).parents:
        if (d / '.git').is_dir():
            return d
    return None  # no .git dir found


def get_git_origin_url():
    """
    Retrieves the origin URL of a git repository.

    Returns:
        (str) or (None, *args, **kwargs): The origin URL of the git repository.
    """
    if is_git_dir():
        with contextlib.suppress(subprocess.CalledProcessError):
            origin = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'])
            return origin.decode().strip()
    return None  # if not git dir or on error


def get_git_branch():
    """
    Returns the current git branch name. If not in a git repository, returns None.

    Returns:
        (str) or (None, *args, **kwargs): The current git branch name.
    """
    if is_git_dir():
        with contextlib.suppress(subprocess.CalledProcessError):
            origin = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
            return origin.decode().strip()
    return None  # if not git dir or on error


def get_default_args(func, *args, **kwargs):
    """Returns a dictionary of default arguments for a function.

    Args:
        func (callable, *args, **kwargs): The function to inspect.

    Returns:
        dict: A dictionary where each key is a parameter name, and each value is the default value of that parameter.
    """
    signature = inspect.signature(func)
    return {k: v.default for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty}


def get_user_config_dir(sub_dir='PJYoloVision', *args, **kwargs):
    """
    Get the user config directory.

    Args:
        sub_dir (str): The name of the subdirectory to create.

    Returns:
        Path: The path to the user config directory.
    """
    # Return the appropriate config directory for each operating system
    if WINDOWS:
        path = Path.home() / 'AppData' / 'Roaming' / sub_dir
    elif MACOS:  # macOS
        path = Path.home() / 'Library' / 'Application Support' / sub_dir
    elif LINUX:
        path = Path.home() / '.config' / sub_dir
    else:
        raise ValueError(f'Unsupported operating system: {platform.system()}')

    # GCP and AWS lambda fix, only /tmp is writeable
    if not is_dir_writeable(str(path.parent)):
        path = Path('/tmp') / sub_dir

    # Create the subdirectory if it does not exist
    path.mkdir(parents=True, exist_ok=True)

    return path


USER_CONFIG_DIR = os.getenv('YOLO_CONFIG_DIR', get_user_config_dir())  # PJYoloVision settings dir


def emojis(string='', *args, **kwargs):
    # Return platform-dependent emoji-safe version of string
    return string.encode().decode('ascii', 'ignore') if WINDOWS else string


def colorstr(*input, **kwargs):
    # Colors a string https://en.wikipedia.org/wiki/ANSI_escape_code, i.e.  colorstr('blue', 'hello world')
    *args, string = input if len(input) > 1 else ('blue', 'bold', input[0])  # color arguments, string
    colors = {
        'black': '\033[30m',  # basic colors
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',  # bright colors
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'end': '\033[0m',  # misc
        'bold': '\033[1m',
        'underline': '\033[4m'}
    return ''.join(colors[x] for x in args) + f'{string}' + colors['end']


class TryExcept(contextlib.ContextDecorator):
    # PJYoloVision TryExcept class. Usage: @TryExcept() decorator or 'with TryExcept():' context manager
    def __init__(self, msg='', detail=True, *args, **kwargs):
        self.msg = msg
        self.detail = detail

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, exc_type, value, traceback, *args, **kwargs):
        if self.detail and value:
            print(emojis(f"{self.msg}{': ' if self.msg else ''}{value}"))
        return True


def threaded(func, *args, **kwargs):
    # Multi-threads a target function and returns thread. Usage: @threaded decorator
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


def set_sentry():
    """
    Initialize the Sentry SDK for error tracking and reporting if pytest is not currently running.
    """

    def before_send(event, hint, *args, **kwargs):
        if 'exc_info' in hint:
            exc_type, exc_value, tb = hint['exc_info']
            if exc_type in (KeyboardInterrupt, FileNotFoundError) \
                    or 'out of memory' in str(exc_value, *args, **kwargs):
                return None  # do not send event

        event['tags'] = {
            'sys_argv': sys.argv[0],
            'sys_argv_name': Path(sys.argv[0]).name,
            'install': 'git' if is_git_dir() else 'pip' if is_pip_package() else 'other',
            'os': ENVIRONMENT}
        return event

    if SETTINGS['sync'] and \
            RANK in (-1, 0) and \
            Path(sys.argv[0]).name == 'yolo' and \
            not TESTS_RUNNING and \
            ONLINE and \
            (is_pip_package() and not is_git_dir()):

        import sentry_sdk  # noqa
        sentry_sdk.init(
            dsn='https://f805855f03bb4363bc1e16cb7d87b654@o4504521589325824.ingest.sentry.io/4504521592406016',
            debug=False,
            traces_sample_rate=1.0,
            release=__version__,
            environment='production',  # 'dev' or 'production'
            before_send=before_send,
            ignore_errors=[KeyboardInterrupt, FileNotFoundError])
        sentry_sdk.set_user({'id': SETTINGS['uuid']})

        # Disable all sentry logging
        for logger in 'sentry_sdk', 'sentry_sdk.errors':
            logging.getLogger(logger).setLevel(logging.CRITICAL)


def get_settings(file=USER_CONFIG_DIR / 'settings.yaml', version='0.0.2', *args, **kwargs):
    import hashlib

    from PJYoloVision.yolo.utils.checks import check_version
    from PJYoloVision.yolo.utils.torch_utils import torch_distributed_zero_first

    git_dir = get_git_dir()
    root = git_dir or Path()
    datasets_root = (root.parent if git_dir and is_dir_writeable(root.parent) else root).resolve()

    defaults = {
        'datasets_dir': str(datasets_root / 'PJYoloVision'),
        'weights_dir': str(root / 'downloads'),
        'runs_dir': str(root / 'runs'),
        'sync': True,
        'uuid': hashlib.sha256(str(uuid.getnode()).encode()).hexdigest(),
        'settings_version': version}

    with torch_distributed_zero_first(RANK):
        if not file.exists():

            yaml_save(file, defaults)

        settings = yaml_load(file)

        # Check that settings keys and types match defaults
        correct = \
            settings.keys() == defaults.keys() \
            and all(type(a) == type(b) for a, b in zip(settings.values(), defaults.values())) \
            and check_version(settings['settings_version'], version)

        if not correct:
            LOGGER.warning('Opps Wait  PJYoloVision settings reset to defaults. This is normal and may be due to a '
                           'recent PJYoloVision package update, but may have overwritten previous settings. '
                           f"\nView and update settings with 'yolo settings' or at '{file}'")
            settings = defaults
            yaml_save(file, settings)

        return settings


def set_settings(kwargs, file=USER_CONFIG_DIR / 'settings.yaml', *args):
    SETTINGS.update(kwargs)
    yaml_save(file, SETTINGS)


PREFIX = colorstr('PJYoloVision: ')
SETTINGS = get_settings()

DATASETS_DIR = Path(SETTINGS['datasets_dir'])

ENVIRONMENT = 'Colab' if is_colab() else 'Kaggle' if is_kaggle() else 'Jupyter' if is_jupyter() else \
    'Docker' if is_docker() else platform.system()
TESTS_RUNNING = is_pytest_running() or is_github_actions_ci()
set_sentry()
