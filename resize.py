# -*- coding: utf-8 -*-


from __future__ import print_function
import os
import sys
import re
import gc
import uuid
from PIL import Image

def get_jpeg_file_yield(dirpath):
    """
    指定したディクレクトリからJPEGファイルを列挙してパスを取得する(yield)
    """
    file_pattern = re.compile(r'.+\.(jpg|JPG|jpeg|JPEG)$')
    for filename in os.listdir(dirpath):
        if file_pattern.match(filename) == None: #jpgのみ対象
            continue
        filepath = os.path.join(dirpath, filename)
        yield filepath

def get_image_dir_yield(base_path, img_dirnames=None):
    if img_dirnames == None:
        return base_path
    dir_img_base=os.path.join(base_path, 'Images')
    for dir_name in img_dirnames:
        image_dir = os.path.join(dir_img_base, dir_name)
        if not os.path.isdir(image_dir):
            continue
        yield image_dir

def resize_images(base_path, img_dirnames, size):
    """
    指定したディレクトリ以下のJPGファイルを指定した解像度以下になるようにリサイズする
    """
    for image_dir in get_image_dir_yield(base_path, img_dirnames):
        for path in get_jpeg_file_yield(image_dir): #jpgのみ対象:
            img = Image.open(path)
            origin_size = img.size
            if origin_size <= size: #リサイズ不要
                continue
            img = img.resize(size, Image.LANCZOS)
            img.save(path)
def rename_jpegs(base_path, img_dirnames):
    for image_dir in get_image_dir_yield(base_path, img_dirnames):
        for path in get_jpeg_file_yield(image_dir): #jpgのみ対象:
            name, ext = os.path.splitext(path)
            if ext in [".jpeg", ".JPEG", ".JPG"]:
                os.rename(path, name + ".jpg")
                print(path)

base_dir = './trein_data'
# img_dirnames = ['008']
# img_dirnames = [ '001','007']
# img_dirnames = [ '000' ]
img_dirnames = ['008', '007']
size = (800, 800)
resize_images(base_dir, img_dirnames, size)
rename_jpegs(base_dir, img_dirnames)
