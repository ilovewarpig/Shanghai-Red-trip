# 场馆介绍页面
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import pandas as pd
import ttkthemes


class IntroPage(object):

    def __init__(self, goIndex):
        # 初始化
        # 景点基本信息，包含出发点
        self.df = pd.read_csv('basic_information.csv', encoding='gbk')
        self.total_spots = 16
        self.clicked_pro = [0 for i in range(self.total_spots)]
        self.table = pd.read_csv('mix_time.csv')
        # 开销矩阵，包含出发点
        self.cost_matrix = self.table.iloc[list(range(self.total_spots)), list(range(self.total_spots))].copy()
        self.spots_name = list(self.df['name'][:self.total_spots])
        self.select_spots = []
        self.bolds = []
        self.clicked = [0 for i in range(self.total_spots)]
        self.clicked[0] = 1
        self.select_style = 0
        self.style_dict = {0 : [i for i in range(self.total_spots)],
                           1 : [1, 3, 4, 8, 12, 15],
                           2 : [3, 6],
                           3 : [0, 6, 10, 11],
                           4 : [2, 5, 7, 9, 14],
                           5 : [4, 8, 12, 15],
                           6 : [6, 13],
                           7 : [5, 7, 9, 14],
                           8 : [1, 2]
                           }
        # 创建主窗口
        self.create_main_window()
        # Frame布局
        self.creat_frames()
        # 窗体1 部件布局、事件绑定
        self.create_widgets_f1()
        # 窗体2 部件布局、事件绑定
        self.create_widgets_f2()
        # 窗体3 部件布局、事件绑定
        self.create_widgets_f3()
        # 窗体4 部件布局、事件绑定
        self.create_widgets_f4()
        self.root.mainloop()

    # 回到目录
    def bf_goindex(self):
        self.goIndex()

    # 创建主窗口
    def create_main_window(self):
        self.root = ttkthemes.ThemedTk(theme='adapta')# Tk()
        width = 800
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (width, height, (screen_width - width) / 2, (screen_height - height) / 2)
        self.root.geometry(align_str)
        self.root.resizable(False, False)

    # 创建4个子窗口
    def creat_frames(self):
        self.input_frame = ttk.LabelFrame(self.root, text='系列选择', width=400, height=200, padding=(3, 3, 3, 3))
        self.select_frame = ttk.LabelFrame(self.root, text='场馆选择', width=400, height=400)
        self.output_up_frame = ttk.LabelFrame(self.root, text='基本信息', width=400, height=100, padding=(3, 3, 3, 3))
        self.output_down_frame = ttk.LabelFrame(self.root, text='场馆简介', width=400, height=500, padding=(3, 3, 3, 3))

        self.input_frame.grid(column=0, row=0, columnspan=1, rowspan=2, padx=3, pady=3)
        self.select_frame.grid(column=0, row=2, columnspan=1, rowspan=4, padx=3, pady=3)
        self.output_up_frame.grid(column=1, row=0, columnspan=1, rowspan=1, padx=3, pady=3)
        self.output_down_frame.grid(column=1, row=1, columnspan=1, rowspan=5, padx=3, pady=3)

    # 创建子窗口1的部件
    def create_widgets_f1(self):
        # 输入框 选择系列标签
        tags = ['爱国主义教育基地', '中共', '工人运动', '抗日战争', '人物类纪念馆', '人大', '青年学子', '革命', '地下活动']
        my_padx = 10
        for index, item in enumerate(tags):
            temp = ttk.Button(self.input_frame, text=item, command=lambda num=index: self.change_style(num))
            temp.grid(column=int(index/3), row=int(index%3), padx=my_padx, pady=5)

    # 切换景点系列
    def change_style(self, num):
        self.select_style = num
        # print('%d被按下'%self.select_style)
        self.bolds = []
        self.clicked = [0 for i in range(15)]
        self.create_widgets_f2()

    # 创建子窗口2的部件
    def create_widgets_f2(self):
        global imgs_pro
        imgs_pro = []
        # 读取场馆图片
        for i in range(self.total_spots):
            try:
                file_path = 'pics/' + self.df['path'][i]
                # print(file_path)
                tpt = ImageTk.PhotoImage(Image.open(file_path).resize((72, 72)))
            except:
                tpt = ImageTk.PhotoImage(Image.open('SAMPLE.png').resize((72, 72)))
            imgs_pro.append(tpt)
        # 选择框 显示 3 * 3的场馆图片，可点击选择
        self.myimg = ImageTk.PhotoImage(Image.open('SAMPLE.png').resize((72, 72)))
        img_width = 72
        img_pad_x = 20
        img_pad_y = 20
        start_x = 20
        start_y = 10
        current_x = start_x
        current_y = start_y
        sentence_pad = 3
        images = []
        self.my_canvas = Canvas(self.select_frame, width=390, height=390)
        # print(self.style_dict[self.select_style])
        for index, item in enumerate(self.style_dict[self.select_style]):
            # 图片
            temp = self.my_canvas.create_image(current_x, current_y, image=imgs_pro[item], anchor='nw')
            # 场馆标题
            self.my_canvas.create_text(current_x, current_y + sentence_pad + img_width, text=self.spots_name[item][:6],
                                       anchor='nw')
            # 边框
            bold = self.my_canvas.create_rectangle(current_x - 3, current_y - 3, current_x + img_width + 3,
                                                   current_y + img_width + 3, fill='', outline='white', width=2)
            self.bolds.append(bold)
            # 绑定按钮
            self.my_canvas.tag_bind(temp, "<Button-1>",
                                    lambda event, num=item, widget_id=bold: self.set_color_bold_intro(num, widget_id))

            # 满4个换行
            if (index + 1) % 4 != 0:
                current_x = current_x + img_width + img_pad_x
            else:
                current_x = start_x
                current_y = current_y + img_width + img_pad_y + sentence_pad
        self.my_canvas.grid(column=0, row=0)

    # 更新图片按钮的边框颜色
    def set_color_bold_intro(self, num, widget_id):
        # 更新按钮记录
        self.clicked = [0 for i in range(self.total_spots)]
        self.clicked[num] = 1
        # 更新边框颜色
        for item in self.bolds:
            self.my_canvas.itemconfig(item, outline='white')
        self.my_canvas.itemconfig(widget_id, outline='#8B0000')
        # print('已经按下了%d个按钮'%np.array(self.clicked).sum(), self.spots_name[num])
        # 更新场馆信息
        self.name_text.set(self.df.iloc[num]['name'])
        self.tag_text.set(self.df.iloc[num]['tag'])
        self.ticket_text.set(self.df.iloc[num]['ticket'])
        self.open_time_text.set(self.df.iloc[num]['opening_time'])
        self.tel_text.set(self.df.iloc[num]['tel'])
        self.address_text.set(self.df.iloc[num]['address'])

        self.spot_name.config(text=self.name_text.get())
        self.my_tag2.config(text=self.tag_text.get())
        self.ticket2.config(text=self.ticket_text.get())
        self.address2.config(text=self.address_text.get())
        self.tel2.config(text=self.tel_text.get())
        self.open_time2.config(text=self.open_time_text.get())
        # 更新场馆简介
        mystr = self.df.iloc[num]['intro']
        mystr = mystr.replace('<>', '\r\n\r\n')
        self.output_text.delete(0.0, END)
        self.output_text.insert(index=INSERT,chars=mystr)

    # 创建子窗口3的部件
    def create_widgets_f3(self):
        # 上方输出框
        self.name_text = StringVar()
        self.name_text.set('馆名')
        self.tag_text = StringVar()
        self.tag_text.set('标签')
        self.ticket_text = StringVar()
        self.ticket_text.set('门票')
        self.open_time_text = StringVar()
        self.open_time_text.set('开放时间')
        self.tel_text = StringVar()
        self.tel_text.set('电话')
        self.address_text = StringVar()
        self.address_text.set('地址')

        self.spot_name = ttk.Label(self.output_up_frame, text=self.name_text.get(), width=40)
        my_tag = ttk.Label(self.output_up_frame, text='标签', width=4)
        self.my_tag2 = ttk.Label(self.output_up_frame, text=self.tag_text.get(), width=20)
        ticket = ttk.Label(self.output_up_frame, text='门票', width=4)
        self.ticket2 = ttk.Label(self.output_up_frame, text=self.ticket_text.get(), width=4)
        open_time = ttk.Label(self.output_up_frame, text='开放时间', width=8)
        self.open_time2 = ttk.Label(self.output_up_frame, text=self.open_time_text.get(), width=27)
        tel = ttk.Label(self.output_up_frame, text='电话', width=4)
        self.tel2 = ttk.Label(self.output_up_frame, text=self.tel_text.get(), width=12)
        address = ttk.Label(self.output_up_frame, text='地址', width=4)
        self.address2 = ttk.Label(self.output_up_frame, text=self.address_text.get(), width=40)

        self.back_intro = ttk.Button(self.output_up_frame, text="回到目录", width=8, command=self.goIndex)
        self.load_csv_intro = ttk.Button(self.output_up_frame, text="导入景点", width=8, command=self.goIndex)

        my_padx = 1
        self.back_intro.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        self.load_csv_intro.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        self.spot_name.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W, padx=my_padx)
        my_tag.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        self.my_tag2.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        ticket.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        self.ticket2.grid(row=2, column=3, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        open_time.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        self.open_time2.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        tel.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        self.tel2.grid(row=3, column=3, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        address.grid(row=4, column=0, rowspan=1, columnspan=1, sticky=W, padx=my_padx)
        self.address2.grid(row=4, column=1, rowspan=1, columnspan=3, sticky=W, padx=my_padx)

    # 创建子窗口4的部件
    def create_widgets_f4(self):
        # 下方输出框
        self.output_text = Text(self.output_down_frame, width=50, height=30)
        self.output_text.grid(column=0, row=0)


if __name__ == '__main__':
    root = ttkthemes.ThemedTk(theme='adapta')# Tk()
    root.resizable(False, False)
    ttkthemes.themed_style.ThemedStyle(theme="adapta")

    IntroPage(None)
    root.mainloop()