Segmentation of Chinese text using [pkuseg-python](https://github.com/lancopku/pkuseg-python).
Pkuseg does not build with Python 3.9, so use 3.8 (tested with 3.8.6).

# CLI
Script for segmenting files or (interactively) segmenting input from stdin.
Used as segmentation engine for my CLI vocabulary manager/analyzer [han-cihui](https://github.com/jannes/han-cihui).

## Dependencies
- pkuseg
- regex
- pyinstaller

## Building
Use the `make.sh` build script, python binary must be compiled with `--enable-framework` for pyinstaller to work.  
On Mac with pyenv: `env PYTHON_CONFIGURE_OPTS="--enable-framework CC=clang" pyenv install 3.8.6` to install Python 3.8.6 with `--enable-framework`

# HTTP
Small microservice for segmenting text.
Used as segmentation engine for my vocabulary analyzer web app [jihanzi](https://www.jihanzi.com).

## Dependencies
- pkuseg
- regex
- flask
- gunicorn

