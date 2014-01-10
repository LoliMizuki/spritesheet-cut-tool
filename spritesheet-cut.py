# -*- coding: UTF-8 -*-
#!/usr/bin/env python

# TODO: 輸出同時, 順便 rename
# TODO: 不等比出圖 -- cut TexturePacker ... get info from .plist file

import os
import sys
import Image

version = "0.2"
appName = ""


def is_argvs_enough_to_work():
    return len(sys.argv) == 4


def cut_image_into_frames(image_path, deciles_in_width, deciles_in_height):

    if os.path.exists(image_path) == False:
        print "not exists image file: " + image_path
        sys.exit()

    image = Image.open(image_path)

    img_width = get_width(image.size)
    img_height = get_height(image.size)

    if img_width % deciles_in_width != 0 or img_height % deciles_in_height != 0:
        print "illegal deciles"
        sys.exit()

    frame_width = img_width / deciles_in_width
    frame_height = img_height / deciles_in_height

    image_name_without_ext = os.path.basename(image_path).split(".")[0]
    
    output_path = os.path.dirname(image_path) + "/"
    os.chdir(output_path)

    for w in range(deciles_in_width):
        for h in range(deciles_in_height):
            frame_left = frame_width * w
            frame_top = frame_height * h
            frame_right = frame_left + frame_width
            frame_botton = frame_top + frame_height

            cut_rect = (frame_left, frame_top, frame_right, frame_botton)
            frame_image = image.crop(cut_rect)

            frame_file_name = "{}-{}-{}.{}".format(
                image_name_without_ext, w, h, image.format.lower())
            frame_image.save(frame_file_name)
            print "create frame: " + frame_file_name


def get_width(size):
    return size[0]


def get_height(size):
    return size[1]

if __name__ == '__main__':

    appName = os.path.basename(__file__)

    if is_argvs_enough_to_work() == False:
        print """usege:
    python {} <image_path> <deciles_in_width> <deciles_in_height>
    -- will create cuted frames from image.
    (ver={})""".format(appName, version)
        sys.exit()

    try:
        image_path = sys.argv[1]
        deciles_in_width = int(sys.argv[2])
        deciles_in_height = int(sys.argv[3])
    except ValueError:
        print "decile must be INTEGER"
        sys.exit()

    cut_image_into_frames(image_path, deciles_in_width, deciles_in_height)
