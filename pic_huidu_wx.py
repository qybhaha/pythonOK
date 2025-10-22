import wx
import wx.xrc
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


class MyFrame1 ( wx.Frame ):
   pic_list = []
   def __init__( self, parent ):
      wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"图片灰度计算", pos = wx.DefaultPosition, size = wx.Size( 285,354 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.ICONIZE|wx.MINIMIZE|wx.TAB_TRAVERSAL )

      self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
      self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

      bSizer1 = wx.BoxSizer( wx.VERTICAL )

      self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"图片灰度计算（全图法）", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
      self.m_staticText1.Wrap( -1 )

      self.m_staticText1.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

      bSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

      self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
      bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 3 )

      bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

      self.m_button1 = wx.Button( self, wx.ID_ANY, u"选择图片", wx.DefaultPosition, wx.DefaultSize, 0 )
      bSizer2.Add( self.m_button1, 0, wx.ALL, 3 )

      self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"共选择了", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText2.Wrap( -1 )

      bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

      self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText3.Wrap( -1 )

      bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )

      self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"张图片", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText4.Wrap( -1 )

      bSizer2.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


      bSizer1.Add( bSizer2, 0, wx.EXPAND, 2 )

      self.m_button2 = wx.Button( self, wx.ID_ANY, u"查看结果", wx.DefaultPosition, wx.DefaultSize, 0 )
      bSizer1.Add( self.m_button2, 0, wx.ALL, 3 )

      self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, style = wx.TE_MULTILINE)
      self.m_textCtrl1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

      bSizer1.Add( self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )

      self.SetSizer( bSizer1 )
      self.Layout()

      self.Centre( wx.BOTH )

      # Connect Events
      self.m_button1.Bind( wx.EVT_BUTTON, self.click1 )
      self.m_button2.Bind( wx.EVT_BUTTON, self.click2 )


   def __del__( self ):
      pass


   # Virtual event handlers, overide them in your derived class
   def click1( self, event ):
      #加载图片
      wildcard = "JPG(*.jpg)|*.jpg|PNG(*.png)|*.png"
      dlg = wx.FileDialog(self, "Choose pictures", os.getcwd(), "", wildcard, wx.FD_OPEN|wx.FD_MULTIPLE)
      if dlg.ShowModal() == wx.ID_OK:
         self.pic_list = dlg.GetPaths()
         # 验证
         # print(self.pic_list)
         self.m_staticText3.SetLabel(str(len(self.pic_list)))
      event.Skip()

   def click2( self, event ):
     #计算每张图片灰度
      self.m_textCtrl1.SetValue('')
      if self.pic_list == []:
         wx.MessageBox('未选择图片！', 'Info', wx.OK | wx.ICON_INFORMATION)
      else:
         words = ''
         for f in self.pic_list:
            name = f.split('\\')[-1]
            n1 = plt.imread(f)
            #print(n1) 每个点都是三维数
            n2 = np.array([0.299, 0.587, 0.114])
            x = np.dot(n1, n2)
            #print(x)  每个点变成一维数
            words = words + name + ' 的灰度值为 ' + str('%.2f'%x.mean()) + '\n\n'
         self.m_textCtrl1.SetValue(words)

      event.Skip()


if __name__ == "__main__":

      app = wx.App()
      today = dt.date.today()
      if today.year != 2022:
         wx.MessageBox('证书已过期！', 'Info', wx.OK | wx.ICON_INFORMATION)
      else:
         window = MyFrame1(None)     #MyFrame1是项目中定义的窗口名
         window.Show(True)
         app.MainLoop()
