#coding=utf-8
import wx,os
from os import sep as PS
import wx.animate as _A
from wx.lib.agw.advancedsplash import AdvancedSplash

import conf

_Title=conf._Title
mainC=conf.MC()

Iround=lambda x,d=0:int(round(x,d))

def getFileName(path):
	if os.path.isfile(path):
		return path[path.rindex(PS)+1:]
	return ''

def ShowTip(parent, message, title=u'提示', style=wx.OK|wx.CENTRE):
	tip=wx.MessageDialog(parent, message, title, style)
	tip.ShowModal()
	tip.Destroy()

def frameFadeOut(frame):
	#print T.clock()-startT,'30'
	#if sumt<256:
		#sumt=256
	#per=Iround(sumt/256)
	#per=round(per/1000,3)
	#print per,'per'
	"""for i in xrange(0,255):
		frame.SetTransparent(255-i)
		#if i != 255:
			##print T.clock()-startT,'40'
		T.sleep(0.001)
			##print T.clock()-startT,'42'
	#print T.clock()-startT,'43'
	frame.Destroy()"""
	def OnTimer(e):
		if frame._timern < 236:
			frame._timern+=20
			#print frame._timern
			frame.SetTransparent(255-frame._timern)
		else:
			frame._timer.Stop()
			del frame._timer
			frame.Destroy()
	frame._timer=wx.Timer(frame, -1)
	frame._timern=0
	frame.Bind(wx.EVT_TIMER, OnTimer, frame._timer)
	frame._timer.Start(30)

class MySplashFrame(AdvancedSplash):
	"""docstring for MySplashFrame"""
	def __init__(self, app, bmp, size, timeout):
		super(self.__class__, self).__init__(None, -1, (-1,-1), size, 32786, bmp, timeout)
		self.app=app
		self.Bind(wx.EVT_CLOSE, self.OnClose)

	def OnClose(self, e=None):
		self.Enable(False)
		if hasattr(self, '_splashtimer'):
			self._splashtimer.Stop()
		if hasattr(self.app, 'mFrame'):
			del self._splashtimer
			self.app.mFrame.Show()
			frameFadeOut(self)
		else:
			self._splashtimer.Start(100)

class WaitingFrame(wx.MiniFrame):
	"""docstring for WaitingFrame"""
	def __init__(self, control):
		super(self.__class__, self).__init__(wx.GetApp().mFrame, size=mainC.waitingFrameSize, style=wx.NO_BORDER|wx.STAY_ON_TOP)
		self.Center()
		#self.SetTransparent(150)
		self.SetBackgroundColour('white')
		ani = _A.Animation(mainC.waitingIm)
		ctrl = _A.AnimationCtrl(self, -1, ani)
		#ctrl.SetBackgroundColour('gray')
		ctrl.Play()
		wx.StaticText(self, -1, 'please waiting ...', (80, 30), (100,80), wx.ALIGN_CENTER)
		self.Show(True)
		control.Enable(False)
		self.ct=control

	def Hide(self):
		self.ct.Enable(True)
		frameFadeOut(self)
		

class MyMenu(object):
	"""docstring for MyPopupMenu"""
	def __init__(self, parent, menuData, type, fontSize=9):
		super(self.__class__, self).__init__()
		self.parent=parent
		if type == 'menubar':
			self.__obj=self.createMenuBar(menuData)
		elif type == 'popupMenu':
			self.__obj = self.createMenu(menuData)
		else:
			self.__obj = wx.MenuBar()
		if hasattr(self.__obj, 'SetFont'):
			self.__obj.SetFont(wx.Font(fontSize, wx.FONTFAMILY_MAX, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

	def __repr__(self):
		return 'self.__obj'

	def __str__(self):
		return str(self.__obj)

	def __getattr__(self, attr):
		return getattr(self.__obj, attr)

	def get(self):
		return self.__obj

	def createMenuBar(self, menuData):
		menuBar=wx.MenuBar()
		for menu in menuData:
			menuBar.Append(self.createMenu(menu[1]), menu[0])
		return menuBar

	def createMenu(self, menuData):
		menu = wx.Menu()
		for eachItem in menuData:
			if len(eachItem) == 2:
				label = eachItem[0]
				subMenu = self.createMenu(eachItem[1])
				menu.AppendMenu(wx.NewId(), label, subMenu)
			else:
				self.createMenuItem(menu, *eachItem)
		return menu

	def createMenuItem(self, menu, label, status, handler, id=-1, kind=wx.ITEM_NORMAL, enable=True):
		if not label:
			menu.AppendSeparator()
			return
		menuItem = menu.Append(id, label, status, kind)
		self.parent.Bind(wx.EVT_MENU, handler, menuItem)
		if not enable:
			menu.Enable(id, False)

class MyToolTip(wx.ToolTip, wx.EvtHandler):			#unused
	"""docstring for MyToolTip"""
	def __init__(self, text=''):
		wx.ToolTip.__init__(self, text)
		wx.EvtHandler.__init__(self)
		