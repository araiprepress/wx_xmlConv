#! c:/Python27/python.exe
# -*- coding: utf-8 -*-

import sys, os.path
import codecs
import re

from lxml import etree
import io

import wx
import wx.stc as stc

#IDs
ID_TARGET_XSLTFN = wx.NewId()
ID_TARGET_XMLFN  = wx.NewId()
ID_TARGET_LOG    = wx.NewId()

#settings


class BaseFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="xml_xslt > html", size=(500,400))

        self.CreateMainPanel()

    def CreateMainPanel(self):
        panel_Trn = wx.Panel(self, wx.ID_ANY)
        panel_Trn.SetBackgroundColour("#FDFBF8")


#panel_Trn  control items:
        btn_Load_xslt = wx.Button(panel_Trn, wx.ID_ANY, "XSL(T)ファイルを選択", size=(150,25))
        self.xslt_fn_TextCtrl = wx.TextCtrl(panel_Trn, ID_TARGET_XSLTFN, style=wx.TE_LEFT)

        btn_Load_xml_file = wx.Button(panel_Trn, wx.ID_ANY, "XMLファイルを選択（単数）", size=(150,25))
        self.xml_fn_TextCtrl  = wx.TextCtrl(panel_Trn, ID_TARGET_XSLTFN, style=wx.TE_LEFT)

        btn_Trn_excute = wx.Button(panel_Trn, wx.ID_ANY, "変換実行", size=(150,25))
        btn_Exit = wx.Button(panel_Trn, wx.ID_EXIT, "終　了", size=(150,25))#これは明らかにexitボタンです

        self.log_TextCtrl = wx.TextCtrl(panel_Trn, ID_TARGET_LOG, style=wx.TE_LEFT|wx.TE_MULTILINE)
        btn_ClearLog = wx.Button(panel_Trn, wx.ID_ANY, "メッセージをクリア", size=(150,25))

#Bind() buttons:
        btn_Load_xslt.Bind(wx.EVT_BUTTON, self.loadXslt)
        btn_Load_xml_file.Bind(wx.EVT_BUTTON, self.loadXmlFile)
        btn_Trn_excute.Bind(wx.EVT_BUTTON, self.transform_to_Html)
        btn_Exit.Bind(wx.EVT_BUTTON, self.exitApp)
        btn_ClearLog.Bind(wx.EVT_BUTTON, self.clearLog)


#panel_Trn  layout:
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizerH = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(btn_Load_xslt, border=5, flag = wx.ALL)
        sizer.Add(self.xslt_fn_TextCtrl, border=5, flag = wx.ALL|wx.EXPAND)
        sizer.Add(wx.Size(0,5))
        sizer.Add(btn_Load_xml_file, border=5, flag = wx.ALL)
        sizer.Add(self.xml_fn_TextCtrl, border=5, flag = wx.ALL|wx.EXPAND)
        sizer.Add(btn_Trn_excute, border=5, flag = wx.ALL)
        sizer.Add(wx.StaticLine(panel_Trn), flag=wx.EXPAND)

        sizer.Add(wx.StaticText(panel_Trn, wx.ID_ANY, "　メッセージ:"))
        sizer.Add(self.log_TextCtrl, border=5, proportion=1, flag = wx.ALL|wx.EXPAND)

        sizerH.Add(btn_ClearLog, border=5, flag = wx.ALL)
        sizerH.Add(btn_Exit, border=5, flag = wx.ALL)
        sizer.Add(sizerH)

        panel_Trn.SetSizer(sizer)
        self.Show()



#load files for transform
    def loadXslt(self, event):
        """ load xsl(t) : self.pathName>self.xslt_fn_TextCtrl"""
        self.xslt_fn_TextCtrl.Clear()
        xslt_wildCard = "xslt(*.xsl,*.xslt)|*.xsl;*.xslt"
        fileDialogXSLT = wx.FileDialog(self, "XSL(T)ファイルをロード", defaultFile="*.xsl/*.xslt", wildcard=xslt_wildCard, style=wx.FD_DEFAULT_STYLE)
        if fileDialogXSLT.ShowModal() == wx.ID_OK:
            self.pathName = fileDialogXSLT.GetPath()
            self.xslt_fn_TextCtrl.SetValue(self.pathName)
        fileDialogXSLT.Destroy()
        #self.xslt_fn_TextCtrl.SetEditable(False)

    def loadXmlFile(self,event):
        """ load xml file : self.pathNameXml>self.xml_fn_TextCtrl"""
        self.xml_fn_TextCtrl.Clear()
        xml_wildCard = "xml(*.xml)|*.xml"
        fileDialogXML = wx.FileDialog(self, "XMLファイルをロード", defaultFile="*.xml", wildcard=xml_wildCard, style=wx.FD_DEFAULT_STYLE)
        if fileDialogXML.ShowModal() == wx.ID_OK:
            self.pathNameXml = fileDialogXML.GetPath()
            self.xml_fn_TextCtrl.SetValue(self.pathNameXml)
        fileDialogXML.Destroy()
        #print self.xml_filenames   OK

#transform
    def transform_to_Html(self, event):
        """ transform xml + xsl(t) > html """
        xsl_str = ''
        log_str = ''
        if self.xslt_fn_TextCtrl.GetValue() !="":
            try:
                xsl_f = open(self.xslt_fn_TextCtrl.GetValue(), "r")
                for xsl_line in xsl_f:
                    xsl_str = xsl_str + xsl_line
                xsl_root = etree.XML(xsl_str)
                xsl_transform = etree.XSLT(xsl_root)
            except etree.XMLSyntaxError as errr:
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'XMLSyntaxError in '+self.pathName +'\n'+'message: '+errr.message+'\n'
                log_str += 'type: '+ str(type(errr))+'\n'
            except IOError as errr:
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'IOError in XSL(T): message: '+errr.message+'\n'
                log_str += 'type: '+ str(type(errr))+'\n'
            except Exception as errr:
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'Message: '+errr.message+'\n'
                log_str += 'type: '+ str(type(errr))+'\n'
            #self.AppendLogString(log_str)
            self.log_TextCtrl.AppendText(log_str)


        if self.xml_fn_TextCtrl.GetValue() !="":
            new_filepath=""
            tar_xmlfile = open(self.xml_fn_TextCtrl.GetValue(), "r")
            tr_xmlfn = self.xml_fn_TextCtrl.GetValue()
            new_filepath = tr_xmlfn.replace('.xml','.html')
            try:
                tar_xmlfile = open(self.xml_fn_TextCtrl.GetValue(), "r")
                #tr_xmlfn = self.xml_fn_TextCtrl.GetValue()
                tr_xml_tree = etree.parse(tar_xmlfile)
                new_HtmlTree = xsl_transform(tr_xml_tree)###########
                tar_xmlfile.close()
            
                new_f = open(new_filepath, "w")
                new_f.write(str(new_HtmlTree))
                new_f.close()
                log_str += tr_xmlfn + " :: OK " +"\n"
            except etree.XMLSyntaxError as err:
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'XMLSyntaxError in ' + tr_xmlfn + ' Message: '+err.message+'\n'
                log_str += 'type: '+ str(type(err))+'\n'
            except IOError as err:
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'IOError in your xml file: Message: '+err.message+'\n'
                log_str += 'type: '+ str(type(err))+'\n'
            except Exception as err:
                self.log_TextCtrl.SetForegroundColour((255,0,0))
                log_str += 'Message: '+err.message+'\n'
                log_str += 'type: '+ str(type(err))+'\n'
            #self.AppendLogString(log_str)
            self.log_TextCtrl.AppendText(log_str)

#logs

    def clearLog(self, event):
        """ clear log tex """
        self.log_TextCtrl.SetForegroundColour((0,0,0))
        self.log_TextCtrl.Clear()


    #def AppendLogString(self, erString):
    #    logStr = erString+"\n"
    #    self.log_TextCtrl.AppendText(logStr)
        

    def exitApp(self, event):
        wx.Exit()



app = wx.App(False)
BaseFrame('wxFrame')
app.MainLoop()

