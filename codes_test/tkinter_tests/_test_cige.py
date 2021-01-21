#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from pathlib import Path
from midi import cige

DEFAULT_FONT = ('unifont', 10)
ROOT = '../../midis'


class MyGUI(object):
    def __init__(self, window):
        self.window = window

    # 设置窗口
    def set_window(self):
        # 窗口
        self.window.title('从 MIDI 文件生成词格')          # 窗口名
        self.window.geometry('1280x720+80+80')             # ?x? 为窗口大小，+? +? 定义窗口弹出时的默认展示位置
        self.window.resizable(width=0, height=0)           # 不可改变窗口大小
        self.window.attributes("-alpha", 0.95)              # 透明度，值越小透明度越高
        self.window.iconbitmap('./icons/books.ico')

        # 标签
        self.label_files = Label(self.window, text='请选择 MIDI 文件', borderwidth=2, relief='groove', font=DEFAULT_FONT)
        self.label_files.place(x=20, y=20, width=240, height=40)

        self.label_hits_per_bar = Label(self.window, text='请输入小节细分数 (需为 2 的幂)', borderwidth=2, relief='groove', font=DEFAULT_FONT)
        self.label_hits_per_bar.place(x=280, y=20, width=320, height=40)

        self.label_shortening_factor = Label(self.window, text='请输入缩短倍率 (需为 2 的幂)', borderwidth=2, relief='groove', font=DEFAULT_FONT)
        self.label_shortening_factor.place(x=280, y=140, width=320, height=40)

        self.label_line_breaks = Label(self.window, text='输入需要换行的小节差分数 (使用逗号分隔)', borderwidth=2, relief='groove', font=DEFAULT_FONT)
        self.label_line_breaks.place(x=280, y=260, width=320, height=40)

        self.label_result = Label(self.window, text='输出词格', borderwidth=2, relief='groove', font=DEFAULT_FONT)
        self.label_result.place(x=620, y=20, width=640, height=40)

        # 选择框
        self.listbox_files = Listbox(self.window, font=DEFAULT_FONT)
        for p in Path(ROOT).glob('*.mid'):
            self.listbox_files.insert('end', p)
        self.listbox_files.place(x=20, y=80, width=240, height=560)
        self.listbox_files.bind('<Double-1>', func=lambda event: self.button_execute_func())

        # 文本框
        self.text_hits_per_bar = Text(self.window, font=DEFAULT_FONT)
        self.text_hits_per_bar.insert('end', '16')
        self.text_hits_per_bar.place(x=280, y=80, width=320, height=40)

        self.text_shortening_factor = Text(self.window, font=DEFAULT_FONT)
        self.text_shortening_factor.insert('end', '2')
        self.text_shortening_factor.place(x=280, y=200, width=320, height=40)

        self.text_line_breaks = Text(self.window, font=DEFAULT_FONT)
        self.text_line_breaks.insert('end', '4')
        self.text_line_breaks.place(x=280, y=320, width=320, height=320)

        self.text_result = Text(self.window, state='disabled', font=DEFAULT_FONT)
        self.text_result.place(x=620, y=80, width=640, height=560)

        # 按钮
        self.button_execute = Button(self.window, text='生成', bg='light steel blue', command=self.button_execute_func, font=DEFAULT_FONT)
        self.button_execute.place(x=20, y=660, width=1240, height=40)

    # 功能函数
    def button_execute_func(self):
        try:
            filename = self.listbox_files.selection_get()
        except:
            self.text_result.config(state='normal')
            self.text_result.delete(1.0, 'end')
            self.text_result.insert(1.0, '请选择文件！')
            self.text_result.config(state='disabled')
            return

        hits_per_bar = self.text_hits_per_bar.get(1.0, 'end').strip()
        hits_per_bar = re.sub('[^\d]', '', hits_per_bar)
        if hits_per_bar != '':
            hits_per_bar = int(hits_per_bar)
        else:
            hits_per_bar = 16

        shortening_factor = self.text_shortening_factor.get(1.0, 'end').strip()
        shortening_factor = re.sub('[^\d]', '', shortening_factor)
        if shortening_factor != '':
            shortening_factor = int(shortening_factor)
        else:
            shortening_factor = 2

        line_breaks = self.text_line_breaks.get(1.0, 'end').strip()
        line_breaks = re.sub('[^\d,]', '', line_breaks)
        if line_breaks != '':
            line_breaks = [int(lb) for lb in line_breaks.split(',') if lb != '']
        else:
            line_breaks = (4, )

        try:
            out = cige(filename, hits_per_bar=hits_per_bar, line_breaks=line_breaks, shortening_factor=shortening_factor)
        except:
            out = '词格生成失败！请检查配置是否正确！'

        self.text_result.config(state='normal')
        self.text_result.delete(1.0, 'end')
        self.text_result.insert(1.0, out)
        self.text_result.config(state='disabled')


def gui_start():
    # 实例化出一个父窗口
    init_window = Tk()
    # 使用自定义类
    my_gui = MyGUI(init_window)
    # 设置根窗口默认属性
    my_gui.set_window()
    # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    init_window.mainloop()


gui_start()
