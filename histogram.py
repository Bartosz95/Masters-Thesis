import cv2
import os

path = "D:\Clouds\OneDrive\Polibuda\Praca magisterska\Programs\Project\images\Dataset\\blue\Training\\00000"
image_names = os.listdir(path)

color = 0

for image_name in image_names:
    p = os.path.join(path,image_name)
    image = cv2.imread(p)
    cv2.imshow("", image)
    height, weight, deep, = image.shape
    hist = []
    for w in range(weight):
        sum = 0
        for h in range(height):
            sum += image[h][w][color]
        sum = int(sum/height)
        hist.append(sum)
    print(hist)

    cv2.waitKey(0)
cv2.destroyAllWindows()
