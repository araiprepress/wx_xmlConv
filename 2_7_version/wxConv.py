#! c:/Python27/python.exe
# -*- coding: utf-8 -*-
import datetime
import sys, os.path
import codecs
import re

from lxml import etree
import StringIO

import wx
import wx.stc as stc

#IDs
ID_TARGET_XSLTFN = wx.NewId()
ID_TARGET_XMLFN  = wx.NewId()
ID_TARGET_LOG    = wx.NewId()

#settings

class BaseFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="xml_xslt > html", pos=(100, 100), size=(550,600))

        self.CreateMainPanel()

    def CreateMainPanel(self):
        panel_Trn = wx.Panel(self, wx.ID_ANY)
        panel_Trn.SetBackgroundColour("#FDFBF8")


#panel_Trn  control items:
        btn_Load_xslt = wx.Button(panel_Trn, wx.ID_ANY, u"XSL(T)ファイルを選択", size=(150,25))
        btn_Open_xslt = wx.Button(panel_Trn, wx.ID_ANY, u"XSL(T)ファイルを開く", size=(150,25))
        btn_Clear_xslt = wx.Button(panel_Trn, wx.ID_ANY, u"XSL(T)ファイルをクリア", size=(150,25))
        self.xslt_fn_TextCtrl = wx.TextCtrl(panel_Trn, ID_TARGET_XSLTFN, style=wx.TE_LEFT)

        btn_Load_xml_files = wx.Button(panel_Trn, wx.ID_ANY, u"XMLファイルを選択（複数可）", size=(150,25))
        btn_Unload_xml_file = wx.Button(panel_Trn, wx.ID_ANY, u"XMLファイルをリストから除外", size=(150,25))
        btn_Clear_xml_files = wx.Button(panel_Trn, wx.ID_ANY, u"XMLファイルをクリア", size=(150,25))
        xmlfnList=[]
        self.xml_fn_ListBox = wx.ListBox(panel_Trn, ID_TARGET_XMLFN, choices=xmlfnList, style=wx.LB_SINGLE)

        btn_Trn_excute = wx.Button(panel_Trn, wx.ID_ANY, u"変換実行", size=(200,25))
        btn_Exit = wx.Button(panel_Trn, wx.ID_EXIT, u"終　了", size=(200,25))#これは明らかにexitボタンです

        btn_Trn_savelog = wx.Button(panel_Trn, wx.ID_ANY, u"作業LOGを保存", size=(150,25))
        btn_ClearLog    = wx.Button(panel_Trn, wx.ID_ANY, u"LOGをクリア", size=(150,25))
        self.log_TextCtrl = wx.TextCtrl(panel_Trn, ID_TARGET_LOG, style=wx.TE_LEFT|wx.TE_MULTILINE)

#Bind() buttons:
        btn_Load_xslt.Bind(wx.EVT_BUTTON, self.loadXslt)
        btn_Open_xslt.Bind(wx.EVT_BUTTON, self.openXslt)
        btn_Clear_xslt.Bind(wx.EVT_BUTTON, self.clearXslt)#############
        btn_Load_xml_files.Bind(wx.EVT_BUTTON, self.loadXmlFiles)
        btn_Unload_xml_file.Bind(wx.EVT_BUTTON, self.unloadXmlFile)
        btn_Clear_xml_files.Bind(wx.EVT_BUTTON, self.ClearXmlFiles)############
        btn_Trn_excute.Bind(wx.EVT_BUTTON, self.transform_Xml)
        btn_Exit.Bind(wx.EVT_BUTTON, self.exitApp)
        btn_Trn_savelog.Bind(wx.EVT_BUTTON, self.saveLog)
        btn_ClearLog.Bind(wx.EVT_BUTTON, self.clearLog)

#Bind() xml_fn_ListBox:
        self.xml_fn_ListBox.Bind(wx.EVT_LISTBOX_DCLICK, self.RunOnDblClick)

#panel_Trn  layout:
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_H0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_H1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_H2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_H3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_H0.Add(btn_Load_xslt, border=5, flag = wx.ALL)
        sizer_H0.Add(btn_Open_xslt, border=5, flag = wx.ALL)
        sizer_H0.Add(btn_Clear_xslt, border=5, flag = wx.ALL)
        sizer.Add(sizer_H0)
        sizer.Add(self.xslt_fn_TextCtrl, border=5, flag = wx.ALL|wx.EXPAND)

        sizer.Add(wx.Size(0,10))
        sizer.Add(wx.StaticLine(panel_Trn), flag=wx.EXPAND)
        sizer.Add(wx.Size(0,10))

        sizer_H3.Add(btn_Load_xml_files, border=5, flag = wx.ALL)
        sizer_H3.Add(btn_Unload_xml_file, border=5, flag = wx.ALL)
        sizer_H3.Add(btn_Clear_xml_files, border=5, flag = wx.ALL)
        sizer.Add(sizer_H3)

        sizer.Add(self.xml_fn_ListBox, border=5, proportion=1, flag = wx.ALL|wx.EXPAND)#

        sizer_H1.Add(btn_Trn_excute, border=5, flag = wx.ALL)
        sizer_H1.Add(btn_Exit, border=5, flag = wx.ALL)
        sizer.Add(sizer_H1)
        sizer.Add(wx.Size(0,10))
        sizer.Add(wx.StaticLine(panel_Trn), flag=wx.EXPAND)
        sizer.Add(wx.Size(0,10))

        sizer.Add(wx.StaticText(panel_Trn, wx.ID_ANY, u"　ログ:"))
        sizer.Add(self.log_TextCtrl, border=5, proportion=1, flag = wx.ALL|wx.EXPAND)
        sizer_H2.Add(btn_Trn_savelog, border=5, flag = wx.ALL)
        sizer_H2.Add(btn_ClearLog, border=5, flag = wx.ALL)
        sizer.Add(sizer_H2)

        panel_Trn.SetSizer(sizer)
        self.Show()



#load files for transform
    def loadXslt(self, event):
        """ load xsl(t) : self.pathName>self.xslt_fn_TextCtrl"""
        self.xslt_fn_TextCtrl.Clear()
        self.xslt_fn_TextCtrl.SetForegroundColour((0,0,0))
        xslt_wildCard = "xslt(*.xsl,*.xslt)|*.xsl;*.xslt"
        fileDialogXSLT = wx.FileDialog(self, u"XSL(T)ファイルをロード", defaultFile="*.xsl/*.xslt", wildcard=xslt_wildCard, style=wx.FD_DEFAULT_STYLE)
        if fileDialogXSLT.ShowModal() == wx.ID_OK:
            self.pathName = fileDialogXSLT.GetPath()
            self.xslt_fn_TextCtrl.SetValue(self.pathName)#############
        fileDialogXSLT.Destroy()
        #self.xslt_fn_TextCtrl.SetEditable(False)

    def loadXmlFiles(self,event):
        """ load xml files :self.pathNameS>self.xml_fn_ListBox """
        self.log_TextCtrl.SetForegroundColour((0,0,0))
        xmlfnList = self.xml_fn_ListBox.GetItems()#ListBoxはiterableでないので、取りおきlistが必要！！
        xml_wildCard = "xml(*.xml)|*.xml"
        fileDialogXML = wx.FileDialog(self, u"XMLファイルをロード", defaultFile="*.xml", wildcard=xml_wildCard, style=wx.FD_DEFAULT_STYLE|wx.FD_MULTIPLE)

        if fileDialogXML.ShowModal() == wx.ID_OK:
            self.pathNameS = fileDialogXML.GetPaths()
            for pn in self.pathNameS:
                if pn not in xmlfnList:
                    # xmlfnList.append(pn)
                   self.xml_fn_ListBox.Append(pn)
            #self.xml_fn_ListBox.SetItems(xmlfnList)##############
        fileDialogXML.Destroy()

    def unloadXmlFile(self, event):
        ulSelection = self.xml_fn_ListBox.GetSelection()
        if ulSelection >-1:
            self.xml_fn_ListBox.Delete(ulSelection)
    

#transform
    def transform_Xml(self, event):
        """ transform xml + xsl(t) > html or xml """
        xsl_str = ''
        log_str = ''
        trnXsltFlag = False#xsl(t)を先にパースし、(trnXsltFlag=True)出来なければxml処理に進まない
        parser = etree.XMLParser(ns_clean=True)#namespaceはどけておく
        parser.resolvers.add(FileResolver())


        if self.xslt_fn_TextCtrl.GetValue() !="" and self.xml_fn_ListBox.GetItems() !=[] :
            try:
                xsl_f = codecs.open(self.xslt_fn_TextCtrl.GetValue(), "r", "utf-8-sig")
                xslfn = self.xslt_fn_TextCtrl.GetValue()
                xsl_root = etree.parse(xsl_f, parser)
                xsl_transform = etree.XSLT(xsl_root)
                xsl_f.close()
                trnXsltFlag = True
            except etree.XMLSyntaxError, errr:
                #self.xslt_fn_TextCtrl.SetForegroundColour((255,0,0))
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'XMLSyntaxError in : '+ self.pathName +' : '+ str(errr)+'\n'
                trnXsltFlag = False
            except IOError, errr:
                #self.xslt_fn_TextCtrl.SetForegroundColour((255,0,0))
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'IOError : '+ self.pathName +' : '+ str(errr)+'\n'
                trnXsltFlag = False
            except Exception, errr:
                #self.xslt_fn_TextCtrl.SetForegroundColour((255,0,0))
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'Unexpected error : '+ self.pathName +' : '+ str(errr)+'\n'
                trnXsltFlag = False
            if log_str != "":
                self.AppendLogString(log_str)
        
#xmlファイル処理
#xslt自体がNGなときは一切先に進まない。
        if self.xml_fn_ListBox.GetItems() !=[] and trnXsltFlag ==True:
            for tr_xmlfn in self.xml_fn_ListBox.GetItems():
                try:
                    tar_xmlfile = codecs.open(tr_xmlfn, "r", "utf-8-sig")
                    # htmlのfilename文字列を作成
                    new_filepath=""
                    #とりあえずxml名のhtmlファイルとします。
                    new_filepath = tr_xmlfn.replace('.xml','.html')

                    tr_xml_tree = etree.parse(tar_xmlfile)
                    new_HtmlTree = xsl_transform(tr_xml_tree)
                    tar_xmlfile.close()
                    new_f = open(new_filepath, "w")
                    new_f.write(str(new_HtmlTree))
                    new_f.close()

                except etree.XMLSyntaxError, errr:
                    self.log_TextCtrl.SetForegroundColour((255,0,0))
                    log_str += 'XMLSyntaxError in : ' + tr_xmlfn +' : '+ str(errr)+'\n'
                except IOError, errr:
                    self.log_TextCtrl.SetForegroundColour((255,0,0))
                    log_str += 'IOError in : ' + tr_xmlfn +' : '+ str(errr)+'\n'
                except Exception, errr:
                    self.log_TextCtrl.SetForegroundColour((255,0,0))
                    log_str += 'Unexpected error in : ' + tr_xmlfn +' : '+ str(errr)+'\n'
                else:
                    self.log_TextCtrl.SetForegroundColour((0,0,0))
                    log_str += tr_xmlfn + ":"+new_filepath+" :: OK " +"\n"

            self.AppendLogString(log_str)


#logs
    def saveLog(self, event):
        """ save log text : self.log_TextCtrl > files  """
        fileDiaSaveLog = wx.FileDialog(self, "save log ...", defaultDir=".", defaultFile=self.dtDetailStr()+"log", wildcard="*.txt", style=wx.FD_SAVE)
        if fileDiaSaveLog.ShowModal() == wx.ID_OK:
            path = fileDiaSaveLog.GetPath()
            #print path
            fp = open(path, 'w')
            fp.write(self.log_TextCtrl.GetValue())
            fp.close()
        fileDiaSaveLog.Destroy()

    def clearLog(self, event):
        """ clear log tex """
        self.log_TextCtrl.SetForegroundColour((0,0,0))
        self.log_TextCtrl.Clear()

    def dtDetailStr(self):
        dtStr=datetime.datetime.today()
        return dtStr.strftime("%Y%m%d_%H%M%S_")

#open files if need to edit or confirm
    def openXslt(self, event):
        """ Open the xsl(t) """
        OpenXsltFn = self.xslt_fn_TextCtrl.GetValue()
        if OpenXsltFn == "":
            return
        try:
            bsname = os.path.basename(OpenXsltFn)
            EditFileFrame(bsname, event, OpenXsltFn)
        except IOError, err:
            self.AppendLogString("I/O error:" + OpenXsltFn + " <-- Cannot open.")
        except:
            self.AppendLogString("Unexpected error:" + str(sys.exc_info()[0]))
            pass


    def RunOnDblClick(self, event):
        """ open the DClicked xml file on EditFileFrame """
        DCselectedXml = self.xml_fn_ListBox.GetStringSelection()

        try:
            bsname = os.path.basename(DCselectedXml)
            EditFileFrame(bsname, event, DCselectedXml)
        except IOError, err:
            self.AppendLogString("I/O error:" + DCselectedXml + " <-- Cannot open file.")
        except:
            self.AppendLogString("Unexpected error:" + str(sys.exc_info()[0]))
            pass

    def clearXslt(self, event):
        self.xslt_fn_TextCtrl.Clear()
        self.pathName=""

    def ClearXmlFiles(self, event):
        self.xml_fn_ListBox.Clear()
        self.xmlfnList=[]


    def AppendLogString(self, erString):
        logStr = erString+"\n"
        self.log_TextCtrl.AppendText(logStr)
        

    def exitApp(self, event):
        wx.Exit()

#http://lxml.de/resolvers.html#uri-resolvers　参考。
class FileResolver(etree.Resolver):
    def resolve(self, url, id, context):
        return self.resolve_filename(url, context)


########################################################################
####################  EDIT    TEXT    FRAME  ###########################
########################################################################

class EditFileFrame(wx.Frame):

    def __init__(self, title, event, DCselectedXmlFn):
        wx.Frame.__init__(self, None, -1, title, pos=(650, 100), size=(550,600))
        self.DCselectedXmlFn = DCselectedXmlFn
        self.flagDirty = False
        self.createMenuBar()
        self.createStyledTextControl()
        self.CreateStatusBar()
        self.Bind(wx.EVT_CLOSE, self.OnClose)###################
        self.Show()

    def createMenuBar(self):
    #MenuBar
        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)

    #Menu
        menu_File = wx.Menu()
        menu_Edit = wx.Menu()
        menuBar.Append(menu_File, "File")
        menuBar.Append(menu_Edit, "Edit")

    #MenuItems
        menu_File_Save   = menu_File.Append(wx.ID_ANY, "&Save"+"\t"+"Ctrl+S", "Save")
        menu_File_SaveAs = menu_File.Append(wx.ID_ANY, "&SaveAs"+"\t"+"Ctrl+Shift+S", "Save As")
        menu_File_Close  = menu_File.Append(wx.ID_CLOSE, "&Close"+"\t"+"Ctrl+W", "Close")###############

        menu_Edit_Cut    = menu_Edit.Append(wx.ID_ANY, "&Cut"+"\t"+"Ctrl+X", "Cut")
        menu_Edit_Copy   = menu_Edit.Append(wx.ID_ANY, "&Copy"+"\t"+"Ctrl+C")
        menu_Edit_Paste  = menu_Edit.Append(wx.ID_ANY, "&Paste"+"\t"+"Ctrl+V")
        menu_Edit.AppendSeparator()
        menu_Edit_Undo   = menu_Edit.Append(wx.ID_ANY, "&Undo"+"\t"+"Ctrl+Z")
        menu_Edit_Redo   = menu_Edit.Append(wx.ID_ANY, "&Redo"+"\t"+"Ctrl+Shift+Z")

        self.Bind(wx.EVT_MENU, self.OnSave,   menu_File_Save)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menu_File_SaveAs)
        self.Bind(wx.EVT_MENU, self.menuClose,  menu_File_Close)

        self.Bind(wx.EVT_MENU, self.OnCut,   menu_Edit_Cut)
        self.Bind(wx.EVT_MENU, self.OnCopy,  menu_Edit_Copy)
        self.Bind(wx.EVT_MENU, self.OnPaste, menu_Edit_Paste)
        self.Bind(wx.EVT_MENU, self.OnUndo,  menu_Edit_Undo)
        self.Bind(wx.EVT_MENU, self.OnRedo,  menu_Edit_Redo)

        self.Bind(wx.EVT_CLOSE, self.OnClose)


##################  createStyledTextControl  #################
    def createStyledTextControl(self):
        self.St_TextCtrl = stc.StyledTextCtrl(self)
        self.St_TextCtrl.SetWindowStyle(self.St_TextCtrl.GetWindowStyle() | wx.DOUBLE_BORDER)
        self.St_TextCtrl.StyleSetSpec(stc.STC_STYLE_DEFAULT, "size:10,face:Courier New")
        self.St_TextCtrl.SetWrapMode(stc.STC_WRAP_WORD) 

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.St_TextCtrl, proportion=1, border=0, flag=wx.ALL|wx.EXPAND)
        self.SetSizer(layout)

        self.St_TextCtrl.Bind(stc.EVT_STC_CHANGE, self.OnChangeTxtCtrl)
        self.OpenSelectedXml()


    def OnChangeTxtCtrl(self, e):
        lines = self.St_TextCtrl.GetLineCount()
        width = self.St_TextCtrl.TextWidth(stc.STC_STYLE_LINENUMBER, str(lines)+" ")
        self.St_TextCtrl.SetMarginWidth(0, width)



    def OpenSelectedXml(self): 
        f = codecs.open(self.DCselectedXmlFn, "r", "utf-8")
        self.St_TextCtrl.ClearAll()
        for line in f:
            self.St_TextCtrl.AddText(line)
        f.close()
        self.St_TextCtrl.SetSavePoint()#SetSavePoint sets the Document state to unmodified. 



    def OnSaveAs(self, event): 
        wildCard = "xml(*.xml)|*.xml"
        fileSaveDialog = wx.FileDialog(self, u"textファイルを保存", defaultFile="*.xml", wildcard=wildCard, style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if fileSaveDialog.ShowModal() == wx.ID_OK:
            #saveStr = self.St_TextCtrl.GetValue()
            
            saveFileName = fileSaveDialog.GetPath()
            #fileSavePath = open(saveFileName, 'w')
            fileSavePath = codecs.open(saveFileName, "w", "utf-8")
            fileSavePath.write(self.St_TextCtrl.GetText())
            fileSavePath.close()
        fileSaveDialog.Destroy()


    def OnSave(self, event):
        fileSavePath = codecs.open(self.DCselectedXmlFn, "w", "utf-8")
        fileSavePath.write(self.St_TextCtrl.GetText())
        fileSavePath.close()
        self.St_TextCtrl.SetSavePoint()#SetSavePoint sets the Document state to unmodified. 


    def OnCut(self, event):
        self.St_TextCtrl.Cut()


    def OnCopy(self, event):
        self.St_TextCtrl.Copy()


    def OnPaste(self, event):
        self.St_TextCtrl.Paste()


    def OnUndo(self, event):
        self.St_TextCtrl.Undo()


    def OnRedo(self, event):
        self.St_TextCtrl.Redo()


    def OnClose(self, event):
        if event.CanVeto() and self.St_TextCtrl.GetModify():
        #if self.St_TextCtrl.GetModify():
            d=wx.MessageDialog(self, u'Save file?', 'MessageBoxCaptionStr', wx.YES_NO|wx.YES_DEFAULT|wx.CANCEL)
            _showModal = d.ShowModal()
            d.Destroy()
            if _showModal == wx.ID_CANCEL:
                event.Veto()
                return
            if _showModal == wx.ID_YES:
                self.OnSaveAs(self)
            if _showModal == wx.ID_NO:
                event.Veto()
                self.Destroy()#このFrameのみ閉じる
                #sys.exit()#全部お終い
        event.Veto()
        self.Destroy()

    def menuClose(self, event):
        self.Close()




app = wx.App(False)
BaseFrame(u'wxFrame')
app.MainLoop()

