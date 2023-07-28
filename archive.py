'''
### 座標設定の方法メモ ###

- あらかじめ座標のパターンを用意しておく
'''

import os
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

back_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/2007_test.png")

back_img_2 = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/images/easy/01.png")

circle_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/images/easy/size/img/circle.png")

sheep_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/images/easy/add/sheep.png")

boy_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/2007_trim.png")

cloud_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/0.png")




### 処理に必要なマスクの作成
def create_mask(img):
    # グレースケールに変換する。
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255 - gray

    # 2値化する。
    ret, bin_img = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    # 輪郭抽出する。
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 面積が最大の輪郭を取得する
    contour = max(contours, key=lambda x: cv2.contourArea(x))

    # マスク画像を作成する。
    mask = np.zeros_like(bin_img)
    cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
    
    # マスク処理
    result = cv2.bitwise_and(img, img, mask=mask)
    
    return result


### 拡大縮小・平行移動・回転
def processing(fore_img, back_img, deg=0, scale=0, dx=0, dy=0):
    # 画像サイズの取得
    fore_h, fore_w = fore_img.shape[:2]
    back_h, back_w = back_img.shape[:2]
    
    # 回転・拡大・縮小
    M = cv2.getRotationMatrix2D((int(fore_w/2), int(fore_h/2)), deg, scale)
    rotated_img = cv2.warpAffine(fore_img, M, (back_w, back_h))

    # 移動
    M = np.array([[1, 0, dx], [0, 1, dy]], dtype=float)
    moved_img = cv2.warpAffine(rotated_img, M, (back_w, back_h))

    # 二値化処理
    foreimg_gray = cv2.cvtColor(moved_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(foreimg_gray, 5, 255, cv2.THRESH_BINARY)

    # 輪郭抽出
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    max_cnt = max(contours, key=lambda x: cv2.contourArea(x))

    # マスク画像の作成
    mask = cv2.drawContours(foreimg_gray, [max_cnt], -1, 255, -1)
    
    # 移動後の前面画像のサイズ取得
    h, w = moved_img.shape[:2]
    x, y = 0, 0
    
    fg_roi = moved_img[:h, :w]
    bg_roi = back_img[y : y + h, x : x + w]

    result = np.where(mask[:back_h, :back_w, np.newaxis] == 0, bg_roi, fg_roi)
    
    # デバッグ用
    cv2.imshow('result', result)
    # cv2.imshow('result', moved_img)
    cv2.moveWindow("result", 2300, 000)  # 画面上の位置を調節する
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return result


def main():
    # 男の子
    # img = create_mask(boy_img)
    # processing(img, back_img, 90, 1.0, 290, 270)
    
    # 雲
    # img = create_mask(cloud_img)
    # processing(img, back_img, 0, 0.5, 180, 5)
    
    # 拡大・縮小テスト
    img = create_mask(circle_img)
    # pos_x = random.randint(250, 280)
    pos_x = 280
    # pos_y = random.randint(5, 30)
    pos_y = 30
    
    
    # print(pos)
    
    processing(img, back_img_2, deg=0, scale=1.0, dx=pos_x, dy=pos_y)
    processing(img, back_img_2, deg=0, scale=0.8, dx=pos_x, dy=pos_y)
    
    
    # processing(create_mask(sheep_img), back_img_2, 0, 1.0, 280, 50)

if __name__ == '__main__':
    main()


'''
back_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/2007_test.png")

boy_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/2007_trim.png")

cloud_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/0.png")


### 処理に必要なマスクの作成
def create_mask(img):
    # グレースケールに変換する。
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255 - gray

    # 2値化する。
    ret, bin_img = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    # 輪郭抽出する。
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 面積が最大の輪郭を取得する
    contour = max(contours, key=lambda x: cv2.contourArea(x))

    # マスク画像を作成する。
    mask = np.zeros_like(bin_img)
    cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
    
    # マスク処理
    result = cv2.bitwise_and(img, img, mask=mask)
    
    return result


### 回転処理
def processing(fore_img, back_img, deg, scale, dx, dy):
    
    
    # 画像サイズの取得
    fore_h, fore_w = fore_img.shape[:2]
    back_h, back_w = back_img.shape[:2]
    
    # 回転
    M = cv2.getRotationMatrix2D((int(fore_w/2), int(fore_h/2)), deg, scale)
    rotated_img = cv2.warpAffine(fore_img, M, (back_w, back_h))

    # 移動
    M = np.array([[1, 0, dx], [0, 1, dy]], dtype=float)
    moved_img = cv2.warpAffine(rotated_img, M, (back_w, back_h))
    
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__)) + "/moved_img.png", moved_img)

    # 二値化処理
    foreimg_gray = cv2.cvtColor(moved_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(foreimg_gray, 5, 255, cv2.THRESH_BINARY)

    # 輪郭抽出
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    max_cnt = max(contours, key=lambda x: cv2.contourArea(x))

    # マスク画像の作成
    mask = cv2.drawContours(foreimg_gray, [max_cnt], -1, 255, -1)
    
    # 移動後の前面画像のサイズ取得
    h, w = moved_img.shape[:2]
    x, y = 0, 0
    
    fg_roi = moved_img[:h, :w]
    bg_roi = back_img[y : y + h, x : x + w]

    result = np.where(mask[:back_h, :back_w, np.newaxis] == 0, bg_roi, fg_roi)
    
    # デバッグ用
    cv2.imshow('result', result)
    # cv2.imshow('result', moved_img)
    cv2.moveWindow("result", 2300, 500)  # 画面上の位置を調節する
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return result

def main():
    # 男の子
    img = create_mask(boy_img)
    processing(img, back_img, 90, 1.0, 290, 270)
    
    # 雲
    # img = create_mask(cloud_img)
    # processing(img, back_img, 0, 0.5, 180, 5)


if __name__ == '__main__':
    main()

'''