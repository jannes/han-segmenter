#!/bin/bash
site_packages_dir=$(pip show pkuseg | grep Location | cut -d" " -f 2)
pyinstaller \
    --add-data "${site_packages_dir}/pkuseg/dicts:pkuseg/dicts" \
    --add-data "${site_packages_dir}/pkuseg/models:pkuseg/models" \
    --add-data "dictionary.txt:." \
    --add-data "dictionary-fanjian.txt:." \
    --onedir main.py \
    --name han-segmenter
