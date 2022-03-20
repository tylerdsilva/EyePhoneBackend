
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Plot image
def plot_image(img, title=None):
    plt.figure(figsize=(15,20))
    plt.title(title)
    plt.imshow(img)
    plt.show()
    
# Draw elipsis on image
def draw_ellipse(mask):
    m3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    contours, hierarchy = cv2.findContours(mask, 1, 2)
    has_ellipse = len(contours) > 0
    if has_ellipse:
        cnt = contours[0]
        ellipse = cv2.fitEllipse(cnt)
        cx, cy = np.array(ellipse[0], dtype=np.int)
        m3[cy-2:cy+2,cx-2:cx+2] = (255, 0, 0)
        cv2.ellipse(m3, ellipse, (0, 255, 0), 1)
        # print("ellipse", ellipse)

        ellipseLength = ellipse[0][0]
        ellipseWidth = ellipse[0][1]

    return has_ellipse, m3, max(ellipseWidth, ellipseLength)

def computeEllipse(masks):
    pupilDiameters = []
    files_with_ellipse = 0
    for mask in masks:
        # mask = cv2.imread(mask, 0)  # imread(..., -1) returns grayscale images
        has_ellipse, mask_with_ellipse, diameter = draw_ellipse(mask)
        if has_ellipse:
            pupilDiameters.append(diameter)
            files_with_ellipse = files_with_ellipse+1
            # plot_image(mask_with_ellipse, mask)
    return pupilDiameters