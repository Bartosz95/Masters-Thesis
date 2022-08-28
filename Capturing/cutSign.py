import cv2
import os


def click_and_crop(event, x, y, flags, param):
    global refPt, cropping, number

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        x1, y1 = refPt[0]
        x2, y2 = refPt[1]
        roi = image[y1:y2, x1:x2]
        cv2.rectangle(image, (x1-5, y1-5), (x2+5, y2+5), COLOR, FONT_SIZE)
        name, extension = image_name.split('.')
        path_new_image = 'images/{}_{}.{}'.format(name, number, extension)
        number += 1
        cv2.imwrite(path_new_image, roi)


COLOR = (0, 255, 255)
FONT_SIZE = 2
path = "D:\Clouds\OneDrive\Polibuda\Praca magisterska\Programs\Images\my\Od Beatki"
image_names_paths = os.listdir(path)

for image_name in image_names_paths:
    try:
        image_path = os.path.join(path, image_name)
        image = cv2.imread(image_path)
        height, weight, channels = image.shape
        image = cv2.resize(image, dsize=(int(weight/5), int(height/5)), interpolation=cv2.INTER_CUBIC)
        number = 0
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", click_and_crop)
        while True:
            cv2.imshow("image", image)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
    except:
        pass

cv2.destroyAllWindows()
