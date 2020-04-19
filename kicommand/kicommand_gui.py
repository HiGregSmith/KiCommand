# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 28 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.richtext

###########################################################################
## Class kicommand_panel
###########################################################################

class kicommand_panel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_mgr.AddPane( self.m_panel1, wx.aui.AuiPaneInfo() .Center() .CaptionVisible( False ).CloseButton( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( True ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		entryboxChoices = []
		self.entrybox = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"help", wx.DefaultPosition, wx.DefaultSize, entryboxChoices, wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER )
		bSizer2.Add( self.entrybox, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.outputbox = wx.richtext.RichTextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS|wx.TE_RICH )
		bSizer2.Add( self.outputbox, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		
		self.m_mgr.Update()
		
		# Connect Events
		self.entrybox.Bind( wx.EVT_TEXT_ENTER, self.process )
	
	def __del__( self ):
		self.m_mgr.UnInit()
		
	
	
	# Virtual event handlers, overide them in your derived class
	def process( self, event ):
		event.Skip()
	

