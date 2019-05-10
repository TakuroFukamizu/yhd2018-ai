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

#### Yolo v3 tiny

```sh
$ set -x; \
  export CLASS_NUM=9; \
  export CFG_TRAIN=cfg/yolov3-tiny.train.cfg; \
  export CFG_PREDI=cfg/yolov3-tiny.predict.cfg; \
  export FILTERS=`expr \( $CLASS_NUM + 5 \) \* 3`; \
  cp cfg/yolov3-tiny.template.cfg ${CFG_TRAIN}; \
    sed -i.bak 's/^batch=64/batch=32/g' ${CFG_TRAIN}; \
    sed -i.bak 's/^classes=80/classes='${CLASS_NUM}'/g' ${CFG_TRAIN}; \
    sed -i.bak 's/^filters=255/filters='${FILTERS}'/g' ${CFG_TRAIN}; \
  cp cfg/yolov3-tiny.template.cfg cfg/${CFG_PREDI}; \
    sed -i.bak 's/^batch=64/batch=1/g' cfg/${CFG_PREDI}; \
    sed -i.bak 's/^subdivisions=16/subdivisions=1/g' ${CFG_PREDI}; \
    sed -i.bak 's/^classes=80/classes='${CLASS_NUM}'/g' ${CFG_PREDI}; \
    sed -i.bak 's/^filters=255/filters='${FILTERS}'/g' ${CFG_PREDI}; \
  rm ${CFG_TRAIN}.bak; \
  rm ${CFG_PREDI}.bak
```

#### Yolo v2 tiny

```sh
$ set -x; \
  export CLASS_NUM=9; \
  export CFG_TRAIN=cfg/yolov3-tiny.train.cfg; \
  export CFG_PREDI=cfg/yolov3-tiny.predict.cfg; \
  export FILTERS=`expr \( $CLASS_NUM + 5 \) \* 3`; \
  cp cfg/yolov3-tiny.template.cfg ${CFG_TRAIN}; \
    sed -i.bak 's/^## {BATCH_PARAM} ##/batch=32/g' ${CFG_TRAIN}; \
    sed -i.bak 's/^## {SUBDIVISION_PARAM} ##/subdivisions=16/g' ${CFG_PREDI}; \
    sed -i.bak 's/^## {CLASSES_PARAM} ##/classes='${CLASS_NUM}'/g' ${CFG_TRAIN}; \
    sed -i.bak 's/^## {FILTERS_PARAM} ##/filters='${FILTERS}'/g' ${CFG_TRAIN}; \
  cp cfg/yolov3-tiny.template.cfg cfg/${CFG_PREDI}; \
    sed -i.bak 's/^## {BATCH_PARAM} ##/batch=1/g' cfg/${CFG_PREDI}; \
    sed -i.bak 's/^## {SUBDIVISION_PARAM} ##/subdivisions=1/g' ${CFG_PREDI}; \
    sed -i.bak 's/^## {CLASSES_PARAM} ##/classes='${CLASS_NUM}'/g' ${CFG_PREDI}; \
    sed -i.bak 's/^## {FILTERS_PARAM} ##/filters='${FILTERS}'/g' ${CFG_PREDI}; \
  rm ${CFG_TRAIN}.bak; \
  rm ${CFG_PREDI}.bak
```

### make dataset file 

```sh
$ set -x; \
  export CLASS_NUM=9; \
  export FILE_DB=cfg/dataset.txt; \
  export FILE_LBL=cfg/labels.txt; \
cat << EOT > ${FILE_DB}
classes=${CLASS_NUM}
train = temp/train/index.txt 
backup=backup/
labels=${FILE_LBL}
names=${FILE_LBL}
EOT
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

### yolo v3 tiny

In container

```sh
$ cd /opt/kby
$ ./prep.sh
$ export PATH=/opt/darknet:$PATH
$ darknet detector train \
    cfg/dataset.txt \
    cfg/yolov3-tiny.train.cfg \
    yolov3-tiny.conv.15
```

### yolo v2 tiny

In container

```sh
$ cd /opt/kby
$ ./prep.sh
$ export PATH=/opt/darknet:$PATH
$ darknet detector train \
    cfg/dataset.txt \
    cfg/yolov2-tiny.train.cfg \
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

## Keras yolo

### conver darknet weights to keras model

```sh
# yolo3(original)
$ cd keras-yolo3
$ wget https://pjreddie.com/media/files/yolov3.weights
$ pipenv run python3 convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
# tiny-yolo3
$ wget https://pjreddie.com/media/files/yolov3-tiny.weights
$ pipenv run python3 convert.py yolov3-tiny.cfg yolov3-tiny.weights model_data/yolo-tiny.h5
```

### run detect 

```sh
$ pipenv run python3 run_yolo3.py
$ pipenv run python3 run_yolo3tiny.py
```


## refs
- https://wakuphas.hatenablog.com/entry/2018/09/19/025941
- http://demura.net/misc/14458.html
- https://qiita.com/yoyoyo_/items/10d550b03b4b9c175d9c
