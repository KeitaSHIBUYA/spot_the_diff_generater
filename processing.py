'''
### 座標設定の方法メモ ###

- あらかじめ座標のパターンを用意しておく
- Lamaでオブジェクトを消去するときに使うマスクで座標を設定する
'''

import os

import cv2
import numpy as np

mode = "easy"       # for debug

# 実行ファイルパスを文字列で取得
path_str = os.path.dirname(os.path.abspath(__file__))

# for debug_img
back_img_2 = path_str + "/images/" + mode + "/02.png"

circle_img = path_str + "/images/" + mode + "/size/img/circle.png"
test_add = path_str + "/images/" + mode + "/size/img/circle.png"
test_mask = path_str + "/images/" + mode + "/size/circle.png"

test_img = path_str + "/images/" + mode + "/add/flower.png"



color_dict = {
    "grill.png": 255,
    "sarad.png": 255,
    "flower.png": np.array([53, 201, 179]),
    "saize.png": np.array([77, 183, 33]),
    "circle.png": np.array([28, 147, 247]),
    "doria.png": np.array([73, 173, 65]),
    "star.png": np.array([73, 173, 65]),
}


### 処理に必要なマスクの作成
def create_mask(path):
    img = cv2.imread(path)
    
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

### オブジェクトを塗りつぶす（拡大・縮小の際に使用）
def fill(base, target_path):
    mask = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)
    h, w = base.shape[:2]

    for i in range(h):
        for j in range(w):
            if mask[i, j] != 0:
                # 塗りつぶす対象の名前をキーとしてcolor_dictから塗りつぶしの色を取得
                base[i, j] = color_dict[os.path.basename(target_path)]
                # print(base[i, j])     # for debug

    return base


### 拡大縮小・平行移動・回転・追加
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

    # 背景と同じサイズでマスク画像を作成
    mask = cv2.drawContours(foreimg_gray, [max_cnt], -1, 255, -1)
    
    # 移動後の前面画像のサイズ取得
    h, w = moved_img.shape[:2]
    x, y = 0, 0
    
    fg_roi = moved_img[:h, :w]
    bg_roi = back_img[y : y + h, x : x + w]

    result = np.where(mask[:back_h, :back_w, np.newaxis] == 0, bg_roi, fg_roi)
    
    return result



def main():
    # 拡大・縮小テスト
    back_img = cv2.imread(back_img_2)
    
    # imgに処理した画像を代入する
    # この場合は、以下のようなイメージ
    '''
    02.pngの中にあるcircleをtest_mask（circleを覆うマスク画像）で塗りつぶした画像を背景とする
    上記の背景画像に対してcircleを縮小した画像を貼り付ける
    座標は（288, 25）でスケールは0.8倍、角度の変更は無し
    
    '''
    img = processing(create_mask(test_img), fill(back_img, test_mask), deg=0, scale=1.0, dx=530, dy=250)
    # img2 = processing(create_mask(grill_img), img, deg=0, scale=1.0, dx=100, dy=100)
    

    # for debug
    cv2.imshow('result', img)
    # cv2.imshow('result', moved_img)
    cv2.moveWindow("result", 2300, 000)  # 画面上の位置を調節する
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    
if __name__ == '__main__':
    main()