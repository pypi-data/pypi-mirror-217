import contextlib
import subprocess
from itertools import repeat
from multiprocessing.pool import ThreadPool
from pathlib import Path
from urllib import parse, request
from zipfile import BadZipFile, ZipFile, is_zipfile

import requests
import torch
from tqdm import tqdm

from PJYoloVision.yolo.utils import LOGGER, checks, is_online

GITHUB_ASSET_NAMES = [f'PJYoloVision{size}{suffix}.pt' for size in 'nsmlx' for suffix in ('', '6', '-cls', '-seg')] + \
                     [f'yolov5{size}u.pt' for size in 'nsmlx'] + \
                     [f'yolov3{size}u.pt' for size in ('', '-spp', '-tiny')]
GITHUB_ASSET_STEMS = [Path(k).stem for k in GITHUB_ASSET_NAMES]


def is_url(url, check=True, *args, **kwargs):
    # Check if string is URL and check if URL exists
    with contextlib.suppress(Exception):
        url = str(url)
        result = parse.urlparse(url)
        assert all([result.scheme, result.netloc])  # check if is url
        if check:
            with request.urlopen(url) as response:
                return response.getcode() == 200  # check if exists online
        return True
    return False


def unzip_file(file, path=None, exclude=('.DS_Store', '__MACOSX')):
    """
    Unzip a *.zip file to path/, excluding files containing strings in exclude list
    Replaces: ZipFile(file).extractall(path=path)
    """
    if not (Path(file).exists() and is_zipfile(file)):
        raise BadZipFile(f"File '{file}' does not exist or is a bad zip file.")
    if path is None:
        path = Path(file).parent  # default path
    with ZipFile(file) as zipObj:
        for f in zipObj.namelist():  # list all archived filenames in the zip
            if all(x not in f for x in exclude):
                zipObj.extract(f, path=path)
        return zipObj.namelist()[0]  # return unzip dir


def safe_download(url,
                  file=None,
                  dir=None,
                  unzip=True,
                  delete=False,
                  curl=False,
                  retry=3,
                  min_bytes=1E0,
                  progress=True, *args, **kwargs):
    if '://' not in str(url) and Path(url).is_file():
        f = Path(url)
    else:
        assert dir or file, 'dir or file required for download'
        f = dir / Path(url).name if dir else Path(file)
        desc = f'Downloading {url} to {f}'
        LOGGER.info(f'{desc}...')
        f.parent.mkdir(parents=True, exist_ok=True)  # make directory if missing
        for i in range(retry + 1):
            try:
                if curl or i > 0:  # curl download with retry, continue
                    s = 'sS' * (not progress)  # silent
                    r = subprocess.run(['curl', '-#', f'-{s}L', url, '-o', f, '--retry', '3', '-C', '-']).returncode
                    assert r == 0, f'Curl return value {r}'
                else:  # urllib download
                    method = 'torch'
                    if method == 'torch':
                        torch.hub.download_url_to_file(url, f, progress=progress)
                    else:
                        from PJYoloVision.yolo.utils import TQDM_BAR_FORMAT
                        with request.urlopen(url) as response, tqdm(total=int(response.getheader('Content-Length', 0)),
                                                                    desc=desc,
                                                                    disable=not progress,
                                                                    unit='B',
                                                                    unit_scale=True,
                                                                    unit_divisor=1024,
                                                                    bar_format=TQDM_BAR_FORMAT) as pbar:
                            with open(f, 'wb') as f_opened:
                                for data in response:
                                    f_opened.write(data)
                                    pbar.update(len(data))

                if f.exists():
                    if f.stat().st_size > min_bytes:
                        break  # success
                    f.unlink()  # remove partial downloads
            except Exception as e:
                if i == 0 and not is_online():
                    raise ConnectionError(f'Download failure for {url}. make sure your online') from e
                elif i >= retry:
                    raise ConnectionError(f'Download failure for {url}. Retry limit reached.') from e
                LOGGER.warning(f'⚠️ Download failure, retrying {i + 1}/{retry} {url}...')

    if unzip and f.exists() and f.suffix in ('.zip', '.tar', '.gz'):
        unzip_dir = dir or f.parent  # unzip to dir if provided else unzip in place
        LOGGER.info(f'Unzipping {f} to {unzip_dir}...')
        if f.suffix == '.zip':
            unzip_dir = unzip_file(file=f, path=unzip_dir)  # unzip
        elif f.suffix == '.tar':
            subprocess.run(['tar', 'xf', f, '--directory', unzip_dir], check=True)  # unzip
        elif f.suffix == '.gz':
            subprocess.run(['tar', 'xfz', f, '--directory', unzip_dir], check=True)  # unzip
        if delete:
            f.unlink()  # remove zip
        return unzip_dir


def download_from_git(file, repo='erfanzar/PJYoloVision', release='v0.0.1', *args, **kwargs):
    from PJYoloVision.yolo.utils import SETTINGS

    file = str(file)

    file = Path(file.strip().replace("'", ''))
    if file.exists():
        return str(file)
    elif (SETTINGS['weights_dir'] / file).exists():
        return str(SETTINGS['weights_dir'] / file)
    else:
        LOGGER.info(f'file : {file}')
        safe_download(url=f'https://github.com/{repo}/releases/download/{release}/{file}', file=file, min_bytes=1E5)

        return str(file)


def download(url, dir=Path.cwd(), unzip=True, delete=False, curl=False, threads=1, retry=3, *args, **kwargs):
    dir = Path(dir)
    dir.mkdir(parents=True, exist_ok=True)  # make directory
    if threads > 1:
        with ThreadPool(threads) as pool:
            pool.map(
                lambda x: safe_download(
                    url=x[0], dir=x[1], unzip=unzip, delete=delete, curl=curl, retry=retry, progress=threads <= 1),
                zip(url, repeat(dir)))
            pool.close()
            pool.join()
    else:
        for u in [url] if isinstance(url, (str, Path)) else url:
            safe_download(url=u, dir=dir, unzip=unzip, delete=delete, curl=curl, retry=retry)
