#coding=utf-8
#start at 2012-10-19
from __future__ import division		#this must be put at the beginning
import wx,os,threading as TD#,time as T
from os import sep as PS
#import wx.animate as _A
from wx.lib.agw.multidirdialog import MultiDirDialog

import commonUITools as _ct
from workspace import WorkFrame

#_ScrollBarWidth=18
_WaitingHandler=None
_UI_BLANK=0
_UI_SELECTED=1
_UI_HOVER=2
#try:
#_ct.mainC=conf.MC()
#except Exception, e:
#	print 'conf set error',e
#	exit()

class ImContainer(wx.Window):
	"""docstring for ImContainer"""
	def __init__(self, parent, label='', path=_ct.mainC.blankIm, _ui_status=_UI_BLANK, id=-1, pos=wx.DefaultPosition, size=_ct.mainC.imConSize):
		super(self.__class__, self).__init__(parent, id, pos, size, wx.TAB_TRAVERSAL | wx.NO_BORDER, label)
		self.SetBackgroundColour('#FFFFFFFF')
		#print self.SetTransparent(50)
		self.imPath=path
		self.doSize=1
		self._ui_status=_ui_status
		self.pen=wx.Pen(wx.Colour(35, 142,  35, 160))
		self.hoverBrush=wx.Brush(wx.Colour(35, 142, 35, 20))
		self.selBrush=wx.Brush(wx.Colour(35, 142, 35, 50))
		#self._readyToPaint=False

		#self._threadCondition=TD.Condition()
		self.initBitmap()
		self.initBuffer()
		#self.initText()
		#self.nameText.SetInsertionPoint(0)

		self.initToolTip()
		#self.toolTip.Bind(wx.EVT_LEFT_UP, self.test)
		#self.toolTip.Bind(wx.EVT_RIGHT_UP, self.UnSel)
		#self.toolTip.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_IDLE, self.OnIdle)
		self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
		self.Bind(wx.EVT_LEFT_UP, self.OnSel)
		self.Bind(wx.EVT_RIGHT_UP, self.UnSel)
		self.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)
		#self.Bind(wx.EVT_CLOSE, self.onClose)

	def initText(self):			#已经被替代
		sz=self.GetSize()
		#print _ct.Iround(sz.x*0.15)
		if hasattr(self, 'nameText'):
			del self.nameText
		else:
			nt=self.nameText=wx.StaticText(self, -1, _ct.getFileName(self.imPath), (_ct.Iround(sz.x*0.15), sz.y-45), (sz.x,30), wx.ALIGN_CENTER)
			nt.Wrap(_ct.Iround(sz.x*0.7))

	def initBitmap(self, image_changed=0):
		#print image_changed
		#if self._threadCondition.acquire():
		sz=self.GetSize()
		self.impos=[4,4]
		'''if image_changed and hasattr(self, 'gifC'):
			#print 'del'
			self.gifC.Stop()
			self.gifC.Destroy()
			del self.gifC
		if self.imPath.split('.')[-1].lower() == 'gif':
			if hasattr(self, 'gifC'):
				return
			if hasattr(self, 'pic'):
				self.Refresh(0)
				del self.pic
			gif=_A.Animation(self.imPath)
			self.gifC=_A.AnimationCtrl(self, -1, gif, (self.impos[0], self.impos[1]))
			self.gifC.Play()
			#wx.Yield()
			return'''
		if hasattr(self,'image') and not image_changed:
			im = self.image.Copy()
		else:
			self.image=wx.Image(self.imPath)
			im = self.image.Copy()
		x,y=im.GetSize()
		if x/y > sz.x/(sz.y-30):
			y=_ct.Iround(y*(sz.x-8)/x)
			im.Rescale(sz.x-8, y)
			self.impos[1]=_ct.Iround(abs(sz.y-38-y)/2)
		else:
			x=_ct.Iround(x*(sz.y-38)/y)
			im.Rescale(x, sz.y-38)
			self.impos[0]=_ct.Iround(abs(sz.x-x)/2)
		self.pic=im.ConvertToBitmap()
		self.GetParent().GetParent().Enable(True)
		self.reInitBuffer=1
		#self.ProcessEvent(wx.PyCommandEvent(wx.EVT_IDLE.typeId, self.GetId()))
		#self.initBuffer()
		#self._readyToPaint=True
		#self.AddPendingEvent(wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
		#self._threadCondition.release()

	def InitBitmap(self, *args):
		#print 'test'
		if not hasattr(self,'_readThread') or not self._readThread.isAlive():
			self.GetParent().GetParent().Enable(False)
			self._readThread=TD.Thread(target=self.InitBitmap, name='InitBitmap', args=args)
			self._readThread.start()
		elif self._readThread.isAlive():
			pass
			#self._readThread.join()
			#self.initBitmap(args)

	def initBuffer(self, brush='sel'):
		#print 't'
		sz=self.GetSize()
		self.buffer = wx.EmptyBitmap(sz.x, sz.y)
		dc=wx.BufferedDC(None, self.buffer)
		dc=wx.GCDC(dc)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		if self._ui_status == _UI_SELECTED or brush=='hover' and self.HitTest(wx.GetMousePosition()-self.GetScreenPosition())==wx.HT_WINDOW_INSIDE:
			dc.SetPen(self.pen)
			dc.SetBrush(getattr(self, brush+'Brush'))
			dc.DrawRoundedRectangleRect(wx.Rect(0,0,sz.x,sz.y), 5)
		if hasattr(self,'pic'):
			dc.DrawBitmap(self.pic, self.impos[0], self.impos[1], True)
		#dc.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		if self.imPath != _ct.mainC.blankIm:
			name=_ct.getFileName(self.imPath)
			tn=_ct.Iround((sz.x-100)/6)+1
			name=name if len(name)<tn else name[:tn-1]+'...'
			#namepos=[_ct.Iround(sz.x*0.15)]
			dc.DrawText(name, _ct.Iround((sz.x-6*len(name))/2), sz.y-26)
		self.reInitBuffer = 0

	def initToolTip(self):
		name=_ct.getFileName(self.imPath)
		x,y=self.image.GetSize()
		tip=name+"\n"+str(x)+u'×'+str(y)+u'像素'
		if hasattr(self, 'toolTip'):
			self.toolTip.SetTip(tip)
		else:
			self.toolTip=wx.ToolTip(tip)
			self.SetToolTip(self.toolTip)

	def OnPaint(self, e):
		#print 'paint',self.GetLabel(),self.GetPosition()
		#if hasattr(self, 'buffer'):
		wx.BufferedPaintDC(self, self.buffer)

	def OnSize(self, e):
		self.reInitBuffer = 1
		if self.doSize:
			#self.initText()
			self.initBitmap()
		#print 'size'
		#self.initBuffer()
		#self.Refresh(0)
		#e.Skip()

	def OnIdle(self, e):
		if self.reInitBuffer and self.doSize:
			#print 'OnIdle'
			self.initBuffer()
			self.Refresh(0)

		#if self.image.GetSize()

	def OnEnter(self, e):
		self.paintSel()
		"""if not hasattr(self, 'toolTip'):
			self.toolTip=wx.TipWindow(self, 'sometest')"""

	def OnLeave(self, e):
		"""if hasattr(self, 'toolTip'):
			self.toolTip.Destroy()
			del self.toolTip"""
		if self.HitTest(wx.GetMousePosition()-self.GetScreenPosition()) == wx.HT_WINDOW_INSIDE:
			return
		if self._ui_status != _UI_SELECTED:
			self._ui_status=_UI_BLANK
			self.paintSel('leave')

	def OnSel(self, e=None):
		self.paintSel('selected')

	def UnSel(self, e=None):
		if self._ui_status == _UI_SELECTED:
			self._ui_status = _UI_HOVER
			self.initBuffer('hover')
			self.Refresh(0)
			#wx.BufferedPaintDC(self, self.buffer)
			#T.sleep(0.1)
			#self.paintSel()

	def paintSel(self, case='hover'):
		#dc.Clear()
		if case == 'hover' and self._ui_status == _UI_BLANK:
			self._ui_status=_UI_HOVER
			"""sz=self.GetSize()
			dc=wx.GCDC(wx.ClientDC(self))
			dc.SetPen(self.pen)
			dc.SetBrush(self.hoverBrush)
			dc.DrawRoundedRectangleRect(wx.Rect(0,0,sz.x,sz.y), 5)
			if hasattr(self,'pic'):
				dc.DrawBitmap(self.pic, self.impos[0], self.impos[1], True)"""
			self.initBuffer('hover')
			self.Refresh(0)
		elif case == 'selected' and self._ui_status != _UI_SELECTED:
			self._ui_status=_UI_SELECTED
			self.initBuffer()
			self.Refresh(0)
		elif case == 'leave':
			self.initBuffer()
			self.Refresh(0)

	def OnDClick(self, e):
		app=wx.GetApp()
		if hasattr(app, 'workSpace') and app.workSpace:
			app.workSpace.OnChangeImg(self.image)
		else:
			app.workSpace=WorkFrame(app.mFrame, self.image)

	def Destroy(self):
		#pass
		#print 'close'
		"""if hasattr(self, '_readThread') :#and self._readThread.isAlive():
			self._readThread.join(0)"""
		super(self.__class__, self).Destroy()

	def drawImName(self, dc, name, sz, minBorder=30):			#useless
		pass

	def SetImPath(self, path, _ui_status=_UI_BLANK):
		if path != self.imPath:
			if os.path.isfile(path):
				self.imPath=path
				self._ui_status=_ui_status
				self.initBitmap(1)
				self.initBuffer()
				self.initToolTip()
				self.Refresh()
		elif _ui_status == _UI_SELECTED and self._ui_status != _UI_SELECTED:
			self.OnSel()
		elif self._ui_status == _UI_SELECTED:
			self.UnSel()

	def test(self, e):
		pass
		#print 'test'
		

class MyImWindow(wx.Panel):
	"""docstring for MyImWindow"""
	def __init__(self, parent, paths, sel='', size=(-1,-1)):
		super(self.__class__, self).__init__(parent, size=size)
		self.SetBackgroundColour('white')
		self.paths=paths if paths else [_ct.mainC.blankIm]
		#print 'client size',parent.GetClientSize()
		self.parent=parent
		self.sel=sel
		self.size=self.GetSize()
		l=len(paths)
		r,c = self.sortRC(l)
		self.SetSizer(wx.GridSizer(r, c, 20, 20))
		#print self.size
		#self.scrollBar=wx.ScrollBar(self, -1, (-1,-1), (-1,-1), wx.SB_VERTICAL)
		self.Init()
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_MOUSEWHEEL, self.OnScroll)

	def sortRC(self, l):
			if l <= 1:
				r,c=1,1
			elif l == 2:
				r,c=2,1
			elif 2< l <5:
				r,c=2,2
			else:
				r,c=3,3
			return (r,c)

	def Init(self):
		global _WaitingHandler
		#print 'init'
		ss= self.Sizer
		sps=self.paths
		pn=len(sps)
		sn=len(ss.GetChildren())
		sel=self.sel
		#print hasattr(__main__, 'app')
		#print 'app' in globals().keys()
		if 'app' in globals().keys() and not _WaitingHandler:
			_WaitingHandler=_ct.WaitingFrame(self.parent)
			#DT.Thread(target=_ct.WaitingFrame, args=(self.parent,)).start()
			wx.Yield()
		if sel and pn>9 and sel in sps:
			index=sps.index(sel)
			start=index if pn-index>8 else pn-9
		else:
			start=0

		if pn<sn:
			for n in xrange(pn,sn):
				label='cpic_'+str(n)
				cWin=self.FindWindowByLabel(label)
				ss.Remove(cWin)
				cWin.Destroy()

		if not pn:
			sps=[_ct.mainC.blankIm]
		for i,n in enumerate(xrange(start,start+9 if pn>8 else pn if pn else 1)):
			label='cpic_'+str(i)
			#print label
			cWin=self.FindWindowByLabel(label)
			if not cWin:
				cWin=ImContainer(self, label, sps[n], sps[n]==self.sel)
				ss.Add(cWin, 1, wx.EXPAND)
			else:
				cWin.SetImPath(sps[n])

		l = len(ss.GetChildren())
		r,c=self.sortRC(l)
		ss.SetRows(r)
		ss.SetCols(c)
		self.AddPendingEvent(wx.PyCommandEvent(wx.EVT_SIZE.typeId, self.GetId()))
		if _WaitingHandler:
			_WaitingHandler.Hide()
		#self.Refresh(0)
		#self.Update()
		#print ss.GetRows(),ss.GetCols()

	def initScrollBar(self):			#暂时没用
		sb=self.scrollBar
		#print self.size
		sb.SetPosition(0)
		#sb.SetSize(wx.Size(_ScrollBarWidth, self.size.y))

	def onPaint(self, e):		#暂时没用
		#print 'paint'
		#dc=wx.PaintDC(self)
		#dc.Clear()
		e.Skip()

	def OnSize(self, e):
		#self.size=e.GetSize()
		#print 'size'
		self.size=self.GetSize()
		#self.Refresh()
		e.Skip()

	def OnScroll(self, e):
		pass
		#for i in dir(e):
			#print i
		#print e.GetWheelRotation()

	def SetPaths(self, paths, sel=''):
		if self.paths != paths:
			self.paths=paths
			if sel in paths:
				self.sel=sel
			self.Init()
			#self.Refresh()

	def SetListSel(self, sel=''):
		if sel in self.paths:
			self.sel=sel
			self.Init()

	def test(self, e):			#测试用
		"""global _WaitingHandler
		if _WaitingHandler:
			_WaitingHandler.Hide()
		else:
			_WaitingHandler=_ct.WaitingFrame(self.parent)"""
		#ss=self.Sizer
		#ss.Add(ImContainer(self, 'label', self.paths[0]))
		#self.Init()
		#print e.GetEventHandler()
		#print len(ss.GetChildren())
		for c in self.Sizer.GetChildren():
			print c.GetWindow()._readThread.isAlive()


class MainWindow(wx.SplitterWindow):
	"""docstring for MainWindow"""
	def __init__(self, parent):
		super(self.__class__, self).__init__(parent, style=wx.SP_LIVE_UPDATE)
		self.IG_PREVENT_SIZE=0
		#self.SetSashSize(0)
		self.SetSize(parent.GetClientSize())
		self.initSash()
		#print parent.GetClientSize()
		fl=self.folderList=wx.TreeCtrl(self)
		fl.SetWindowStyle(wx.TR_HIDE_ROOT)
		fl.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		#print T.clock()-startT,'92'
		self.initFolderList()
		#print T.clock()-startT,'94'
		sel=fl.GetFirstVisibleItem()
		self.preItem=self.ItemGetPath(sel)
		fl.Expand(sel)
		size=self.GetSize()
		ig=self.imageGlimpse=MyImWindow(self, self.ItemGetListPaths(sel), '', (size.x-self.sashPos, size.y))
		#ig.SetBackgroundColour('gray')
		self.SplitVertically(fl, ig, self.sashPos)

		self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnSashChanging)
		self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged)
		self.Bind(wx.EVT_SPLITTER_DCLICK, None)
		self.Bind(wx.EVT_SIZE, self.onSize)
		self.Bind(wx.EVT_PAINT, self.onPaint)
		#fl.Bind(wx.EVT_LEFT_DCLICK, self.OnHideFL)
		#fl.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
		#fl.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
		fl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
		fl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
		fl.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnTreeRightClick)

	def onPaint(self, e):
		#print 'test'
		wx.PaintDC(self)
		#self.PrepareDC(dc)
		#self.DrawShapes(dc)
		#e.Skip()

	def initSash(self):
		self.sashPos=_ct.Iround(self.GetParent().GetClientSize().x*0.27) if _ct.mainC.sashPos==0 else _ct.mainC.sashPos
		if self.sashPos>_ct.mainC.maxSashPos:
			self.sashPos=_ct.mainC.maxSashPos
		if self.sashPos<0:
			self.resSashPos=-self.sashPos
			self.sashPos=1
		if self.sashPos<10:
			self.SetMinimumPaneSize(0)
			self.SetSashSize(0)
		else:
			self.SetMinimumPaneSize(100)
		self.SetSashPosition(self.sashPos)

	def initFolderList(self, old=None):
		global _WaitingHandler
		mF=_ct.mainC.listFolder
		fl=self.folderList
		changes=[[],[]]
		if old is None:
			pass
		elif not old:
			fl.DeleteAllItems()
		elif mF and mF !=['']:
			for x in mF:
				if x not in old:
					changes[0].append(x)
			for x in old:
				if x not in mF:
					changes[1].append(x)
		if not mF or mF == ['']:
			fl.DeleteAllItems()
			root=fl.AddRoot("None")
			self.AddTreeNodes(root, [u'未选择文件夹'])
			fl.SelectItem(fl.GetFirstVisibleItem())
			return
		root=fl.GetRootItem()
		if not root:
			root = fl.AddRoot("picFolders")
		trees=[]
		if not changes[0] and not changes[1]:
			for p in mF:
				list_data=self.formFolderList(p)
				if list_data:
					trees.append(list_data)
		else:
			for p in changes[1]:
				item=self.GetItemByText(p)
				if item:
					fl.Delete(item)
			for p in changes[0]:
				list_data=self.formFolderList(p)
				if list_data:
					trees.append(list_data)
		if trees:
			self.AddTreeNodes(root, trees)
			if old == []:
				fl.SelectItem(fl.GetLastChild(root))
			elif old:
				fl.SelectItem(self.GetItemByText(changes[0][0]))
		fl.popupFolderMenu = _ct.MyMenu(fl, self.MenuData('folder'), 'popupMenu').get()
		fl.popupFileMenu = _ct.MyMenu(fl, self.MenuData('file'), 'popupMenu').get()
		if _WaitingHandler:
			_WaitingHandler.Hide()

	def MenuData(self, t):
		if t == 'folder':
			return [("ShowList", u"显示左侧文件夹列表", None),
					(u'移除', '', self.DelListFolder, 102)]
		elif t == 'file':
			return [("test", u"哈哈", None)]
		else:
			return []

	def AddTreeNodes(self, parentItem, items):
		"""
		Recursively traverses the data structure, adding tree nodes to
		match it.
		"""
		for item in items:
			rt=isinstance(item, (str, unicode))
			if rt:
				self.folderList.AppendItem(parentItem, item)
			else:
				if len(item)>1:
					newItem = self.folderList.AppendItem(parentItem, item[0])
					self.AddTreeNodes(newItem, item[1])
				else:
					if rt:
						self.folderList.AppendItem(parentItem, item)
					else:
						self.AddTreeNodes(parentItem, item)

	def formFolderList(self, path=''):
		"""
		给定路径，以配置里图片文件后缀list为依据，过滤并形成对应特定文件及文件夹list，方便后面使用
		"""
		#lis=os.listdir(path)
		tr=os.walk(path)
		data=[]
		imtype=_ct.mainC.imTypes
		def Lindex(l,i):
			if i in l:
				return l.index(i)
			else:
				for x in xrange(0,len(l)):
					if type(l[x])==list:
						if i==l[x][0]:
							return x
			return -1
		for x in tr:
			if not x:
				continue
			ltemp=x[2][:]
			for f in ltemp:
				if f.split('.')[-1].lower() not in imtype:
					x[2].remove(f)
			x[1].extend(x[2])
			x=[x[0],x[1]]
			if not x[1]:
				continue
			if not data:
				data=list(x)
			else:
				pos=[path]+x[0][len(path)+1:].split(PS)
				posStr='data[1]'
				indexs=[]
				for j in xrange(1,len(pos)):
					posStr='data[1]'
					if not indexs:
						indexs.append(Lindex(data[1],pos[1]))
					else:
						for p in indexs:
							posStr+='['+str(p)+'][1]'
						posStr='Lindex('+posStr+',pos['+str(j)+'])'
						try:
							indexs.append(eval(posStr))
						except Exception:
							raise Exception('filelist error')
				posStr='data[1]'
				for n,p in enumerate(indexs):
					if n==len(indexs)-1:
						posStr+='['+str(p)+']'
					else:
						posStr+='['+str(p)+'][1]'
				posStr+='=x'
				x[0]=pos[-1]
				try:
					exec posStr in globals(),locals()
				except Exception:
					raise Exception('filelist error')
		if not data:
			old=_ct.mainC.listFolder[:]
			_ct.mainC.delListFolder([path])
			self.initFolderList(old)
		else:
			return data

	def GetItemByText(self, text=''):
		"""
		通过list的字符串，查找对应的item对象
		"""
		fl=self.folderList
		if text:
			child,cookie=fl.GetFirstChild(fl.GetRootItem())
			while fl.GetItemText(child) != text:
				child=fl.GetNextSibling(child)
				if not child:
					break
			if child and fl.GetItemText(child) == text:
				return child
		return None

	def ItemGetListPaths(self, item):
		"""
		通过选中的item对象，若选中文件夹，返回该文件夹下所有文件（不包括子目录）；若选中的是文件，则返回该文件所在目录的所有文件的绝对路径（不包括子目录）
		"""
		fl=self.folderList
		paths=[]
		if os.path.isfile(self.ItemGetPath(item)):
			item=fl.GetItemParent(item)
		child,cookie=fl.GetFirstChild(item)
		while child:
			path=self.ItemGetPath(child)
			if os.path.isfile(path):
				paths.append(path)
			child=fl.GetNextSibling(child)
		return paths

	def ItemGetPath(self, item):
		"""
		通过item对象返回该对象对应的绝对路径，若计算结果不是系统文件夹或文件路径则返回空字符
		"""
		path=''
		fl=self.folderList
		path=fl.GetItemText(item)
		curItem=item
		while fl.GetItemParent(curItem) != fl.GetRootItem():
			curItem=fl.GetItemParent(curItem)
			path=fl.GetItemText(curItem)+PS+path
		if os.path.isdir(path) or os.path.isfile(path):
			return path
		else:
			return ''

	def DelListFolder(self, e):
		fl=self.folderList
		old=_ct.mainC.listFolder[:]
		_ct.mainC.delListFolder([fl.GetItemText(fl.GetSelection())])
		self.initFolderList(old)

	def OnSelChanged(self, e=None):
		#fl=self.folderList
		item=e.GetItem()
		try:
			pre=self.preItem
			path=self.ItemGetPath(item)
			cItem=os.path.dirname(path) if os.path.isfile(path) else path
			pItem=os.path.dirname(pre) if os.path.isfile(pre) else pre
			#print pItem,cItem
			if pItem != cItem:
				self.preItem=cItem
				self.imageGlimpse.SetPaths(self.ItemGetListPaths(item), path)
			else:
				self.imageGlimpse.SetListSel(path)
		except:
			raise
		else:
			self.initStatus()
			
	def initStatus(self):
		fl=self.folderList
		item=fl.GetSelection()
		path=self.ItemGetPath(item)
		i=0 	#选中文件索引
		f=0 	#文件夹数
		n=0 	#文件及文件夹总数
		if os.path.isfile(path):
			cItem=os.path.dirname(path)
			n=fl.GetChildrenCount(fl.GetItemParent(item), False)
			while item and not fl.GetChildrenCount(item, False):
				item=fl.GetPrevSibling(item)
				i+=1
			while item and fl.GetChildrenCount(item, False):
				item=fl.GetPrevSibling(item)
				f+=1
		else:
			cItem=path
			n=fl.GetChildrenCount(item, False)
			item=fl.GetFirstChild(item)[0]
			while item and fl.GetChildrenCount(item, False):
				item=fl.GetNextSibling(item)
				f+=1
		cItem=cItem if len(cItem)<30 else cItem[:27]+'...'

		statusText0=u'目录：'+cItem
		statusText1=''
		statusText2=''
		if i:
			statusText1+=u'图片：'+str(n)+u'张   选中第'+str(i)+u'张'
			if f:
				statusText2+=str(f)+u'个子目录'
		else:
			if n:
				if n-f:
					statusText1+=u'图片：'+str(n-f)+u"张"
				if f:
					statusText2+=str(f)+u'个子目录'
			else:
				statusText1+=u'目录木有要找的东东'
		sb=self.GetParent().statusBar
		sb.SetStatusText(statusText0, 0)
		sb.SetStatusText(statusText1, 1)
		sb.SetStatusText(statusText2, 2)

	def OnActivated(self, e):
		pass

	def OnToggleFL(self, e=None):
		if self.sashPos<10 and not hasattr(self, 'resSashPos'):
			self.resSashPos=_ct.Iround(self.GetParent().GetClientSize().x*0.27)
		else:
			if self.sashPos>10:
				self.resSashPos=self.sashPos
		#fl=self.folderList
		self.ig_prevent_size()
		"""if self.GetSashPosition()>9:
			self.SetMinimumPaneSize(0)
			t=_ct.Iround(500/sp)
			if t<1:
				t=1
			for x in xrange(0,sp-1):
				self.SetSashPosition(sp-x-1)
				if x != sp-2:
					self.imageGlimpse.Update()
					T.sleep(t/1000)
					#if x == sp-2:
						#fl.Hide()
			#self.imageGlimpse.Refresh()
			#self.Refresh()
			#self.Initialize(self.imageGlimpse)
			self.SetSashSize(0)

		else:
			#self.SplitVertically(fl, self.imageGlimpse, 1)
			#fl.Show()
			self.SetSashSize(3)
			t=_ct.Iround(400/sp)
			for x in xrange(2,sp+1):
				self.SetSashPosition(x)
				self.imageGlimpse.Update()
				if x!=sp:
					T.sleep(t/1000)
			self.SetMinimumPaneSize(100)"""
		def _toggleSash(e):
			_sashPos=self.GetSashPosition()
			#print self.resSashPos
			if self._toggleStatus:
				if _sashPos < self.resSashPos-1:
					self.SetSashPosition(_sashPos+2)
					self.imageGlimpse.Update()
				else:
					if _sashPos != self.resSashPos:
						_sashPos=self.resSashPos
						self.SetSashPosition(_sashPos)
						self.imageGlimpse.Update()
					self.SetMinimumPaneSize(100)
			else:
				if _sashPos > 2:
					self.SetSashPosition(_sashPos-2)
					self.imageGlimpse.Update()
				else:
					if _sashPos != 1:
						_sashPos=1
						self.SetSashPosition(1)
						self.imageGlimpse.Update()
			if (self._toggleStatus and _sashPos == self.resSashPos) or (not self._toggleStatus and _sashPos == 1):
				self._toggleTimer.Stop()
				del self._toggleTimer
				self.sashPos=_sashPos
				#print self.sashPos
				if _sashPos<10:
					_ct.mainC.setSashPos(-self.resSashPos)
				else:
					_ct.mainC.setSashPos(_sashPos)
				self.ig_prevent_size(False)

		self._toggleTimer=wx.Timer(self, -1)
		if self.GetSashPosition()>9:
			self._toggleStatus=False 		#表示收起list
			self.SetMinimumPaneSize(1)
			self.SetSashSize(0)
		else:
			self._toggleStatus=True 		#表示展开list
			self.SetSashSize(3)
		self.Bind(wx.EVT_TIMER, _toggleSash, self._toggleTimer)
		self._toggleTimer.Start(2)
		#self.imageGlimpse.Update()

	def OnSashChanging(self, e):
		#self.sashPos=e.GetSashPosition()
		#self.SetSashPosition(self.sashPos)
		#self.Refresh()
		self.ig_prevent_size()
		#e.Skip()

	def OnSashChanged(self, e=None):
		#print 'test'
		#print self.imageGlimpse.Sizer.GetChildren()[0].GetWindow().doSize
		self.ig_prevent_size(False)
		self.sashPos=e.GetSashPosition()
		_ct.mainC.setSashPos(self.sashPos)

	def ig_prevent_size(self, t=True):
		ig_children=self.imageGlimpse.Sizer.GetChildren()
		if not t and self.IG_PREVENT_SIZE:
			for m in ig_children:
				m.GetWindow().doSize=1
				m.GetWindow().initBitmap()
			self.IG_PREVENT_SIZE=0
		else:
			for m in ig_children:
				m.GetWindow().doSize=0
			self.IG_PREVENT_SIZE=1

	def OnTreeRightClick(self, e):
		item=e.GetItem()
		pos=e.GetPoint()
		fl=self.folderList
		fl.SelectItem(item)
		selPath=self.ItemGetPath(item)
		if os.path.isfile(selPath):
			fl.PopupMenu(fl.popupFileMenu, pos)
		elif os.path.isdir(selPath):
			if fl.GetItemParent(item) == fl.GetRootItem():
				fl.popupFolderMenu.Enable(102, True)
			else:
				fl.popupFolderMenu.Enable(102, False)
			fl.PopupMenu(fl.popupFolderMenu, pos)

	def onSize(self, e):
		#size=self.GetSize()
		#print self.sashPos
		#self.imageGlimpse.SetSize((size.x-self.sashPos, size.y))
		e.Skip()

class MainFrame(wx.Frame):
	"""docstring for MainFrame"""
	def __init__(self, title,size):
		super(self.__class__, self).__init__(None,-1,title,(-1,-1),size)
		self.icon=wx.Icon(_ct.mainC.icon, wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)
		self.Center()
		#self.title = title
		#self.size = size
		#print T.clock()-startT,'271'
		self.window = MainWindow(self)
		#self.window.SetBackgroundColour('#')
		#self.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.initStatusBar()
		self.menuBar=_ct.MyMenu(self, self.menuData(), 'menubar', 12)
		self.SetMenuBar(self.menuBar.get())
		self.initBind()

	def menuData(self): #2 菜单数据
		return [(u"文件", (
					("&New\tCtrl+N", u"新建图像", self.OnNew),
					("&Folder\tCtrl+F", u"选择图像目录", self.OnOpen),
					("Save", u"保存文件", self.OnSave),
					("Save as", u"另存为...", self.OnSaveas),
					("theme", (
						("white", "", self.OnColor, wx.ITEM_RADIO),
						("red", "", self.OnColor, wx.ITEM_RADIO),
						("green", "", self.OnColor, wx.ITEM_RADIO),
						("yellow", "", self.OnColor, wx.ITEM_RADIO))),
					("Print", u"打印", self.OnPrint),
					("Quit\tCtrl+Q", u"退出", self.OnCloseWindow))),
				 (u"视图",(
				 	("ToggleList", u"显示/隐藏左侧文件夹列表", self.window.OnToggleFL, 2010),
				 	('test', '', self.window.imageGlimpse.test)))]

	def initBind(self):
		#self.window.Bind(wx.EVT_MOTION, self.OnWindowMotion)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_CLOSE, self.OnClose)

	def initStatusBar(self):
		self.statusBar=self.CreateStatusBar()
		self.statusBar.SetFieldsCount(3)
		self.statusBar.SetStatusWidths([-2, -2, -1])

	def setFolders(self, folders):
		global _WaitingHandler
		old=_ct.mainC.listFolder[:]
		_ct.mainC.addListFolder(folders)
		if _ct.mainC.listFolder != old:
			#app.waiting.Show()
			#print _WaitingHandler
			_WaitingHandler=_ct.WaitingFrame(self)
			wx.Yield()
			self.window.initFolderList(old)
		else:
			_ct.ShowTip(self, u'选择的文件重复或已包含，若要缩小文件夹范围请先删除已包含的父文件夹!', u'提示')

	def OnWindowMotion(self, e):
		self.statusBar.SetStatusText(str(e.GetPositionTuple()))

	def OnNew(self, e): pass
	def OnOpen(self, e):
		openD=MultiDirDialog(self, u'选择一个或多个文件夹', u'浏览文件夹', _ct.mainC.defaultPath)
		if openD.ShowModal() == wx.ID_OK:
			paths=openD.GetPaths()
			paths=filter(lambda item:item.find(PS)>-1,paths)
			if paths:
				self.setFolders(paths)
			else:
				_ct.ShowTip(self, u'文件夹暂不支持整个硬盘分区直接加入')
		openD.Destroy()

	def OnSave(self, e): pass
	def OnSaveas(self, e):
		pass
	def OnPrint(self, e):
		pass

	def OnColor(self, e):
		menubar = self.GetMenuBar()
		itemId = e.GetId()
		item = menubar.FindItemById(itemId)
		color =item.GetLabel()
		self.window.SetBackgroundColour(color)
		self.window.Refresh()

	def OnSize(self, e):
		#print 'OnSize'
		if not self.IsMaximized():
			_ct.mainC.setSize(self.GetSize())
		self.window.initSash()
		e.Skip()

	def OnClose(self, e):
		self.window.folderList.SelectItem(self.window.folderList.GetLastChild(self.window.folderList.GetRootItem()))	#消除关闭时，文件列表错误
		self.window.folderList.Destroy()
		e.Skip()

	def OnCloseWindow(self, e):
		self.Close()

class PicM(wx.App):
	"""docstring for PicManager"""
	def OnInit(self):
		bmp=wx.Image(_ct.mainC.blankIm, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		bmp.SetMask(wx.Mask(bmp))
		_ct.MySplashFrame(self, bmp, (bmp.GetWidth(),bmp.GetHeight()),_ct.mainC.welT)
		wx.Yield()
		#print T.clock()-startT,'344'
		self.mFrame=MainFrame(_ct._Title, _ct.mainC.size)
		#print T.clock()-startT,'346'
		self.SetTopWindow(self.mFrame)
		#self.waiting=_ct.WaitingFrame(self.mFrame)
		#self.waiting.Show()
		return True

if _ct.mainC and __name__=='__main__':
	#startT=T.clock()
	app=PicM(0)
	app.MainLoop()
	_ct.mainC.save()
