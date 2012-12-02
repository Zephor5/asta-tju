#!/usr/bin/python
# -*- coding: UTF-8 -*-

# testCv.py

# opencv2 api测试
# http://blog.x-5.me

# Usage: custom
from __future__ import division     #this must be put at the beginning
import os,cv2,time,numpy as np#,cPickle as P

def timeit(func):
 
    # 定义一个内嵌的包装函数，给传入的函数加上计时功能的包装
    def wrapper(self):
        start = time.clock()
        func(self)
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
        x=np.size(self.image,1)
        y=np.size(self.image,0)
        if x>1000 or y>700:
            if y/x>0.7:
                self.image=cv2.resize(self.image, (int(round(x*700/y)), 700))
            else:
                self.image=cv2.resize(self.image, (1000, int(round(y*1000/x))))
        self.curImage=np.copy(self.image)
        #print self.image.

    def showImage(self,dic=None):
        #print self.image[0][0][1]
        if type(dic) == dict:
            for wname in dic:
                #cv2.namedWindow(wname,1)
                if hasattr(self, dic[wname]):
                    cv2.imshow(wname,getattr(self, dic[wname]))
            cv2.waitKey(0)
        else:
            #cv2.namedWindow(self.winname,1)
            cv2.imshow(self.winname,self.curImage)
            cv2.waitKey(0)
    @timeit
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

    @timeit
    def test(self):
        #P.dump(self.image,file('test','w'))
        #print self.curImage.__len__()
        #x=[[[12,12,12],[12,12,12]],[[12,12,12],[12,12,12]]]
        #print type(x),np.ndarray(1)
        #cv2.creatImage([[[123,123,123]]])
        #for x in range(1,10):
            #print x
        #x=9
        #self.curImage=cv2.blur(self.image, (x,x))
        #self.curImage=cv2.medianBlur(self.image, x)
        #a,self.curImage=cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)
        self.curImage=cv2.cvtColor(self.image, 6)
        a,self.curImage=cv2.threshold(self.curImage, 180, 255, cv2.THRESH_BINARY)
        self.image2=cv2.cvtColor(self.image, 7)
        a,self.image2=cv2.threshold(self.image2, 180, 255, cv2.THRESH_BINARY)

test=cvTest('test.jpg')
#test.showImage()
#test.plus=timeit(test.plus)
#test.plus()
test.test()
test.showImage({
    u'原图'.encode('gbk'):'image',
    u'变换1'.encode('gbk'):'curImage',
    u'变换2'.encode('gbk'):'image2'
    })
#test.test()
#test.showImage()
#print type(test.image)