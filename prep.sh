#!/bin/sh -x

mkdir -p temp/train/images
mkdir -p temp/train/labels
# mkdir -p temp/val/images
# mkdir -p temp/val/labels

cp -r train_data/Images/* temp/train/images/
cp -r train_data/BBoxes/* temp/train/labels/
# cp -r train_data/train.txt temp/train/index.txt

# cp -r val_data/Images/* temp/val/images/
# cp -r val_data/BBoxes/* temp/val/labels/
# cp -r val_data/train.txt temp/val/index.txt

ls temp/train/images/**/*.jpg > temp/train/index.txt
# ls temp/val/images/**/*.jpg > temp/val/index.txt
