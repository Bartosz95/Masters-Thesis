import cv2
import os
import pickle
import myTSR

refPt = []
cropping = False


def click_and_crop0(event, x, y, flags, param):
    global refPt, cropping, signs_0

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        x1, y1 = refPt[0]
        x2, y2 = refPt[1]
        cv2.rectangle(image[0], refPt[0], refPt[1], COLOR, FONT_SIZE)
        cv2.putText(image[0], signs_type, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, FONT_SIZE, 1)
        signs_0[1].append(((x1, y1, x2, y2), signs_type, signs_color))


def click_and_crop1(event, x, y, flags, param):
    global refPt, cropping, signs_1

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        x1, y1 = refPt[0]
        x2, y2 = refPt[1]
        cv2.rectangle(image[1], refPt[0], refPt[1], COLOR, FONT_SIZE)
        cv2.putText(image[1], signs_type, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, FONT_SIZE, 1)
        signs_1[1].append(((x1, y1, x2, y2), signs_type, signs_color))


def click_and_crop2(event, x, y, flags, param):
    global refPt, cropping, signs_2

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        x1, y1 = refPt[0]
        x2, y2 = refPt[1]
        cv2.rectangle(image[2], refPt[0], refPt[1], COLOR, FONT_SIZE)
        cv2.putText(image[2], signs_type, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, FONT_SIZE, 1)
        signs_2[1].append(((x1, y1, x2, y2), signs_type, signs_color))


def save_signs():
    pickle_path = os.path.join(path, pickles[0])
    pickle_out = open(pickle_path, "wb")
    pickle.dump(saved_signs0, pickle_out)
    pickle_out.close()

    pickle_path = os.path.join(path, pickles[1])
    pickle_out = open(pickle_path, "wb")
    pickle.dump(saved_signs1, pickle_out)
    pickle_out.close()

    pickle_path = os.path.join(path, pickles[2])
    pickle_out = open(pickle_path, "wb")
    pickle.dump(saved_signs2, pickle_out)
    pickle_out.close()


def get_saved_signs():
    pickle_path = os.path.join(path, pickles[0])
    pickle_in = open(pickle_path, "rb")
    saved_signs0 = pickle.load(pickle_in)

    pickle_path = os.path.join(path, pickles[1])
    pickle_in = open(pickle_path, "rb")
    saved_signs1 = pickle.load(pickle_in)

    pickle_path = os.path.join(path, pickles[2])
    pickle_in = open(pickle_path, "rb")
    saved_signs2 = pickle.load(pickle_in)
    return saved_signs0, saved_signs1, saved_signs2


path = "images/Benchmark"
files = os.listdir(path)
cameras = []
pickles = []
for file in files:
    if len(file.split('.')) >= 2:
        pickles.append(file)
    else:
        cameras.append(file)

print(cameras)
path_to_images = []
for camera in cameras:
    path_to_images.append(os.path.join(path, camera))

image_names_paths = []
for path_to_image in path_to_images:
    image_names = os.listdir(path_to_image)
    images_paths = []
    for image_name in image_names:
        images_paths.append(os.path.join(path_to_image, image_name))
    image_names_paths.append(images_paths)

try:
    saved_signs0, saved_signs1, saved_signs2 = get_saved_signs()
except Exception:
    saved_signs0 = []
    saved_signs1 = []
    saved_signs2 = []

signs_type = 'zakaz ruchu busow'
signs_color = 'red'
key = None
COLOR_BLUE = (255, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_YELLOW = (0, 255, 255)
COLOR_GREEN = (0, 255, 0)
FONT_SIZE = 1

for i in range(len(image_names_paths[0])):
    image = []
    clone = []
    name = []

    for j in range(len(cameras)):
        image.append(cv2.imread(image_names_paths[j][i]))
        clone.append(image[j].copy())
        name.append(cameras[j])
        cv2.namedWindow(name[j])

    cv2.setMouseCallback(name[0], click_and_crop0)
    cv2.setMouseCallback(name[1], click_and_crop1)
    cv2.setMouseCallback(name[2], click_and_crop2)

    try:
        signs_0 = saved_signs0[i]
        signs_1 = saved_signs1[i]
        signs_2 = saved_signs2[i]

        for sign in signs_0[1]:
            [x1, y1, x2, y2], signs_name, color = sign
            COLOR = None
            if color == 'blue':
                COLOR = COLOR_BLUE
            elif color == 'red':
                COLOR = COLOR_RED
            if color == 'yellow':
                COLOR = COLOR_YELLOW
            cv2.rectangle(image[0], (x1, y1), (x2, y2), COLOR, FONT_SIZE)
            cv2.putText(image[0], signs_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GREEN, FONT_SIZE, 1)

        for sign in signs_1[1]:
            [x1, y1, x2, y2], signs_name, color = sign
            COLOR = None
            if color == 'blue':
                COLOR = COLOR_BLUE
            elif color == 'red':
                COLOR = COLOR_RED
            if color == 'yellow':
                COLOR = COLOR_YELLOW
            cv2.rectangle(image[1], (x1, y1), (x2, y2), COLOR, FONT_SIZE)
            cv2.putText(image[1], signs_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GREEN, FONT_SIZE, 1)

        for sign in signs_2[1]:
            [x1, y1, x2, y2], signs_name, color = sign
            COLOR = None
            if color == 'blue':
                COLOR = COLOR_BLUE
            elif color == 'red':
                COLOR = COLOR_RED
            if color == 'yellow':
                COLOR = COLOR_YELLOW
            cv2.rectangle(image[2], (x1, y1), (x2, y2), COLOR, FONT_SIZE)
            cv2.putText(image[2], signs_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GREEN, FONT_SIZE, 1)

    except Exception as e:
        print("New")
        signs_0 = [clone[0], []]
        signs_1 = [clone[1], []]
        signs_2 = [clone[2], []]

    print(signs_type, signs_color)

    while True:
        for j in range(len(cameras)):
            cv2.imshow(name[j], image[j])
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            for j in range(len(cameras)):
                image[j] = clone[j].copy()
            signs_0 = [clone[0], []]
            signs_1 = [clone[1], []]
            signs_2 = [clone[2], []]
        elif key == ord("n") or signs_type is None:
            signs_type = input("Write type of signs: ")
            print(signs_type, signs_color)
        elif key == ord("c") or signs_color is None:
            signs_color = input("-blue\n-red\n-yellow\nWrite color of signs: ")
            print(signs_type, signs_color)
        elif key == ord("s") or key == ord("q"):
            break

    try:
        saved_signs0[i], saved_signs1[i], saved_signs2[i] = [signs_0, signs_1, signs_2]
    except Exception:
        saved_signs0.append(signs_0)
        saved_signs1.append(signs_1)
        saved_signs2.append(signs_2)
    finally:
        save_signs()

    if key == ord("q"):
        break

cv2.destroyAllWindows()
