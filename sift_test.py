import cv2
import os
import Segmentation.panorama as p


def get(image):
    height, wight, deep = image.shape
    mianownik = 4
    height = int(height/mianownik)
    wight = int(wight/mianownik)
    image = cv2.resize(image, (wight, height))
    print(height,wight,deep)
    return image

pan = p.Stitcher()
imageA=cv2.imread("images/2.jpg")
imageB=cv2.imread("images/3.jpg")

imageA = get(imageA)
imageB = get(imageB)

"""
kps, features = pan.detectAndDescribe(imageB)
for kp in kps:
    x, y = kp
    cv2.circle(imageB, (x, y), 1, (0, 255, 0), 2)

#cv2.imwrite("images/kpB.jpg", imageB)
"""
#cv2.imshow("A", imageA)
#cv2.imshow("B", imageB)
result, vis = pan.stitch(images=[imageA, imageB], showMatches=True)
result = cv2.imshow("result", vis)
cv2.imwrite("images/kp_pan.jpg", vis)

cv2.waitKey(0)



cv2.destroyAllWindows()

