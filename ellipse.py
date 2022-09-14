
import cv2
import numpy as np
# import matplotlib.pyplot as plt
#
# # Plot image
# def plot_image(img, title=None):
#     plt.figure(figsize=(15,20))
#     plt.title(title)
#     plt.imshow(img)
#     plt.show()
    
# Draw elipsis on image
def draw_ellipse(mask):
    width = None
    print("before squeeze", mask)
    mask = np.squeeze(mask)
    print("after", mask)
    # m3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    has_ellipse = len(contours) > 0

    if has_ellipse:
        cnt = contours[0]
        ellipse = cv2.fitEllipse(cnt)
        cx, cy = np.array(ellipse[0], dtype=np.int)
        # m3[cy-2:cy+2,cx-2:cx+2] = (255, 0, 0)
        # cv2.ellipse(m3, ellipse, (0, 255, 0), 1)
        # print("ellipse", ellipse)

        ellipseLength = ellipse[0][0]
        ellipseWidth = ellipse[0][1]
        width = max(ellipseWidth, ellipseLength)

    return has_ellipse, width

def computeEllipse(masks):
    pupilDiameters = []
    for mask in masks:
        # mask = cv2.imread(mask, 0)  # imread(..., -1) returns grayscale images
        has_ellipse, diameter = draw_ellipse(mask)
        pupilDiameters.append(diameter)
            # plot_image(mask_with_ellipse, mask)
    return pupilDiameters