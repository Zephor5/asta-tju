#coding=utf-8
import wx,cv2
#from os import sep as PS

import commonUITools as _ct
import dataprocess as _dp

class WorkFrame(wx.Frame):
	"""
	"""
	def __init__(self, parent, info, id=-1, title='working', position=(-1,-1), size=(-1,-1)):
		super(self.__class__, self).__init__(parent, id, title, position, size)
		self.SetIcon(parent.icon)
		self.Center()

		self._image=info['image']
		self._image_path=info['path']

		self.initStatusBar()

		self.menuBar=_ct.MyMenu(self, self.menuData(), 'menubar', 12)
		self.SetMenuBar(self.menuBar.get())
		self.initBind()

		self.Show()
		#cv2.imshow(ip[ip.rindex(PS)+1:ip.rindex('.')], self._image)

	def initStatusBar(self):
		self.statusBar=self.CreateStatusBar()
		self.statusBar.SetFieldsCount(3)
		self.statusBar.SetStatusWidths([-2, -2, -1])

	def initBind(self):
		pass
		#self.Bind(wx.EVT_CLOSE, self.OnClose)

	def initBuffer(self):
		sz=self.GetClientSize()
		self.buffer = wx.EmptyBitmap(sz.x, sz.y)
		dc=wx.BufferedDC(None, self.buffer)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()

	def menuData(self): #2 菜单数据
		return [(u"文件", (
					(u"&新建\tCtrl+N", u"新建空白图像", self.OnNew),
					(u"&打开\tCtrl+O", u"选择图像", self.OnOpen),
					(u"保存\tCtrl+S", u"保存文件", self.OnSave),
					(u"另存为\tCtrl+Alt+S", u"另存为...", self.OnSaveas),
					#("theme", (
						#("white", "", self.OnColor, wx.ITEM_RADIO),
						#("red", "", self.OnColor, wx.ITEM_RADIO),
						#("green", "", self.OnColor, wx.ITEM_RADIO),
						#("yellow", "", self.OnColor, wx.ITEM_RADIO))),
					("Print", u"打印", self.OnPrint),
					("Quit\tCtrl+Q", u"退出", self.OnQuit))),
				 (u"视图",(
				 	("blank", u"暂空缺", self.test),
				 	('test', '', self.test))),
				 (u"测量",(
				 	(u"预处理", u"预处理照片", self.pre_processing),
				 	(u"模糊识别", u"模糊识别信息", self.fuzzy_recognition),
				 	(u"坐标系建立",(
				 		(u"建立照片坐标系", u"something for tip", self.pic_coordinate_system_build),
				 		(u"建立现实坐标系", u"something for tip", self.real_coordinate_system_build))),
				 	(u"数据还原", u"前面步骤必须已经完成", self.data_restoration)))]

	def OnChangeImg(self, info):
		if self._image_path != info['path']:
			if self.status_check():
				self._image_path=info['path']
				self._image=info['image']
				self.initBuffer()
			else:
				pass

	def status_check(self):
		pass
		return True

	def pre_processing(self, e=None):
		img=_dp.cvtImObject(self._image)
		cv2.imshow('cv2_show', img)

	def fuzzy_recognition(self, e=None):
		img=cv2.imread(self._image_path)
		self._image=_dp.cvtImObject(img)
		self.initBuffer()
		#print type(img)
		#cv2.imshow('cv2_show1', img)

	def pic_coordinate_system_build(self, e=None):
		pass

	def real_coordinate_system_build(self, e=None):
		pass

	def data_restoration(self, e=None):
		pass

	def OnNew(self, e):
		pass

	def OnOpen(self, e):
		pass

	def OnSave(self, e):
		pass

	def OnSaveas(self, e):
		pass

	def OnPrint(self, e):
		pass

	def OnQuit(self, e):
		pass

	def test(self, e):
		pass