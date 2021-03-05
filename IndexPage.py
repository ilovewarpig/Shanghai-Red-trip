# 目录页
from tkinter import *
from ttkthemes import ThemedStyle
import ttkthemes
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.font as font


class IndexPage(object):
    def goIntro(self):
        self.goIntro()

    def goProvRoute(self):
        self.goProvRoute()

    def goNationalRoute(self):
        self.goNationalRoute()

    def __init__(self, goIntro, goProvRoute, goNationalRoute):

        self.goIntro = goIntro
        self.goProvRoute = goProvRoute
        self.goNationalRoute = goNationalRoute

        self.root = ttkthemes.ThemedTk(theme='adapta')# Tk()
        self.root.resizable(False, False)
        width = 800
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        align_str = '%dx%d+%d+%d'%(width, height, (screen_width-width)/2, (screen_height-height)/2)
        self.root.geometry(align_str)
        self.root.resizable(False, False)

        s = ttk.Style()

        s.configure('Red.TButton', background='#DAA520')


        myimg_index = ImageTk.PhotoImage(Image.open('openning.png').resize((width, height)))
        my_canvas_index = Canvas(self.root, width=width, height=height)
        my_canvas_index.create_image(0, 0, image=myimg_index, anchor='nw')
        my_canvas_index.place(x=0, y=0)

        # myFont = font.Font(fg='white')
        box_width = 100
        box_height = 100
        a = ttk.Button(self.root, text="场馆简介", style='Red.TButton',command=self.goIntro)
        # a['font']=myFont
        a.place(x=280, y=height/2 - box_height, width=box_width, height=box_height, )

        b = ttk.Button(self.root, text="省内路线规划", style='Red.TButton', command=self.goProvRoute)
        b.place(x=430, y=height/2 - box_height, width=box_width, height=box_height)
        c = ttk.Button(self.root, text="数据工作台", style='Red.TButton', command=self.goNationalRoute)
        c.place(x=580, y=height/2 - box_height, width=box_width, height=box_height)


        self.root.mainloop()


if __name__ == '__main__':
    root = ttkthemes.ThemedTk(theme='adapta')# Tk()
    root.resizable(False, False)
    IndexPage(None)
    root.mainloop()