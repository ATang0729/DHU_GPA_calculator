'''使用wx编写一个绩点计算器'''

import wx
import pandas as pd


# 生成一个继承wx.Frame的类
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 300))
        # 创建欢迎语
        self.welcome = wx.StaticText(self, label='欢迎使用绩点计算器，请选择功能', size=(300, 25),style=wx.ALIGN_CENTER)
        # 创建功能选择按钮，绑定事件
        self.button1 = wx.Button(self, label='计算课程绩点', size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.OnClick1, self.button1)
        self.button2 = wx.Button(self, label='预测课程绩点', size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.OnClick2, self.button2)
        self.button3 = wx.Button(self, label='退出', size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.exit, self.button3)

        self.hint = wx.StaticText(self, label='提示：请将成绩单以Excel格式保存，示例图片位于“计算课程绩点”中', size=(350, 60))
        # 创建一个垂直方向的box布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.welcome, proportion=0, flag=wx.CENTER, border=10)
        btnBox.Add(self.button1, proportion=0, flag=wx.ALL, border=10)
        btnBox.Add(self.button2, proportion=0, flag=wx.ALL, border=10)
        btnBox.Add(self.button3, proportion=0, flag=wx.ALL, border=10)
        vbox.Add(btnBox, proportion=0, flag=wx.ALL, border=10)
        vbox.Add(self.hint, proportion=0, flag=wx.CENTER, border=10)

        # 设置背景颜色
        self.SetBackgroundColour('white')
        # 设置box间隔
        vbox.SetSizeHints(self)
        self.SetSizer(vbox)

    def OnClick1(self, event):
        # 关闭当前窗口并打开“绩点计算窗口”
        self.Close()
        window = GPA_Counter1(None, title="计算课程绩点")
        window.Show()
        window.Center()
    
    def OnClick2(self, event):
        # 关闭当前窗口并打开“预测绩点窗口”
        self.Close()
        window = GPA_Counter2(None, title="预测课程绩点")
        window.Show()
        window.Center()

    def exit(self, event):
        # 退出程序
        self.Close()

class GPA_Counter1(wx.Frame):
    def __init__(self, parent, title="绩点计算"):
        wx.Frame.__init__(self, parent, title=title, size=(500, 300))
        self.termList = []
        # 弹出提示框
        wx.MessageBox('请将教务处的成绩报告单中的表格按原格式复制到Excel文件中，如有奖励学分，请手动添加（课程名称、学分、成绩和是否记绩点）！', '提示', wx.OK | wx.ICON_INFORMATION)
        # 显示示例图片
        self.hint = wx.StaticText(self, label='Excel示例格式')
        image = wx.Image('example.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.Bitmap = wx.StaticBitmap(self, -1, image, (0, 0), (image.GetWidth(), image.GetHeight()))
        # 创建“学期”复选框
        self.term = wx.StaticText(self, label='选择学期')
        self.term1 = wx.CheckBox(self, label='1A')
        self.term2 = wx.CheckBox(self, label='1S')
        self.term3 = wx.CheckBox(self, label='2A')
        self.term4 = wx.CheckBox(self, label='2S')
        self.term5 = wx.CheckBox(self, label='3A')
        self.term6 = wx.CheckBox(self, label='3S')
        self.term7 = wx.CheckBox(self, label='4A')
        self.term8 = wx.CheckBox(self, label='4S')
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term1)
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term2)
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term3)
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term4)
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term5)
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term6)
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term7)
        self.Bind(wx.EVT_CHECKBOX, self.check, self.term8)
        # 创建“文件路径”输入框和文件选择按钮
        self.path = wx.StaticText(self, label='Excel文件路径')
        self.path_input = wx.TextCtrl(self, style=wx.TE_READONLY, size=(350, 25))
        self.selectBtn = wx.Button(self, label='选择Excel文件')
        # 创建表格显示窗口
        self.table = wx.ListCtrl(self, size=(600, 400), style=wx.LC_REPORT)
        self.table.InsertColumn(0, '课程名称', width=100, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(1, '学分', width=50, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(2, '课程性质', width=100, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(3, '成绩', width=50, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(4, '是否记学分', width=125, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(5, '是否记绩点', width=125, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(6, '备注', width=50, format=wx.LIST_FORMAT_CENTER)
        # 创建“显示”按钮
        self.showBtn = wx.Button(self, label='读取')
        # 创建“计算”按钮
        self.computeBtn = wx.Button(self, label='计算')
        # 创建“清空”按钮
        self.clearBtn = wx.Button(self, label='清空')
        # 创建“返回”按钮
        self.backBtn = wx.Button(self, label='返回')
        
        self.score = wx.StaticText(self, label='总学分', size=(50, 20))
        self.score_output = wx.TextCtrl(self, style=wx.TE_READONLY, size=(50, 35))
        self.grade = wx.StaticText(self, label='总成绩', size=(50, 20))
        self.grade_output = wx.TextCtrl(self, style=wx.TE_READONLY, size=(50, 35))
        self.gpa = wx.StaticText(self, label='绩点', size=(50, 20))
        self.gpa_output = wx.TextCtrl(self, style=wx.TE_READONLY, size=(50, 35))

        self.nextBtn = wx.Button(self, label='绩点已更新，但成绩单未更新。想知道出的是哪门课的成绩？点击此处进行课程预测！')
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.select, self.selectBtn)
        self.Bind(wx.EVT_BUTTON, self.compute, self.computeBtn)
        self.Bind(wx.EVT_BUTTON, self.clear, self.clearBtn)
        self.Bind(wx.EVT_BUTTON, self.back, self.backBtn)
        self.Bind(wx.EVT_BUTTON, self.tabledisplay, self.showBtn)
        self.Bind(wx.EVT_BUTTON, self.next, self.nextBtn)
        # 创建一个垂直方向的box布局管理器
        mainbox = wx.BoxSizer(wx.VERTICAL)
        checkbox = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box1 = wx.BoxSizer(wx.VERTICAL)
        hintbox = wx.BoxSizer(wx.VERTICAL)
        pathbox = wx.BoxSizer(wx.HORIZONTAL)
        tablebox = wx.BoxSizer(wx.HORIZONTAL)
        btnbox = wx.BoxSizer(wx.VERTICAL)
        scorebox = wx.BoxSizer(wx.HORIZONTAL)
        gradebox = wx.BoxSizer(wx.HORIZONTAL)
        gpa_box = wx.BoxSizer(wx.HORIZONTAL)
        # 将各个控件添加到box布局管理器中
        hintbox.Add(self.hint, 0, wx.ALIGN_CENTER)
        hintbox.Add(self.Bitmap, 0, wx.ALIGN_CENTER)
        checkbox.Add(self.term, 0, wx.ALL, 5)
        checkbox.Add(self.term1, 0, wx.ALL, 5)
        checkbox.Add(self.term2, 0, wx.ALL, 5)
        checkbox.Add(self.term3, 0, wx.ALL, 5)
        checkbox.Add(self.term4, 0, wx.ALL, 5)
        checkbox.Add(self.term5, 0, wx.ALL, 5)
        checkbox.Add(self.term6, 0, wx.ALL, 5)
        checkbox.Add(self.term7, 0, wx.ALL, 5)
        checkbox.Add(self.term8, 0, wx.ALL, 5)
        pathbox.Add(self.path, 0, wx.ALL, 5)
        pathbox.Add(self.path_input, 0, wx.ALL, 5)
        pathbox.Add(self.selectBtn, 0, wx.ALIGN_CENTER)
        scorebox.Add(self.score, 0, wx.ALIGN_CENTER, 0)
        scorebox.Add(self.score_output, 0, wx.ALIGN_CENTER, 0)
        gradebox.Add(self.grade, 0, wx.ALIGN_CENTER, 0)
        gradebox.Add(self.grade_output, 0, wx.ALIGN_CENTER, 0)
        gpa_box.Add(self.gpa, 0, wx.ALIGN_CENTER, 0)
        gpa_box.Add(self.gpa_output, 0, wx.ALIGN_CENTER, 0)
        btnbox.Add(self.showBtn, 0, wx.ALL, 10)
        btnbox.Add(self.computeBtn, 0, wx.ALL,10)
        btnbox.Add(self.clearBtn, 0, wx.ALL,10)
        btnbox.Add(self.backBtn, 0, wx.ALL,10)
        btnbox.Add(scorebox, 0, wx.ALL, 10)
        btnbox.Add(gradebox, 0, wx.ALL, 10)
        btnbox.Add(gpa_box, 0, wx.ALL, 10)

        tablebox.Add(self.table, 0, wx.ALIGN_CENTER)
        tablebox.Add(btnbox, 0, wx.ALIGN_CENTER)

        box1.Add(pathbox, 0, wx.ALL, 5)
        box1.Add(tablebox, 0, wx.ALL, 5)

        box.Add(hintbox, 0, wx.ALIGN_CENTER)
        box.Add(box1, 0, wx.ALIGN_CENTER)

        mainbox.Add(checkbox, 0, wx.ALIGN_CENTER)
        mainbox.Add(box, 0, wx.ALIGN_CENTER)
        mainbox.Add(self.nextBtn, 0, wx.CENTER, border=10)

        self.SetBackgroundColour('white')
        mainbox.SetSizeHints(self)
        self.SetSizer(mainbox)

        self.showBtn.Disable()

    def check(self, event):
        self.termList = []  # 初始化学期列表
        for i in [self.term1, self.term2, self.term3, self.term4, self.term5, self.term6, self.term7, self.term8]:
            if i.GetValue():
                self.termList.append(i.GetLabel())
        if not self.termList:
            self.showBtn.Disable()
        elif self.path_input.GetValue():
            self.showBtn.Enable()
        print(self.termList)
    
    def tabledisplay(self, event=None):
        # 读取Excel文件，并显示在self.table
        pds = []
        for sheet in self.termList:
            self.data = pd.read_excel(self.path_input.GetValue(), sheet_name=sheet, header=0)
            pds.append(self.data)
        self.df = pd.concat(pds)
        self.table.DeleteAllItems()
        for i in range(len(self.df)):
            self.table.InsertItem(i, str(self.df.iloc[i, 0]))
            self.table.SetItem(i, 1, str(self.df.iloc[i, 1]))
            self.table.SetItem(i, 2, str(self.df.iloc[i, 2]))
            self.table.SetItem(i, 3, str(self.df.iloc[i, 3]))
            self.table.SetItem(i, 4, str(self.df.iloc[i, 4]))
            self.table.SetItem(i, 5, str(self.df.iloc[i, 5]))
            self.table.SetItem(i, 6, str(self.df.iloc[i, 6]))

    def select(self, event):
        if self.termList == []:
            wx.MessageBox('请选择学期', '提示', wx.OK | wx.ICON_INFORMATION)
            return 0
        # 创建文件选择对话框
        dialog = wx.FileDialog(None, '选择文件', '', '', 'Excel文件(*.xls;*.xlsx)|*.xls;*.xlsx', wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.path_input.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.showBtn.Enable()
        self.tabledisplay()

    def compute(self, event):
        if self.path_input.GetValue() == '':
            wx.MessageBox('请先选择文件！', '提示', wx.OK | wx.ICON_INFORMATION)
            return 0
        # 总有效学分
        totalscore = 0
        # 总加权分
        totalgrade = 0
        for i in range(len(self.df)):
            if self.df.iloc[i, 5] == '是':
                if pd.isnull(self.df.iloc[i, 3]):
                    continue
                totalscore += float(self.df.iloc[i, 1])
                totalgrade += float(self.df.iloc[i, 1])*float(self.df.iloc[i, 3])
                print(totalgrade, totalscore)
        gpa = round((totalgrade/totalscore)/10-5,5)
        self.score_output.SetLabel(str(totalscore))
        self.grade_output.SetLabel(str(totalgrade))
        self.gpa_output.SetValue(str(gpa))

    def clear(self, event):
        self.table.DeleteAllItems()
        self.gpa_output.SetValue('')
        self.score_output.SetLabel('')
        self.grade_output.SetLabel('')

    def back(self, event):
        frm = MainFrame(None, title="绩点计算器")
        frm.Show()
        self.Destroy() 
        frm.Center()

    def next(self, event):
        if self.gpa_output.GetValue() == '':
            wx.MessageBox('请先计算绩点！', '提示', wx.OK | wx.ICON_INFORMATION)
            return 0
        frm = GPA_Counter2(None, 
                           title="预测课程绩点",
                           flag=True,
                           score=self.score_output.GetValue(),
                           grade=self.grade_output.GetValue(),
                           gpa=self.gpa_output.GetValue())
        frm.Show()
        self.Destroy() 
        frm.Center()


class GPA_Counter2(wx.Frame):
    def __init__(self, parent, title, flag=False,score=None,grade=None,gpa=None):
        wx.Frame.__init__(self, parent, title=title, size=(500, 500))
        self.score = wx.StaticText(self, label='总有效学分：')
        self.score_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.grade = wx.StaticText(self, label='总加权分：')
        self.grade_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.gpa1 = wx.StaticText(self, label='成绩单绩点：')
        self.gpa1_input = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.gpa2 = wx.StaticText(self, label='实际绩点：')
        self.gpa2_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.funcBtn = wx.Button(self, label='不知道总有效学分/总加权分？点击此处进行成绩计算！')

        self.TermRadio = wx.RadioBox(self, label='待预测学期', 
                                    choices=['1A','1S','2A','2S','3A','3S','4A','4S'])

        self.NumRadio = wx.RadioBox(self, label='待预测课程数',
                                    choices=['1'])

        # 创建“文件路径”输入框和文件选择按钮
        self.path = wx.StaticText(self, label='Excel文件路径')
        self.path_input = wx.TextCtrl(self, style=wx.TE_READONLY, size=(350, 25))
        self.selectBtn = wx.Button(self, label='选择Excel文件')
        # 创建表格显示窗口
        self.tableText1 = wx.StaticText(self, label='待预测学期成绩单')
        self.table = wx.ListCtrl(self, size=(600, 400), style=wx.LC_REPORT)
        self.table.InsertColumn(0, '课程名称', width=100, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(1, '学分', width=50, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(2, '课程性质', width=100, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(3, '成绩', width=50, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(4, '是否记学分', width=125, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(5, '是否记绩点', width=125, format=wx.LIST_FORMAT_CENTER)
        self.table.InsertColumn(6, '备注', width=50, format=wx.LIST_FORMAT_CENTER)
        # 创建“显示”按钮
        self.showBtn = wx.Button(self, label='读取')
        # 创建“计算”按钮
        self.computeBtn = wx.Button(self, label='计算')
        # 创建“清空”按钮
        self.clearBtn = wx.Button(self, label='清空')
        # 创建“返回”按钮
        self.backBtn = wx.Button(self, label='返回')

        self.rangeText = wx.StaticText(self, label='预测课程分数上下限（选填）',size=(200, 50))
        self.topText_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,size=(60, 40))
        self.symbolText = wx.StaticText(self, label='~',size=(20, 40))
        self.bottomText_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,size=(60, 40))

        self.tableText2 = wx.StaticText(self, label='预测结果')
        self.table2 = wx.ListCtrl(self, size=(200, 400), style=wx.LC_REPORT)
        self.table2.InsertColumn(0, '课程名称', width=100, format=wx.LIST_FORMAT_CENTER)
        self.table2.InsertColumn(1, '学分', width=50, format=wx.LIST_FORMAT_CENTER)
        self.table2.InsertColumn(2, '成绩', width=50, format=wx.LIST_FORMAT_CENTER)

        mainbox = wx.BoxSizer(wx.VERTICAL)
        enterBox = wx.BoxSizer(wx.HORIZONTAL)
        radioBox = wx.BoxSizer(wx.HORIZONTAL)
        pathBox = wx.BoxSizer(wx.HORIZONTAL)
        tableBox = wx.BoxSizer(wx.HORIZONTAL)
        table1Box = wx.BoxSizer(wx.VERTICAL)
        rangeBox = wx.BoxSizer(wx.VERTICAL)
        rangeBox2 = wx.BoxSizer(wx.HORIZONTAL)
        table2Box = wx.BoxSizer(wx.VERTICAL)
        btnBox = wx.BoxSizer(wx.HORIZONTAL)

        enterBox.Add(self.score, 0, wx.ALIGN_CENTER, 5)
        enterBox.Add(self.score_input, 0, wx.ALIGN_CENTER, 5)
        enterBox.Add(self.grade, 0, wx.ALIGN_CENTER, 5)
        enterBox.Add(self.grade_input, 0, wx.ALIGN_CENTER, 5)
        enterBox.Add(self.gpa1, 0, wx.ALIGN_CENTER, 5)
        enterBox.Add(self.gpa1_input, 0, wx.ALIGN_CENTER, 5)
        enterBox.Add(self.gpa2, 0, wx.ALIGN_CENTER, 5)
        enterBox.Add(self.gpa2_input, 0, wx.ALIGN_CENTER, 5)
        radioBox.Add(self.TermRadio, 0, wx.ALL, 5)
        radioBox.Add(self.NumRadio, 0, wx.ALL, 5)
        pathBox.Add(self.path, 0, wx.ALL, 5)
        pathBox.Add(self.path_input, 0, wx.ALL, 5)
        pathBox.Add(self.selectBtn, 0, wx.ALL, 5)
        table1Box.Add(self.tableText1, 0, wx.ALL, 5)
        table1Box.Add(self.table, 0, wx.ALL, 5)
        rangeBox2.Add(self.bottomText_input, 0, wx.ALL, 5)
        rangeBox2.Add(self.symbolText, 0, wx.ALL, 5)
        rangeBox2.Add(self.topText_input, 0, wx.ALL, 5)
        rangeBox.Add(self.rangeText, 0, wx.ALL, 5)
        rangeBox.Add(rangeBox2, 0, wx.ALL, 5)
        table2Box.Add(self.tableText2, 0, wx.ALL, 5)
        table2Box.Add(self.table2, 0, wx.ALL, 5)
        tableBox.Add(table1Box, 0, wx.ALL, 5)
        tableBox.Add(rangeBox, 0, wx.ALL, 5)
        tableBox.Add(table2Box, 0, wx.ALL, 5)
        btnBox.Add(self.showBtn, 0, wx.ALL, 5)
        btnBox.Add(self.computeBtn, 0, wx.ALL, 5)
        btnBox.Add(self.clearBtn, 0, wx.ALL, 5)
        btnBox.Add(self.backBtn, 0, wx.ALL, 5)

        mainbox.Add(enterBox, 0, wx.CENTER, 5)
        mainbox.Add(self.funcBtn, 0, wx.CENTER, 5)
        mainbox.Add(radioBox, 0, wx.CENTER, 5)
        mainbox.Add(pathBox, 0, wx.CENTER, 5)
        mainbox.Add(tableBox, 0, wx.CENTER, 5)
        mainbox.Add(btnBox, 0, wx.CENTER, 5)

        self.SetBackgroundColour('white')
        mainbox.SetSizeHints(self)
        self.SetSizer(mainbox)

        if flag:
            self.score_input.SetValue(score)
            self.grade_input.SetValue(grade)
            self.gpa1_input.SetValue(gpa)
            self.score_input.Disable()
            self.grade_input.Disable()

        self.Bind(wx.EVT_BUTTON, self.OnFunc, self.funcBtn)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, self.selectBtn)
        self.Bind(wx.EVT_BUTTON, self.OnShow, self.showBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCompute, self.computeBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.clearBtn)
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.backBtn)

        self.Bind(wx.EVT_TEXT, self.GPA, self.score_input)
        self.Bind(wx.EVT_TEXT, self.GPA, self.grade_input)

        self.showBtn.Disable()

    def GPA(self, event):
        if not(self.score_input.GetValue() == '' or self.grade_input.GetValue() == ''):
            self.gpa1_input.SetValue(str(round(float(self.grade_input.GetValue()) / float(self.score_input.GetValue())/10-5,5)))

    def OnFunc(self, event):
        frm = GPA_Counter1(None, title='GPA计算器')
        frm.Show()
        self.Destroy() 
        frm.Center()

    def OnSelect(self, event):
        if self.score_input.GetValue() == '' or self.grade_input.GetValue() == '' or self.gpa2_input.GetValue() == '':
            wx.MessageBox('请先输入成绩、学分和实际绩点', '提示', wx.OK | wx.ICON_INFORMATION)
            return 0
        dlg = wx.FileDialog(self, message='选择文件', defaultFile='', wildcard='*.xls;*.xlsx', style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.path_input.SetValue(dlg.GetPath())
        dlg.Destroy()
        self.showBtn.Enable()
        self.OnShow()

    def OnShow(self, event=None):
        # 读取Excel文件，并显示在self.table
        sheet = self.TermRadio.GetStringSelection()
        self.data = pd.read_excel(self.path_input.GetValue(), sheet_name=sheet, header=0)
        self.table.DeleteAllItems()
        for i in range(len(self.data)):
            self.table.InsertItem(i, str(self.data.iloc[i, 0]))
            self.table.SetItem(i, 1, str(self.data.iloc[i, 1]))
            self.table.SetItem(i, 2, str(self.data.iloc[i, 2]))
            self.table.SetItem(i, 3, str(self.data.iloc[i, 3]))
            self.table.SetItem(i, 4, str(self.data.iloc[i, 4]))
            self.table.SetItem(i, 5, str(self.data.iloc[i, 5]))
            self.table.SetItem(i, 6, str(self.data.iloc[i, 6]))

    def OnCompute(self, event):
        if not self.topText_input.GetValue() == '':
            top = int(self.topText_input.GetValue())
        else:
            top = 100
        if not self.bottomText_input.GetValue() == '':
            bottom = int(self.bottomText_input.GetValue())
        else:
            bottom = 0
        num = self.NumRadio.GetStringSelection()
        pre_list = []
        if num == '1':
            for i in range(len(self.data)):
                dummy_score = float(self.score_input.GetValue())
                dummy_score += float(self.data.iloc[i, 1])
                print('dummy_score:',dummy_score)
                for grade in range(top, bottom, -1):
                    dummy_grade = float(self.grade_input.GetValue())
                    dummy_grade += float(self.data.iloc[i, 1])*grade
                    print('dummy_grade:',dummy_grade)
                    diff = abs(dummy_grade / dummy_score / 10 - 5 - float(self.gpa2_input.GetValue()))
                    print(diff)
                    if diff<=0.0001:
                        pre = [self.data.iloc[i, 0], str(self.data.iloc[i, 1]), str(grade)]
                        pre_list.append(pre)
                        pre_list.append(['','',''])
            if len(pre_list) == 0:
                wx.MessageBox('无可行解', '提示', wx.OK | wx.ICON_INFORMATION)
                return 0
            else:
                for i in range(len(pre_list)):
                    self.table2.InsertItem(i, pre_list[i][0])
                    self.table2.SetItem(i, 1, pre_list[i][1])
                    self.table2.SetItem(i, 2, pre_list[i][2])

    def OnClear(self, event):
        self.table.DeleteAllItems()
        self.table2.DeleteAllItems()
    
    def OnBack(self, event):
        frm = MainFrame(None, title="绩点计算器")
        frm.Show()
        self.Destroy() 
        frm.Center()
        

if __name__ == "__main__":
    app = wx.App()
    frm = MainFrame(None, title="绩点计算器")
    frm.Show()
    frm.Center()
    app.MainLoop()
