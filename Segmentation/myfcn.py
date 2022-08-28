import cv2
import numpy as np


param_1 = 1
param_2 = 100
max_value = 100
window_name = "window"
# cv2.createTrackbar("param 1", window_name, param_1, max_value, trackbar_1)
# cv2.createTrackbar("param 2", window_name, param_2, max_value, trackbar_2)


def trackbar_1(val):
    global param_1
    param_1 = val
    cv2.setTrackbarPos("param 1", window_name, val)


def trackbar_2(val):
    global param_2
    param_2 = val
    cv2.setTrackbarPos("param 2", window_name, val)

def rgb_equalized_hist(image):
    channels = cv2.split(image)
    eq_channels = []
    for ch, color in zip(channels, ['B', 'G', 'R']):
        eq_channels.append(cv2.equalizeHist(ch))
    eq_image = cv2.merge(eq_channels)
    return eq_image


def hsv_equalized_hist(image):
    H, S, V = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    V = cv2.equalizeHist(V)
    #S[:] = 127#cv2.equalizeHist(S)
    eq_image = cv2.cvtColor(cv2.merge([H, S, V]), cv2.COLOR_HSV2BGR)
    return eq_image


def filter(image):
    isSign = True
    b, g, r = cv2.split(image)
    img = np.array(cv2.equalizeHist(b) * 0.01 * 21 - cv2.equalizeHist(r) * 0.01 * 24, np.uint8)

    img = cv2.resize(img, (50, 50))
    cv2.rectangle(img, (0, 0), (49, 49), (255, 255, 255), 2)

    kernel = np.ones((3, 3), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
    _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

    _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    """
    window_name = 'normal_{}'.format("")
    cv2.namedWindow(window_name)
    img = cv2.resize(img, (400, 400))
    cv2.imshow(" ", img)
    
    for cnt in contours:
        hull = cv2.convexHull(cnt, False)
        if len(hull) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            l1, l2 = ellipse[1]
            P = l1*l2*np.pi/2
            return "{}, {}".format(int(P), int(max(l1, l2)/min(l1, l2)))
    """
    return isSign


def region_of_interest(image):
    height = image.shape[0]
    weight = image.shape[1]
    y1 = 0
    y2 = int(height/2)
    x1 = 0
    x2 = int(weight)
    image_roi = image[y1:y2, x1:x2]
    return image_roi


def drawMatches(imageA, imageB, kpsA, kpsB, matches, status):
    # initialize the output visualization image
    (hA, wA) = imageA.shape[:2]
    (hB, wB) = imageB.shape[:2]
    vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
    vis[0:hA, 0:wA] = imageA
    vis[0:hB, wA:] = imageB

    # loop over the matches
    i = 1
    for ((trainIdx, queryIdx), s) in zip(matches, status):
        # only process the match if the keypoint was successfully
        # matched
        if s == 1:
            # draw the match
            ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
            ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
            cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

    # return the visualization
    return vis


def create_panorama(img, img_):
    img1 = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.ORB_create()#xfeatures2d.SURF_create()#SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)


    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    status = []
    for m in matches:
        if m[0].distance < 0.5*m[1].distance:
            good.append(m)
    matches = np.asarray(good)

    if len(matches[:, 0]) >= 2:
        src = np.float32([kp1[m.queryIdx].pt for m in matches[:, 0]]).reshape(-1, 1, 2)
        dst = np.float32([kp2[m.trainIdx].pt for m in matches[:, 0]]).reshape(-1, 1, 2)

        H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        # print H
    else:
        raise AssertionError('Can’t find  enough keypoints.')

    dst = cv2.warpPerspective(img_, H, (img.shape[1] + img_.shape[1], img.shape[0]))
    dst[0:img.shape[0], 0:img.shape[1]] = img
    return dst

