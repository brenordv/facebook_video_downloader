# -*- coding: utf-8 -*-
"""
FACEBOOK VIDEO DOWNLOADER

Arguments:
    video_url: URL for the PUBLIC facebook video.
    filename: Optional. Path + filename of the downloaded video file. (Default: current timestamp in the current folder)
    resolution: Optional. Which resolutio will be used. (Default: HD)
    log_level: Debug, Info, Error or Exception. (Default: No Log)

Repository:


Author:
    Breno RdV

Usage:
    facebook.py help | url <video_url> | output <filename> | resolution <SD_or_HD> | log [<log_level>]
"""
import logging
import re
import requests
from os import getcwd
from docopt import docopt
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

__version__ = "1.0.0"


VALID_RESOLUTIONS = ["SD", "HD"]
BLOCK_SIZE = 1024
DEFAULT_DOUCHEBAG_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
}


def __get_adjusted_filename__(custom_filename: str = None) -> Path:
    if custom_filename is None:
        filename = Path(getcwd()).joinpath(f"{datetime.now().strftime('%Y%m%d_%H%M%S__%f')}.mp4")
    else:
        filename = Path(custom_filename)

    return filename


def __get_adjusted_resolution__(resolution: str):
    adjusted_resolution = resolution.upper().strip()
    if adjusted_resolution not in VALID_RESOLUTIONS:
        raise ValueError(f"Resolution '{resolution}' is not valid. Expected: {', '.join(VALID_RESOLUTIONS)}")

    return adjusted_resolution


class DownloadManager(object):
    def __init__(self, url: str, resolution: str):
        self.__resolution__ = resolution
        self.__url__ = url
        self.__source_url__ = None

        self.__sort_resolutions__()

    def __get_content__(self):
        response = requests.get(self.__url__, headers=DEFAULT_DOUCHEBAG_HEADERS)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to download content of link: {self.__url__} | "
                                  f"Status code: {response.status_code} | "
                                  f"Reason: {response.reason}")

        return response.text

    @staticmethod
    def __check_for_resolution__(content, resolution):
        lower_resolution = resolution.lower()
        res = re.search(r'{res}_src:"(.*?)"'.format(res=lower_resolution), content)
        if res is not None:
            res_url = res.group(1)
        else:
            res_url = None

        return res_url

    def __sort_resolutions__(self):
        content = self.__get_content__()

        res = self.__check_for_resolution__(content, self.__resolution__)

        if res is not None:
            self.__source_url__ = res
            return

        fallback_resolution = [r for r in VALID_RESOLUTIONS if r != self.__resolution__][0]
        logging.warning(f"No sources found for resolution {self.__resolution__}! Falling back to: {fallback_resolution}")
        res = self.__check_for_resolution__(content, fallback_resolution)

        if res is None:
            raise TypeError(f"No resolutions found in url: {self.__url__}")

        self.__source_url__ = res

    def download(self, filename: Path):
        logging.debug(f"Getting video from URL: {self.__source_url__}")
        response = requests.get(self.__source_url__, headers=DEFAULT_DOUCHEBAG_HEADERS, stream=True)

        if response.status_code != 200:
            raise ConnectionError(f"Failed to download video from url: {self.__source_url__} | "
                                  f"Status code: {response.status_code} | "
                                  f"Reason: {response.reason}")

        file_size = int(response.headers['Content-Length'])
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=filename.name, ascii=True) as progress_bar:
            with open(filename, 'wb') as output_file:
                for data in response.iter_content(BLOCK_SIZE):
                    progress_bar.update(len(data))
                    output_file.write(data)


def process_download(url: str = None, custom_filename: str = None, resolution: str = "HD"):
    filename = __get_adjusted_filename__(custom_filename=custom_filename)
    selected_resolution = __get_adjusted_resolution__(resolution=resolution)
    downloader = DownloadManager(url=url, resolution=selected_resolution)
    downloader.download(filename=filename)
    print(f"Video downloaded and saved as: {filename}")


def main():
    args = docopt(__doc__)
    if args.get("help", False) or args.get("url") is None:
        print(__doc__)
        return

    if args.get("log", False):
        logging.basicConfig(level=args.get("<log_level>"))

    process_download(
        url=args.get("<video_url>"),
        custom_filename=args.get("<filename>"),
        resolution=args.get("resolution", "HD")
    )


if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")
