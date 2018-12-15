import glob
import traceback
import argparse
 
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os

num_class = 7

base_path = './res'
save_base_path = './train_data/Images'
label_file = './cfg/labels.txt'

def generate_images(class_name, generator):
    # jpgファイル取得
    resdir = os.path.join(base_path, class_name)
    savedir = os.path.join(save_base_path, class_name)
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    images = glob.glob(resdir + '/*.jpg')
    print("input files = ", len(images))
 
    for image in images:
        image = load_img(image)
        x = img_to_array(image)
        x = np.expand_dims(x, axis=0)
        g = generator.flow(x, save_to_dir=savedir, save_prefix=class_name, save_format='jpg')
        
        # output画像をinputの何倍作成するか 1で1倍, 10で10倍
        for _ in range(3):
            g.next()
 
    print("output files = ", len(glob.glob(savedir + '/*.jpg')))
 
if __name__ == '__main__':
    num_class = len(open(label_file).readlines())
    print('num_class', label_file, num_class)

    parser = argparse.ArgumentParser()
    parser.add_argument("--start_class", type=int, required=False, default=0) # 0 =<
    parser.add_argument("--end_class", type=int, required=False, default=num_class-1) # < num_class
    args, unknown_args = parser.parse_known_args()

    start_class = args.start_class
    end_class = args.end_class + 1

    try:
        # 画像データの拡張パラメータを設定
        train_datagen = ImageDataGenerator(
            rotation_range=0., # 画像をランダムに回転する回転範囲（0-180）
            width_shift_range=0., # ランダムに水平シフトする範囲
            height_shift_range=0., # ランダムに垂直シフトする範囲
            shear_range=0.2, # シアー強度（反時計回りのシアー角度（ラジアン））
            zoom_range=0.2, # ランダムにズームする範囲
            horizontal_flip=True, # 水平方向に入力をランダムに反転
            vertical_flip=True, # 垂直方向に入力をランダムに反転
            rescale=1.0 / 255,  # 与えられた値をデータに積算する
            zca_whitening=True, 
            )
        for i in range(start_class, end_class):
            class_name = '{:0>3}'.format(i)
            generate_images(class_name, train_datagen)
 
    except Exception as e:
        traceback.print_exc()