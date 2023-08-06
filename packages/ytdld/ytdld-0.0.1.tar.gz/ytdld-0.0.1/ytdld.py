
# ToolName   : MaxPhisher
# Author     : ytdlp
# License    : MIT
# Copyright  : KasRoudra 2023
# Github     : https://github.com/KasRoudra
# Contact    : https://m.me/KasRoudra
# Description: Another python youtube downloader
# Tags       : youtube, downloader, yt-dl
# 1st Commit : 08/9/2022
# Language   : Python
# Portable file/script
# If you copy open source code, consider giving credit


"""
MIT License

Copyright (c) 2022-2023 KasRoudra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, iNCluding without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be iNCluded in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from argparse import ArgumentParser
from importlib import (
    import_module as eximport
)
from subprocess import (
    CompletedProcess,
    run
)
from os import (
    getenv,
    mkdir
)
from os.path import (
    dirname,
    isdir,
    isfile
)
from json import (
    dumps,
    loads
)

def shell(command: str, capture_output=False) -> CompletedProcess:
    """ 
    Run shell commands in python
    """
    return run(command, shell=True, capture_output=capture_output, check=True)

def inst_module(pip_module: str):
    """ 
    Try to install pip modules
    """
    try:
        eximport(pip_module)
        return True
    except ImportError:
        try:
            shell(f"pip3 install {pip_module} --break-system-packages")
        except ImportError:
            return False
    try:
        eximport(pip_module)
        return True
    except ImportError:
        return False

modules = ["kasutils", "pytube", "questionary"]

for module in modules:
    if not inst_module(module):
        print(f"{module} can't be installed.  Install in manually!")
        exit()

from kasutils import (
    BLACK,
    BLUE,
    CYAN,
    ENCODING,
    GREEN,
    PURPLE,
    RED,
    YELLOW,
    ask,
    error,
    info,
    info2,
    success,
    cat,
    center_text,
    clear,
    copy,
    delete,
    grep,
    is_online,
    lolcat,
    move,
    readable,
    rename,
    sed,
    sprint,
)
from pytube import (
    YouTube
)
from pytube.cli import (
    on_progress
)
from questionary import (
    select,
    text
)

VERSION = "0.0.1"

logo = f"""
{RED}__   _______     ____  _     ____  
{BLUE}\ \ / /_   _|   |  _ \| |   |  _ \ 
{GREEN} \ V /  | |_____| | | | |   | | | |
{CYAN}  | |   | |_____| |_| | |___| |_| |
{YELLOW}  |_|   |_|     |____/|_____|____/ 
{CYAN}{" "*28}[{BLUE}v{PURPLE}{VERSION[2:]}{CYAN}]
{BLUE}{" "*20}[{CYAN}By {GREEN}KasRoudra{BLUE}]
"""

home = getenv("HOME")
config_file = f"{home}/.config/ytdld/config.json"

argparser = ArgumentParser()

argparser.add_argument(
    "-t",
    "--type",
    help="Type of the media"
)
argparser.add_argument(
    "-f",
    "--format",
    help="File Format or Extension of the media"
)
argparser.add_argument(
    "-q",
    "--quality",
    help="Resolution or Bitrate the media"
)
argparser.add_argument(
    "-b",
    "--best",
    help="Automatically download the media of best resolution or bitrate",
    action="store_true"
)

args = argparser.parse_args()

arg_type = args.type
arg_format = args.format
arg_quality = args.quality
best = args.best

def parse_config() -> dict:
    """
    Read config or create one if doesn't exists
    """
    if isfile(config_file):
        with open(config_file, encoding=ENCODING) as conf:
            config = loads(conf.read())
    else:
        config = {
            "audio": {
                "allow": True,
                "formats": [
                    "mp4",
                    "webm"
                ],
                "qualities": [
                    "48kbps",
                    "50kbps",
                    "70kbps",
                    "128kbps",
                    "160kbps"
                ]
            },
            "video": {
                "allow": True,
                "formats": [
                    "mp4",
                    "webm"
                ],
                "qualities": [
                    "144p",
                    "360p",
                    "480p",
                    "720p",
                    "1080p",
                    "1440p",
                    "2180p"
                ]
            },
            "mixed": {
                "allow": True,
            },
            "directory": f"{home}/Download"
        }
        if not isdir(dirname(config_file)):
            mkdir(dirname(config_file))
        with open(config_file, "w", encoding=ENCODING) as conf:
            conf.write(dumps(config, indent=4))
    return config

def get_choice(streams) -> list:
    """
    Returns a list of choices based on streams.
    The index of choices refers to same item in streams list by index
    """
    choices = []
    for stream in streams:
        extension = stream.mime_type.split("/")[1]
        quality = stream.resolution or stream.abr
        if stream.is_progressive:
            filetype = "Mixed"
        else:
            filetype = stream.type.title()
        if stream.filesize < 1024:
            filesize = f"{round(stream.filesize, 2)} B"
        if stream.filesize > 1024:
            filesize = f"{round(stream.filesize_kb, 2)} KB"
        if stream.filesize > 1024 ** 2:
            filesize = f"{round(stream.filesize_mb, 2)} MB"
        if stream.filesize > 1024 ** 3:
            filesize = f"{round(stream.filesize_gb, 2)} GB"
        choices.append(f"{filetype}: {stream.title}-{quality}.{extension} {filesize}")
    return choices

def filter_streams(streams):
    """
    Filter streams by given configs or argument
    """
    filtered_streams = []
    config = parse_config()
    mixed = config["mixed"]["allow"] if arg_type is None else arg_type == "mixed"
    audio = config["audio"]
    video = config["video"]
    formats = audio["formats"] + video["formats"] if arg_format is None else [arg_format]
    qualities = audio["qualities"] + video["qualities"] if arg_quality is None else [arg_quality]
    for stream in streams:
        extension = stream.mime_type.split("/")[1]
        quality = stream.resolution or stream.abr
        allowed = config[stream.type]["allow"] if arg_type is None else arg_type == stream.type
        progressive = mixed and stream.is_progressive
        formative = extension in formats
        qualitive = quality in qualities
        if progressive or allowed:
            if formative and qualitive:
                filtered_streams.append(stream)
    if best:
        best_quality = 0
        best_extension = "webm" if arg_format is None else arg_format
        best_streams = []
        for best_stream in filtered_streams:
            pattern = "([0-9]*)"
            cur_qua = best_stream.resolution or best_stream.abr
            cur_quality = int(grep(pattern, cur_qua))
            cur_extenstion = best_stream.mime_type.split("/")[1]
            print(cur_extenstion == best_extension)
            print(cur_quality > best_quality)
            if cur_extenstion == best_extension and cur_quality > best_quality:
                best_quality = cur_quality
                best_streams = [best_stream]
        print(best_streams)
        filtered_streams = best_streams
    return filtered_streams

def download_stream(stream):
    """
    Download video from stream
    """
    config = parse_config()
    directory = config["directory"]
    if not isdir(directory):
        mkdir(directory)
    quality = stream.resolution or stream.abr
    extension = stream.mime_type.split("/")[1]
    filename = f"{stream.title}-{quality}.{extension}"
    print(f"{info}Staring download of {filename}")
    stream.download(output_path=directory)
    if isfile(f"{directory}/{filename}"):
        sprint("{info2} Downloaded successfully!")


def download(url):
    """
    Validate url and show download options
    """
    if url is None:
        return
    elif "https://youtube.com/" in url:
        ytid = url.split("=")[1].split("&")[0]
        if not len(ytid)==11:
            print(f"{error}NotYouTubeURLError: This is not a valid youtube url!")
            return
    # https://youtu.be/rdC1_jZtWKE
    elif "https://youtu.be/" in url:
        ytid = url.split("/")[-1]
        if not len(ytid)==11:
            print(f"{error}NotYouTubeURLError: This is not a valid youtube url!")
            return
    else:
        pass
    youtube = YouTube(url, on_progress_callback=on_progress)
    streams = youtube.streams
    filtered_streams = filter_streams(streams)
    choices = get_choice(filtered_streams)
    if len(filtered_streams) == 0:
        print(f"{error}NotFoundError: No media matched for config/argument")
        exit()
    elif len(filtered_streams) == 1:
        download_stream(filtered_streams[0])
    elif len(filtered_streams) > 1:
        chosen = select(
            "Choose your option:",
            choices=choices
        ).ask()
        if chosen is not None:
            index = choices.index(chosen)
            download_stream(filtered_streams[index])
    else:
        print(f"{error}FilterError: There were some error in filtering")
        exit()

def main():
    """
    Entrypoint of script
    """
    try:
        clear(logo=logo)
        url = text("Enter youtube url:").ask()
        # url = "https://youtube.com/watch?v=dCxSsr5xuL8&feature=share9"
        download(url)
    except KeyboardInterrupt:
        print(f"\n{info2}KeyboardInterrupt: Shutting down due to user interrption")
        exit(0)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()
