import cv2
import os
import numpy as np
import glob
import re

img_path = "/Users/keita/Documents/1F10180284_thesis/eye_tracking/saizeriya_images/right/"
save_path = "/Users/keita/Documents/1F10180284_thesis/eye_tracking/saizeriya_images/saliency_right/"

images = glob.glob(img_path + "*.*")

def create_saliency(images, save_path):
    for image in images:
            i = cv2.imread(image, 1)  # 画像読み込み
            filename = os.path.basename(image)

            # サリエンシーディテクション
            saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
            bool, map = saliency.computeSaliency(i)
            i_saliency = (map * 255).astype("uint8")                    # グレースケールのサリエンシーマップ

            result = cv2.applyColorMap(i_saliency, cv2.COLORMAP_JET)    # カラーマップ割り当て
            
            cv2.imwrite(save_path + filename, result)

create_saliency(img_path, save_path)

# img = "/Users/keita/Documents/1F10180284_thesis/eye_tracking/saizeriya_images/right/01.png"

# i = cv2.imread(img, 1)  # 画像読み込み

# # サリエンシーディテクション
# saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
# bool, map = saliency.computeSaliency(i)
# i_saliency = (map * 255).astype("uint8")                    # グレースケールのサリエンシーマップ

# result = cv2.applyColorMap(i_saliency, cv2.COLORMAP_JET)    # カラーマップ割り当て

# print(i_saliency)
# # 表示
# cv2.imshow('result', i_saliency)
# cv2.moveWindow("result", 2300, 500)  # 画面上の位置を調節する
# cv2.waitKey(0)
# cv2.destroyAllWindows()



'''

def main():

    # img = cv2.imread(os.path.dirname(os.path.abspath(__file__)) + "/images/" + "sample1_1.jpeg")
    img = cv2.imread(gdrive + "01.png")
    if img is None:
        exit()
    
    
    saliency = None
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()

    (success, saliencyMap) = saliency.computeSaliency(img)
    saliencyMap = (saliencyMap * 255).astype("uint8")

    # cv2.imshow('img',img)
    # cv2.imshow('srn',saliencyMap)


    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,3)
    # cv2.imshow('dst',dist_transform)
    ret, sure_fg = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    fig, ax = plt.subplots(figsize=(6, 6))
    # ax.imshow(markers, cmap="tab20b")
    # plt.show()

    markers = cv2.watershed(img,markers)
    img[markers == -1] = [255,0,0]
    
    cv2.imshow('result', saliencyMap)
    # cv2.imshow('result', moved_img)
    cv2.moveWindow("result", 2300, 000)  # 画面上の位置を調節する
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # cv2.waitKey()
    # cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/SaliencyMap.png", saliencyMap)

if __name__=='__main__':
    main()
'''