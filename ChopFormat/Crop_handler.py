import cv2
from PIL import Image
import numpy as np
import os

color_dict = {'Blue': (0, 0, 255), 'Red': (255, 0, 0), 'Orange': (255, 127, 25)}

def crop(img_root, subdirs, img_name, left, upper, h, w, color, edge_width, resize_flag=None):

    if resize_flag == 'Keep dimension':
        pass
    elif resize_flag == 'Crop square area':
        h, w = max(h, w), max(h, w)
    img = np.array(Image.open(os.path.join(img_root, subdirs, img_name)))

    img = img[upper:upper+w, left:left+h, :3].copy()

    if resize_flag == 'Resize to square':
        h, w = (max(h, w), max(h, w))
        img = cv2.resize(img, (max(h, w), max(h, w)), cv2.INTER_LINEAR)
    H, W, _ = img.shape
    img = cv2.rectangle(img, (0, 0), (W, H), color=color, thickness=int(edge_width))
    return img, (h, w)


def draw_HRrec(HR_path, left, upper, h, w, color, edge_width):
    img = np.array(Image.open(HR_path))
    img_HR = cv2.rectangle(img, (left, upper), (left + h, upper + w), color, thickness=int(edge_width))

    return img_HR


if __name__ == '__main__':
    img = crop('E:\Workplace/visuals\AIM', 'AIM_DDASR', '0801.png', 100, 100, 512, 512, (255, 127, 25), 10)
    pil = Image.fromarray(img)
    pil.show()