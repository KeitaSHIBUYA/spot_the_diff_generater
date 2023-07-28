'''
マスクで指定した領域の色相を回転する
'''


import cv2
import os
import random
import numpy as np

gdrive = "/Users/keita/Documents/1F10180284_thesis/images/easy/"


# HSV H(色相)の変更
def changedH(hsv, shift):
    hsvimage = hsv.copy()
    hi = hsvimage[:, :, 0].astype(np.int32)
    if shift < 0:
        nhi = hi.flatten()
        for px in nhi:
            if px < 0:
                px = 180 - px
        nhi = nhi.reshape(hsvimage.shape[:2])
        hi = nhi.astype(np.uint8)
    chimg = (hi + shift) % 180
    hsvimage[:, :, 0] = chimg
    return hsvimage


# HSV H(色相)をマスクを用いて変更
def changedH2(hsv, shift, mask):
    hc = changedH(hsv, shift)
    cmask = cv2.merge((mask, mask, mask))
    parts = cv2.bitwise_and(hc, cmask)
    back = cv2.bitwise_and(hsv, cv2.bitwise_not(cmask))
    return cv2.bitwise_or(parts, back)


def main(bg_img, mask, deg):
    # 読み込み
    if isinstance(bg_img, str):
        img = cv2.imread(bg_img)
        mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # HSV H(色相)の変更
        hsv_result = changedH2(hsv.copy(), deg, mask)
        result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
        
        return result
    
    else:
        mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)
        hsv = cv2.cvtColor(bg_img, cv2.COLOR_BGR2HSV)

        # HSV H(色相)の変更
        hsv_result = changedH2(hsv.copy(), deg, mask)
        result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)

        return result


if __name__ == '__main__':
    image_path = gdrive + "02.png"
    mask_path = gdrive + "color/" + "circle.png"
    deg = random.randint(25, 100)
    print(-1 * deg)
    
    result = main(image_path, mask_path, -1 * deg)       # -25がデフォルト
    
    # 表示
    cv2.imshow('HSV - Hue changed', result)
    cv2.moveWindow("HSV - Hue changed", 2300, 500)
    cv2.waitKey(0)
