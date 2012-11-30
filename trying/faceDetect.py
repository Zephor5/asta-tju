#!/usr/bin/python
# coding=utf-8

# faceDect.py

# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b

# Usage: python faceDect.py <image_file>

#import sys, os
import cv2.cv as cv
from PIL import Image, ImageDraw

def detectObjects(image):
    xml_path='../data/'
    """Converts an image to grayscale and prints the locations of any faces found"""
    storage = cv.CreateMemStorage()

    cascade = cv.Load(xml_path+'haarcascade_frontalface_alt.xml')
    faces = cv.HaarDetectObjects(image, cascade, storage)

    result = []
    for (x,y,w,h),n in faces:
        result.append((x, y, x+w, y+h))

    return result

def process(infile, outfile):
    try:
        image = cv.LoadImage(infile)
    except:
        print 'input file wrong'
        return
    if image:
        faces = detectObjects(image)

    im = Image.open(infile)

    if faces:
        draw = ImageDraw.Draw(im)
        for f in faces:
            draw.rectangle(f, outline=(255, 0, 255))

        im.save(outfile, "JPEG", quality=100)
    else:
        print "Error: cannot detect faces on %s" % infile

if __name__ == "__main__":
    process('1.jpg', 'output1.jpg')