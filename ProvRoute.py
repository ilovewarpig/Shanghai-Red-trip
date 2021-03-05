# 省内出游页面
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
from pulp import *
import re
import copy
from ttkthemes import ThemedStyle
import ttkthemes


class ProvRoute(object):
    def __init__(self, goIndex):
        # 初始化
        # 景点基本信息，包含出发点
        self.df = pd.read_csv('spotsF_test.csv', encoding='gbk')
        self.total_spots = 16
        self.starting_point = 16
        self.clicked_pro = [0 for i in range(self.total_spots)]
        self.table = pd.read_csv('cost_matrix.csv')
        # 开销矩阵，包含出发点
        self.cost_matrix = self.table.iloc[list(range(self.total_spots)), list(range(self.total_spots))].copy()
        self.spots_name_pro = list(self.df['name'][:self.total_spots])
        # 边框记录
        self.bolds = []
        # 返回函数
        self.goIndex = goIndex
        # 创建主窗口
        self.create_main_window_pro()
        # 创建子窗口1
        self.creat_subwindow_pro()
        # 创建子窗口2
        self.creat_subwindow_pro2()
        # 创建子窗口3
        self.creat_subwindow_pro3()
        # 主循环
        self.root.mainloop()

    # 回到目录
    def bf_goindex(self):
        self.goIndex()

    # 设置图形按钮外框的颜色
    def set_color_bold(self, num, widget_id):
        print(widget_id, type(widget_id))

        # 输入 被按控件的索引
        # 输出 哪些控件被按下
        if self.clicked_pro[num] == 0:
            # print(str(num), '被按下')
            self.clicked_pro[num] = 1
            self.my_canvas.itemconfig(widget_id, outline='#8B0000')
        else:
            # print(str(num), '被松开')
            self.clicked_pro[num] = 0
            self.my_canvas.itemconfig(widget_id, outline='white')
        # print('已经按下了%d个按钮'%np.array(self.clicked_pro).sum())

    # 重置一切选择
    def reset_choice(self):
        # 重置按键和边框颜色
        # 边框颜色初始化
        for index, item in enumerate(self.clicked_pro):
            if item:
                self.my_canvas.itemconfig(self.bolds[index], outline='white')
        # 按键记录初始化
        self.clicked_pro = [0 for i in range(self.total_spots)]
        self.output_text.delete(0.0, END)

    # 读取景点基本信息（名称、地址、简介......）
    def load_pro_df(self):
        # 导入景点基本信息（默认上海市）
        self.pro_df_address = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                           filetypes=(("CSV Files", "*.csv"),))
        self.df = pd.read_csv(self.pro_df_address, encoding='gbk')
        self.city_label.config(text=self.df['city'][0])
        # self.loadflag1.config(text=os.path.basename(self.address_filename))
        print(os.path.basename(self.pro_df_address))
        self.total_spots = int(simpledialog.askstring(title='获取信息', prompt='请输入景点的数量(不包括出发点)：'))
        self.clicked_pro = [0 for i in range(self.total_spots)]
        # print(self.total_spots)
        self.spots_name_pro = list(self.df['name'])
        # print(self.spots_name_pro)
        self.creat_subwindow_pro2()
        self.creat_subwindow_pro()
        self.reset_choice()

    # 载入邻接矩阵，邻接矩阵的大小一定要和景点信息CSV中吻合
    def load_cost_matrix_df(self):
        # 导入cost matrix（默认上海市）
        self.pro_df_cost = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                           filetypes=(("CSV Files", "*.csv"),))
        self.table = pd.read_csv(self.pro_df_cost, encoding='gbk')
        # self.loadflag1.config(text=os.path.basename(self.address_filename))
        print(os.path.basename(self.pro_df_cost))
        messagebox.showinfo(title='注意', message='开销矩阵一定要和景点基本信息相对应！')

    # 路线规划
    def tsp(self, cost, basic_info):
        # cost: 距离矩阵
        # basic_info:基本信息
        table = cost
        duration = list(basic_info['duration'])

        # 实例化问题
        row = table.shape[0]
        col = table.shape[1]
        prob = LpProblem('Transportation_Problem', sense=LpMinimize)

        # 路线决策变量，0-1
        var = [[LpVariable(f'x{i}_{j}', lowBound=0, upBound=1, cat=LpInteger) for j in range(col)] for i in range(row)]
        # 节点顺序变量
        ui_tag = 'u_%s'
        ui = np.array([LpVariable(ui_tag % (i), lowBound=0, cat='Integer') for i in range(col)])

        # 目标函数
        t = np.array(table)
        prob += lpSum(var[i][j] * (t[i][j] + duration[j]) for i in range(row) for j in range(col) if i != j)

        # 约束条件
        # 遍历每一个点
        prob += lpSum([var[i][j] for i in range(row) for j in range(col)]) == col
        # 不允许两点间折返
        for i in range(row):
            for j in range(col):
                prob += var[i][j] + var[j][i] <= 1
        # 起点约束：以最后一个点为起点
        prob += lpSum([var[col - 1][j] for j in range(row)]) == 1
        # 终点约束：以最后一个点为起终点
        prob += lpSum([var[j][col - 1] for j in range(row)]) == 1
        # 出度约束，每点出度不大于2
        for i in range(row):
            prob += lpSum([var[i][j] for j in range(col)]) <= 1
        # 入度约束，每点入度不大于2
        for j in range(row):
            prob += lpSum([var[i][j] for i in range(row)]) <= 1
        # 防止生成子回路
        for i in range(1, col):
            for j in range(1, col):
                if i != j:
                    prob += (
                            ui[i] - ui[j] + col * var[i][j] <= col - 1
                    )

        prob.solve()
        result = value(prob.objective)
        path = pd.DataFrame([[value(var[i][j]) for j in range(col)] for i in range(row)])
        # print('最短时间: ', result)
        self.output_text.insert(index=INSERT, chars='最短时间'+str(result)+'分钟')

        # 生成顺序路线
        display = False
        cycle_ods = {}
        for varb in prob.variables():
            if varb.name.startswith(ui_tag[0]):
                continue
            if varb.varValue > 0:
                if display:
                    self.output_text.insert(index=INSERT, chars="%s: %s" % (varb.name, varb.varValue))
                od = varb.name.split("_")
                o, d = od[0], od[1]
                cycle_ods[int(re.findall('\d+', o)[0])] = int(d)
        if display:
            self.output_text.insert(index=INSERT, chars="Status: %s" % LpStatus[prob.status])

        tour_pairs = []
        for origin in range(col):
            tour_pairs.append([])
            if origin == 0:
                next_origin = cycle_ods[origin]
                tour_pairs[origin].append(origin)
                tour_pairs[origin].append(next_origin)
                continue
            tour_pairs[origin].append(next_origin)
            next_origin = cycle_ods[next_origin]
            tour_pairs[origin].append(next_origin)
        tour_pairs = {idx: tp for idx, tp in enumerate(tour_pairs)}

        for pairs in range(len(tour_pairs)):
            self.output_text.insert(index=INSERT, chars='\n'+basic_info['name'][tour_pairs[pairs][0]]+ '->'+ basic_info['name'][tour_pairs[pairs][1]])
        return result

    # 更新输出窗口中的路线规划结果
    def text_update(self):
        test_text = 'test'
        cluster4 = []
        # self.output_text.insert(index=INSERT, chars='\n'+test_text)
        cluster4.append(self.starting_point)
        for index, item in enumerate(self.clicked_pro):
            if item == 1:
                cluster4.append(index)
        t4 = self.table.iloc[cluster4, cluster4].copy()
        df_t4 = self.df.iloc[cluster4].copy()
        df_t4.reset_index(inplace=True)
        time_cost = self.tsp(t4, df_t4)
        self.output_text.insert(index=INSERT, chars='\n'+'最短时间为'+str(time_cost)+'分钟，共'+str(time_cost / 60)+'小时')
        self.output_text.insert(index=INSERT,chars='\n--------------------------------------------------\n')

    # 切换出发点。默认包含上海地区教育部直管的高校
    def change_starting_point(self):
        chosen = self.city_choosen.get()
        # print(list(self.df['name']).index(chosen))
        self.starting_point = list(self.df['name']).index(chosen)

    # 创建主窗口
    def create_main_window_pro(self):
        self.root = ttkthemes.ThemedTk(theme='adapta')# Tk()
        self.width = 800
        self.height = 610
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (
        self.width, self.height, (screen_width - self.width) / 2, (screen_height - self.height) / 2)
        self.root.geometry(align_str)
        self.root.resizable(False, False)

    # 创建子窗口1的部件
    def creat_subwindow_pro(self):
        self.input_frame1_pro = ttk.LabelFrame(self.root, text='数据导入', width=400, height=200)
        self.input_frame1_pro.grid(column=0, row=0, columnspan=1, rowspan=1, padx=6)
        # 窗体控件-输入
        label1 = ttk.Label(self.input_frame1_pro, text='省内旅游')
        label2 = ttk.Label(self.input_frame1_pro, text='当前城市: ')
        self.city_label = ttk.Label(self.input_frame1_pro, text=self.df['city'][0])
        label4 = ttk.Label(self.input_frame1_pro, text='出行方式')
        conform_start = ttk.Button(self.input_frame1_pro, text="确定起点", command=self.change_starting_point)
        chose_start = ttk.Label(self.input_frame1_pro, text="请先选择起点")
        n = StringVar()
        self.city_choosen = ttk.Combobox(self.input_frame1_pro, width=26,textvariable=n)
        # print(self.total_spots, list(self.df['name'])[self.total_spots:])
        self.city_choosen['values'] = list(self.df['name'])[self.total_spots:]
        self.city_choosen.current(0)

        import_spot_info_button = ttk.Button(self.input_frame1_pro, text="导入场馆信息", command=self.load_pro_df)
        import_cost_matrix_button = ttk.Button(self.input_frame1_pro, text="导入开销矩阵", command=self.load_cost_matrix_df)
        travel_style = StringVar()

        # 布局 - 输入
        my_padx = 15
        label1.grid(column=0, row=0, padx=my_padx)
        label2.grid(column=2, row=0, padx=my_padx)
        self.city_label.grid(column=3, row=0, padx=my_padx)
        # label4.grid(column=0, row=2, padx=my_padx)
        import_spot_info_button.grid(column=2, row=2, columnspan=2, padx=my_padx, sticky=E)
        import_cost_matrix_button.grid(column=2, row=3, columnspan=2, padx=my_padx, sticky=E)
        chose_start.grid(column=0, row=1, padx=my_padx, pady=6)
        self.city_choosen.grid(column=0, row=2, columnspan=3, rowspan=2, padx=my_padx)
        conform_start.grid(column=3, row=1, columnspan=1, padx=my_padx)

    # 创建子窗口2的部件
    def creat_subwindow_pro2(self):
        # 创建子窗体2
        global myimg_pro
        global imgs_pro
        imgs_pro = []
        for i in range(self.total_spots):
            try:
                file_path = 'pics/' + self.df['path'][i]
                # print(file_path)
                tpt = ImageTk.PhotoImage(Image.open(file_path).resize((72, 72)))
            except:
                tpt = ImageTk.PhotoImage(Image.open('SAMPLE.png').resize((72, 72)))
            imgs_pro.append(tpt)
        myimg_pro = ImageTk.PhotoImage(Image.open('SAMPLE.png').resize((72, 72)))
        self.select_frame_pro = ttk.LabelFrame(self.root, text='场馆选择', width=400, height=400)
        self.select_frame_pro.grid(column=0, row=1, columnspan=1, rowspan=2, padx=6, pady=3)
        # 窗体控件-选择
        img_width = 72
        img_pad_x = 20
        img_pad_y = 20
        start_x = 20
        start_y = 10
        current_x = start_x
        current_y = start_y
        sentence_pad = 3
        self.my_canvas = Canvas(self.select_frame_pro, width=390, height=390)
        for item in range(self.total_spots):
            # 图片
            temp = self.my_canvas.create_image(current_x, current_y, image=imgs_pro[item], anchor='nw')
            # 场馆标题
            self.my_canvas.create_text(current_x, current_y + sentence_pad + img_width, text=self.spots_name_pro[item][:6],
                                       anchor='nw')
            # 边框
            bold = self.my_canvas.create_rectangle(current_x - 3, current_y - 3, current_x + img_width + 3,
                                                   current_y + img_width + 3, fill='', outline='white', width=2)
            self.bolds.append(bold)
            # 绑定按钮
            self.my_canvas.tag_bind(temp, "<Button-1>",
                                    lambda event, num=item, widget_id=bold: self.set_color_bold(num, widget_id))
            # 满4个换行
            if (item + 1) % 4 != 0:
                current_x = current_x + img_width + img_pad_x
            else:
                current_x = start_x
                current_y = current_y + img_width + img_pad_y + sentence_pad
        self.my_canvas.grid(column=0, row=0)

    # 创建子窗口3的部件
    def creat_subwindow_pro3(self):
        # 创建子窗体3
        self.output_frame_pro = ttk.LabelFrame(self.root, text='路线输出', width=400, height=600, padding=(3, 3, 3, 3))
        self.output_frame_pro.grid(column=1, row=0, columnspan=1, rowspan=3, padx=6, pady=3)
        return_button = ttk.Button(self.output_frame_pro, text="回到目录", width=7, command=self.goIndex)
        reselect_button = ttk.Button(self.output_frame_pro, text="重新选择", width=7, command=self.reset_choice)
        entry = ttk.Button(self.output_frame_pro, text="查询路线", width=7, command=self.text_update)
        self.output_text = Text(self.output_frame_pro, width=50, height=41)
        entry.grid(column=1, row=0, pady=6, sticky=(N, S, E, W))
        return_button.grid(column=2, row=0, pady=6, sticky=(N, S, E, W))
        reselect_button.grid(column=3, row=0, pady=6, sticky=(N, S, E, W))
        self.output_text.grid(column=0, row=1, columnspan=4, rowspan=1)


if __name__ == '__main__':
    root = ttkthemes.ThemedTk(theme='adapta')# Tk()
    root.resizable(False, False)
    ProvRoute(None)
    root.mainloop()