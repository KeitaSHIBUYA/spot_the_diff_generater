import cv2
import numpy as np


fore_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/2007_trim.png")


back_img = cv2.imread(
    "/Users/keita/Documents/1F10180284_thesis/Mask/archive/0.png")



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

if __name__ == '__main__':
    img = create_mask(back_img)
    
    cv2.imshow("mask", fore_img)
    cv2.moveWindow("mask", 2300, 500)  # 画面上の位置を調節する
    cv2.waitKey(0)
    cv2.destroyAllWindows()



'''
### デバッグ用

# グレースケールに変換する。
gray = cv2.cvtColor(back_img, cv2.COLOR_BGR2GRAY)
gray = 255 - gray

# 2値化する。
ret, bin_img = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

# 輪郭抽出する。
contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 面積が最大の輪郭を取得する
contour = max(contours, key=lambda x: cv2.contourArea(x))

# マスク画像を作成する。
mask = np.zeros_like(bin_img, dtype=np.uint8)
cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)

# マスク処理
result = cv2.bitwise_and(back_img, back_img, mask=mask)

cv2.imshow("mask", result)
cv2.moveWindow("mask", 2300, 500)  # 画面上の位置を調節する
cv2.waitKey(0)
cv2.destroyAllWindows()
'''