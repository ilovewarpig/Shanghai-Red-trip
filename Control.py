# 控制页面切换
from tkinter import *
from ProvRoute import ProvRoute
from IntroPage import IntroPage
from NationalRoute import NationalRoute
from IndexPage import IndexPage
from ttkthemes import ThemedStyle
import ttkthemes


class Control(IndexPage, IntroPage, ProvRoute, NationalRoute):

    def __init__(self):
        self.root = ttkthemes.ThemedTk(theme='adapta')# Tk()
        self.root.resizable(False, False)
        self.goIndex()
        # style = ThemedStyle(self.root)
        # style.set_theme('Adapta')
        # ttkthemes.themed_style.ThemedStyle(theme="adapta")

    # 目录页
    def goIndex(self):
        self.root.destroy()
        IndexPage.__init__(self, goIntro=self.goIntro, goProvRoute=self.goProvRoute, goNationalRoute=self.goNationalRoute)

    # 场馆介绍页
    def goIntro(self):
        self.root.destroy()
        IntroPage.__init__(self, goIndex=self.goIndex)

    # 省内路线规划页
    def goProvRoute(self):
        self.root.destroy()
        ProvRoute.__init__(self, goIndex=self.goIndex)

    # 跨省路线规划页
    def goNationalRoute(self):
        self.root.destroy()
        NationalRoute.__init__(self, goIndex=self.goIndex)


if __name__ == '__main__':
    Control()
