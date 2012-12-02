#coding=utf-8
import wx

import commonUITools as _ct

class WorkFrame(wx.Frame):
	"""
	"""
	def __init__(self, parent, img, id=-1, title='working', position=(-1,-1), size=(-1,-1)):
		super(self.__class__, self).__init__(parent, id, title, position, size)
		self.SetIcon(parent.icon)
		self.Center()

		self._image=img

		self.initStatusBar()

		self.menuBar=_ct.MyMenu(self, self.menuData(), 'menubar', 12)
		self.SetMenuBar(self.menuBar.get())
		self.initBind()

		self.Show()

	def initStatusBar(self):
		self.statusBar=self.CreateStatusBar()
		self.statusBar.SetFieldsCount(3)
		self.statusBar.SetStatusWidths([-2, -2, -1])

	def initBind(self):
		pass
		#self.Bind(wx.EVT_CLOSE, self.OnClose)

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
				 	('test', '', self.test)))]

	def OnChangeImg(self, img):
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