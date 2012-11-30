#!/usr/bin/python
# -*- coding: UTF-8 -*-

# face_detect.py

# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b

# Usage: python face_detect.py <image_file>

import os,cv2,time,numpy#,cPickle as P

def timeit(func):
 
    # 定义一个内嵌的包装函数，给传入的函数加上计时功能的包装
    def wrapper():
        start = time.clock()
        func()
        end =time.clock()
        print 'used:', end - start
 
    # 将包装后的函数返回
    return wrapper

class cvTest(object):
    """docstring for cvTest"""
    def __init__(self,imname='test.jpg'):
        try:
            if not os.path.isfile(imname):
                raise Exception('图片不存在')
        except Exception,e:
            print '错误：%s' % e
            exit()
        self.winname='testcv'
        self.image = cv2.imread(imname)
        self.curImage=numpy.copy(self.image)
        #print self.image.

    def showImage(self,dic=None):
        #print self.image[0][0][1]
        if type(dic) == dict:
            for wname in dic:
                cv2.namedWindow(wname,1)
                cv2.imshow(wname,dic[wname])
            cv2.waitKey(0)
        else:
            cv2.namedWindow(self.winname,1)
            cv2.imshow(self.winname,self.curImage)
            cv2.waitKey(0)

    def plus(self):
        for x in xrange(0,len(self.curImage)):
            for y in xrange(0,len(self.curImage[x])):
                for z in xrange(0,len(self.curImage[x][y])):
                    #print len(self.curImage[x])
                    self.curImage[x][y][z]=0 if self.curImage[x][y][z]-50<0 else self.curImage[x][y][z]-50
                    z+=1
                    #break
                #print self.curImage[x][y]
                y+=1
                #break
            x+=1
            #break
        #print x,y,z
    def test(self):
        #P.dump(self.image,file('test','w'))
        print self.curImage.__len__()
        #x=[[[12,12,12],[12,12,12]],[[12,12,12],[12,12,12]]]
        #print type(x),numpy.ndarray(1)
        #cv2.creatImage([[[123,123,123]]])
        #for x in range(1,10):
            #print x

test=cvTest('1.jpg')
#test.showImage()
test.plus=timeit(test.plus)
test.plus()
test.showImage({u'原图'.encode('gbk'):test.image,u'变换后'.encode('gbk'):test.curImage})
#test.test()
#test.showImage()
#print type(test.image)