import glob
import os
import random
import re

import change_color
import cv2
import processing
import datetime

mode = "normal"

# 実行ファイルパスを文字列で取得
path_str = os.path.dirname(os.path.abspath(__file__))
# print(path_str)     # for debug

### 背景とマスク画像をそれぞれリスト "*_list" で取得する
bg_list = glob.glob(path_str + "/images/" + mode + "/*.*")
# print(bg_list)      # for debug

add_list = glob.glob(
    path_str + "/images/" + mode + "/add/*.*")

color_list = glob.glob(
    path_str + "/images/" + mode + "/color/*.*")

size_images = glob.glob(
    path_str + "/images/" + mode + "/size/img/*.*")

size_masks = glob.glob(
    path_str + "/images/" + mode + "/size/*.*")

range_dict = {
    "star.png":  [[5, 320],
                  [5, 420]],
    "grass.png":  [[540, 400],
                   [540, 500]],
    "grill.png":  [130, 250],
    "circle.png": [288, 25],
    "saize.png":  [418, 54],
    "sarad.png":  [450, 265],
    "flower.png": [510, 210],
    "doria.png":  [20, 322],
}

# print(range_dict["sheep.png"])          # for debug

### 画像に間違いを生成する （normalは色変化2つ、消去・大きさ変化・追加が1つずつ）


def create_difference(bg_img, add_img, color_mask, size_mask):

    deg1 = random.randint(15, 25)       # 色相の角度を15~25の範囲で与える
    deg2 = random.randint(15, 25)       # 色相の角度を15~25の範囲で与える

    color_changed_img = 0
    added_img = 0

    # dict_keyを参照するためのファイル名を文字列で取得
    dict_key = os.path.basename(add_img)
    # print("add:", dict_key)     # for debug
    # print("key:", range_dict[dict_key][0][0], range_dict[dict_key][1][0])     # for debug

    x_rand = random.randint(
        range_dict[dict_key][0][0], range_dict[dict_key][1][0])
    y_rand = random.randint(
        range_dict[dict_key][0][1], range_dict[dict_key][1][1])

    # 画像とマスクを確認する
    # 背景画像の中に色変化オブジェクトがない場合はもう一度実行する
    if (os.path.basename(bg_img) == os.path.basename(color_mask[0]) or
            os.path.basename(bg_img) == os.path.basename(color_mask[1])):
        print("背景画像の中に色変化オブジェクトが存在しません。", "\n", "もう一度実行します。")
        print("---------------------------")
        main()

    else:
        # 色変化
        print("削除:", os.path.basename(bg_img), "\n",
              "色変化1:", deg1, "度", os.path.basename(color_mask[0]), "\n",
              "色変化2:", deg2, "度", os.path.basename(color_mask[1]))
        color_changed_img = change_color.main(
            bg_img, color_mask[0], (-1 * deg1))
        color_changed_img = change_color.main(
            color_changed_img, color_mask[1], (-1 * deg2))
        # 追加
        print("add:", dict_key)
        print("[x:", x_rand, ",y:", y_rand, "]")
        added_img = processing.processing(processing.create_mask(
            add_img), color_changed_img, deg=0, scale=1.0, dx=x_rand, dy=y_rand)
        # 拡大・縮小
        size_name = os.path.basename(size_mask)     # ファイル名取得
        print("scale:", size_name)
        filled_img = processing.fill(added_img, size_mask)
        scaled_img = processing.processing(
            processing.create_mask(path_str + "/images/" + mode + "/size/img/" + size_name), filled_img, 0, 0.8, range_dict[size_name][0], range_dict[size_name][1])

        # 表示
        # cv2.imshow(mode, scaled_img)
        cv2.imshow(mode, scaled_img)
        cv2.moveWindow(mode, 2300, 000)
        cv2.waitKey(0)

    # result = added_img
    result = scaled_img

    return result


def now_time():
    now = datetime.datetime.now()
    new = "{0:%Y_%m%d_%H%M}".format(now)
    filename = path_str + "/images/result/" + mode + "/" + new + ".png"

    return filename


def main():
    img = create_difference(random.choice(bg_list), random.choice(
        add_list), random.sample(color_list, 2), random.choice(size_masks))
    
    cv2.imwrite(now_time(), img)

if __name__ == "__main__":
    main()


'''
def main():
    total = 0
    while total < 4:
        add_num = random.randint(0, 1)
        color_num = random.randint(1, 2)
        size_num = random.randint(1, 2)
        total = add_num + color_num + size_num
    
    print(add_num, color_num, size_num)
    create_difference(random.choice(bg_list), add_num, color_num, size_num)


### 追加（シームレスクローン）
def add(target_path, base_path, mask, point):
    target  = cv2.imread(target_path, cv2.IMREAD_COLOR)
    base  = cv2.imread(base_path, cv2.IMREAD_COLOR)
    # mask = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)
    
    result1 = cv2.seamlessClone( target, base, mask, point, cv2.NORMAL_CLONE)
    cv2.imshow('NORMAL_CLONE', result1)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
    print("まだ全然できてないよ")
'''
