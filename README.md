# YHD2018 AI

## preparation

### install dependencies

```sh
$ pipenv install
```

### increase image file

```sh
$ pipenv run python increase_img.py
# OR
$ pipenv run python increase_img.py --start_class 7
# OR
$ pipenv run python increase_img.py --start_class 7 --end_class 12
```

### add annotation

```sh
$ python /path/to/bboxtool.py ./train_data ./cfg/labels.txt
```

### edit model config

- classes はクラス数。  
- filtersの計算式は `filters=(クラス数+5)*3` で計算する。

```sh
$ cp cfg/yolov3-tiny.template.cfg cfg/yolov3-tiny.train.cfg; \
    sed -i.bak 's/^classes=80/classes=9/g' cfg/yolov3-tiny.train.cfg; \
    sed -i.bak 's/^filters=255/filters=42/g' cfg/yolov3-tiny.train.cfg
$ cp cfg/yolov3-tiny.template.cfg cfg/yolov3-tiny.predict.cfg; \
    sed -i.bak 's/^batch=64/batch=1/g' cfg/yolov3-tiny.predict.cfg; \
    sed -i.bak 's/^subdivisions=2/subdivisions=1/g' cfg/yolov3-tiny.predict.cfg; \
    sed -i.bak 's/^classes=80/classes=9/g' cfg/yolov3-tiny.predict.cfg; \
    sed -i.bak 's/^filters=255/filters=42/g' cfg/yolov3-tiny.predict.cfg
```

## prep for fine tune

Download default weights file for yolov3-tiny:  
```sh
https://pjreddie.com/media/files/yolov3-tiny.weights
```
  
Get pre-trained weights yolov3-tiny.conv.15 using command: 
```sh
./darknet partial cfg/yolov3-tiny.cfg yolov3-tiny.weights yolov3-tiny.conv.15 15
mv yolov3-tiny.conv.15 ../
```

ref.  
https://github.com/AlexeyAB/darknet#how-to-train-tiny-yolo-to-detect-your-custom-objects

## exec training

```sh
docker run \
    --name yhd2018ai \
    --runtime=nvidia \
    -v $PWD:/opt/kby \
    -it fkmy/nvidia-docker-darknet:latest
```

In container
```sh
$ cd /opt/kby
$ ./prep.sh
$ export PATH=/opt/darknet:$PATH
$ darknet detector train \
    cfg/dataset.txt \
    cfg/yolov3.train.cfg \
    yolov3-tiny.conv.15
```

## prediction

`darknet/cfg/kby.data` を作成  
```
classes=28
train = temp/train/index.txt 
valid = temp/val/index.txt 
labels = /Users/fkmy/git/yhd2018-ai/darknet/data/names.list
backup = backup/
```

`darknet detector test` を実行

```sh
$ cd darknet
$ ./darknet detector test cfg/kby.data ../cfg/yolov3.predict.cfg ../yolov3_50000.weights /Users/fkmy/git/yhd2018-ai/darknet/samples/theai20182nd/OR_IMG_8805.jpg
```

## refs
- https://wakuphas.hatenablog.com/entry/2018/09/19/025941
- http://demura.net/misc/14458.html