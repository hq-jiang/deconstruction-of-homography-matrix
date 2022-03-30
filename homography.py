import os
import math
from functools import partial
import argparse

import numpy as np
import cv2
    
def transform(img, factor, group="euclid"):
    """Apply perspective transform with selected homography"""
    
    height, width, _ = img.shape

    if group=="euclid" or group=="e":
        angle = math.pi*2/100. * factor
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        homography = np.array([
                [cos_a, -sin_a, 0],
                [sin_a, cos_a, 0],
                [0, 0, 1]
            ])
    elif group=="similarity" or group=="s":
        angle = math.pi*2/100. * factor
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        s = 1 + factor/100.

        homography = np.array([
                [s * cos_a, -s*sin_a, 0],
                [s*sin_a, s*cos_a, 0],
                [0, 0, 1]
            ])
    elif group=="affine" or group=="a":
        homography = np.array([
                [1 + factor/50., 0 + factor/20., 0],
                [0, 1 + factor/20., 0],
                [0, 0, 1]
            ])
    elif group=="projective" or group=="p":
        homography = np.array([
                [1, 0, 0],
                [0, 1, 0],
                [factor**2/100000., factor**2/100000., 1]
            ])

    # Target size of the image
    dst_size = (height*3//2, width*3//2)

    # Add a translation to the homography so the transformed image stays in center
    image_center = np.array([width/2, height/2, 1]).T
    warped_center = np.matmul(homography, image_center)
    new_image_center = np.array([dst_size[1]/2, dst_size[0]/2, 1]).T
    translation = new_image_center[0:2] - warped_center[0:2]
    homography[0:2,2] = translation
    
    transformed_img = cv2.warpPerspective(img, homography, dst_size, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    
    return transformed_img


def callback(value, img, group):
    """Callback for GUI"""
    transformed_img = transform(img, value, group=group)
    cv2.imshow("img", transformed_img)


if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Apply homography transforms', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--path', type=str, help='Path to input image', default="begonie.JPG")
    parser.add_argument('-i', '--interactive', type=str, help='Interactive mode for one chosen transform\n'
                                                              'Usage:\n'
                                                              '  -i euclid\n'
                                                              '  -i similarity\n'
                                                              '  -i affine\n'
                                                              '  -i projective\n'
                                                              'or\n'
                                                              '  -i e\n'
                                                              '  -i s\n'
                                                              '  -i a\n'
                                                              '  -i p\n')

    args = parser.parse_args()
    
    img = cv2.imread(args.path)

    if args.interactive:

        if args.interactive not in ["euclid", "similarity", "affine", "projective", "e", "s", "a", "p"]:
            raise ValueError(f"Interactive mode '{args.interactive}' not recognized")

        cv2.namedWindow("img", cv2.WINDOW_AUTOSIZE)
        cv2.createTrackbar("Warp", "img", 1, 100, partial(callback, img=img, group=args.interactive))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Processing euclidean transforms")
        transform_name = "euclid"
        os.makedirs(transform_name, exist_ok=True)
        for i in range (100):
            transformed_img = transform(img, i, group=transform_name)
            filepath = os.path.join(transform_name, f"{str(i).zfill(3)}.jpg")
            cv2.imwrite(filepath, transformed_img)

        print("Processing similarity transforms")
        transform_name = "similarity"
        os.makedirs(transform_name, exist_ok=True)
        for i in range (100):
            transformed_img = transform(img, i, group=transform_name)
            filepath = os.path.join(transform_name, f"{str(i).zfill(3)}.jpg")
            cv2.imwrite(filepath, transformed_img)


        print("Processing affine transforms")
        transform_name = "affine"
        os.makedirs(transform_name, exist_ok=True)
        for i in range (100):
            transformed_img = transform(img, i, group=transform_name)
            filepath = os.path.join(transform_name, f"{str(i).zfill(3)}.jpg")
            cv2.imwrite(filepath, transformed_img)

        print("Processing projective transforms")
        transform_name = "projective"
        os.makedirs(transform_name, exist_ok=True)
        for i in range (100):    
            transformed_img = transform(img, i, group=transform_name)
            filepath = os.path.join(transform_name, f"{str(i).zfill(3)}.jpg")
            cv2.imwrite(filepath, transformed_img)