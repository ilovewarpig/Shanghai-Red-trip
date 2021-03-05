# 数据工作台
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas as pd
import string
import numpy as np
from pulp import *
import requests
import json
from urllib.request import urlopen
import traceback
import ttkthemes

AK = # 调用百度API的个人验证码，为保护隐私已删去。请自行申请百度API的AK码 申请流程可参考 https://blog.csdn.net/qq_27512271/article/details/82994240
class NationalRoute(object):
    # 初始化，默认上海16个景点生成界面
    def __init__(self, goIndex):
        self.goIndex = goIndex

        # 创建主窗口
        self.create_main_window()
        # Frame布局
        self.creat_sub_frames()
        # 窗体1 部件布局、事件绑定
        self.create_widgets_sf1()
        # 窗体2 部件布局、事件绑定
        self.create_widgets_sf2()
        # 窗体3 部件布局、事件绑定
        self.create_widgets_sf3()
        self.root.mainloop()

    # 返回目录
    def bf_goindex(self):
        self.goIndex()

    # 创建labelFrame 子窗口布局
    def creat_sub_frames(self):
        # 创建
        self.frame1 = ttk.LabelFrame(self.root, text='使用示例', width=260, height=590, padding=(3, 3, 3, 3))
        self.frame2 = ttk.LabelFrame(self.root, text='获得场馆经纬度', width=260, height=590)
        self.frame3 = ttk.LabelFrame(self.root, text='计算邻接矩阵', width=260, height=590, padding=(3, 3, 3, 3))
        # 布局
        self.frame1.grid(column=0, row=0, columnspan=1, rowspan=1, padx=3, pady=3)
        self.frame2.grid(column=1, row=0, columnspan=1, rowspan=1, padx=3, pady=3)
        self.frame3.grid(column=2, row=0, columnspan=1, rowspan=1, padx=3, pady=3)

    # 在第一个子窗口(示例)中加载部件
    def create_widgets_sf1(self):
        # 使用示例子窗口
        global flow_chart
        go_back = ttk.Button(self.frame1, text='回到目录', command=self.goIndex)

        # 创建
        lb1 = ttk.Label(self.frame1, text='[说明]', width=6)
        lb2 = ttk.Label(self.frame1, text='[数据工作台的使用流程]', width=20)

        text1 = Text(self.frame1, width=35, height=10)
        text1.insert('1.0', '数据工作台能够帮助使用者导入自己的场馆信息。\n\n使用者只需要提供包含场馆名称、地址、所在城市和'
                            '预计游览时间的CSV文件即可在数据工作台的帮助下在和程序同一文件目录下生成经纬度数据和邻接矩阵'
                            '。\n回到省内规划界面分别导入新生成的两个CSV文件即可实现数据的替换。')
        # flow_chart = ImageTk.PhotoImage(Image.open('SAMPLE.png').resize((230, 320)))
        flow_chart = ImageTk.PhotoImage(Image.open('pics/数据导入流程.png').resize((230, 320)))
        img_labe = ttk.Label(self.frame1, image=flow_chart)

        # 布局
        my_pady = 3
        go_back.grid(row=0, column=5, pady=my_pady, sticky=W)
        lb1.grid(row=1, column=0, pady=my_pady, sticky=W)
        text1.grid(row=2, column=0, rowspan=5, columnspan=6, pady=my_pady)
        lb2.grid(row=7, column=0, pady=my_pady)
        img_labe.grid(row=8, column=0, rowspan=4, columnspan=6, pady=my_pady)

    # 在第二个子窗口(获取经纬度)中加载部件
    def create_widgets_sf2(self):
        # 提取名称地址并转换到经纬度的窗口
        global input_img1
        global output_img1
        # 创建
        load_spot = ttk.Button(self.frame2, text='导入场馆csv', command=self.upload_csv_file)
        get_il = ttk.Button(self.frame2, text='获取经纬度', command=self.get_lng_lat)
        self.loadflag1 = ttk.Label(self.frame2, text='no file...', width=10)
        lb1 = ttk.Label(self.frame2, text='[说明]', width=6)
        lb2 = ttk.Label(self.frame2, text='[输入示例]', width=10)
        lb3 = ttk.Label(self.frame2, text='[输出示例]', width=10)

        text1 = Text(self.frame2, width=35, height=10)
        text1.insert('1.0', '需要先填写场馆csv文件，至少包括：名称、地址、所在省市和预计游览时间，列名请参照输入示例。暂时只支持GBK编码,最多'
                            '支持26个场馆。\n\n点击导入文件按钮可以载入场馆csv，点击获取经纬度后会在同文件目录下生成一个‘经纬度.csv’文件，'
                            '该文件可作为下一步求邻接矩阵的输入数据')
        input_img1 = ImageTk.PhotoImage(Image.open('pics/输入示例1.png').resize((250, 145)))
        img_label = ttk.Label(self.frame2, image=input_img1)
        output_img1 = ImageTk.PhotoImage(Image.open('pics/输出示例1.png').resize((250, 145)))
        img_labe2 = ttk.Label(self.frame2, image=output_img1)

        # 布局
        my_pady = 3
        self.loadflag1.grid(row=0, column=0, pady=my_pady)
        load_spot.grid(row=0, column=4, pady=my_pady)
        get_il.grid(row=0, column=5, pady=my_pady)
        lb1.grid(row=1, column=0, pady=my_pady, sticky=W)
        text1.grid(row=2, column=0, rowspan=5, columnspan=6, pady=my_pady)
        lb2.grid(row=7, column=0, pady=my_pady)
        img_label.grid(row=8, column=0, rowspan=4, columnspan=6, pady=my_pady)
        lb3.grid(row=13, column=0, pady=my_pady)
        img_labe2.grid(row=14, column=0, rowspan=4, columnspan=6, pady=my_pady)

    # 在第三个子窗口(获取邻接矩阵)中加载部件
    def create_widgets_sf3(self):
        # 提取名经纬度并转换到cost matrix的窗口
        global input_img2
        global output_img2
        # 创建
        load_spot = ttk.Button(self.frame3, text='导入经纬度', command=self.upload_il_file)
        get_il = ttk.Button(self.frame3, text='获取邻接矩阵', command=self.get_cost_matrix)
        self.loadflag2 = ttk.Label(self.frame3, text='no file...', width=10)
        lb1 = ttk.Label(self.frame3, text='[说明]', width=6)
        lb2 = ttk.Label(self.frame3, text='[输入示例]', width=10)
        lb3 = ttk.Label(self.frame3, text='[输出示例]', width=10)

        text1 = Text(self.frame3, width=35, height=10)
        text1.insert('1.0', '导入场馆的经纬度暂时只支持GBK编码，列名参照输入示例。如果是上一步生成的经纬度csv文件，可直接使用。\n'
                            '\n点击计算邻接矩阵按钮后会在同文件目录下生成一个‘cost_matrix.csv’文件，'
                            '回到省内路线规划界面，分别导入经纬度.csv和cost_matrix文件即可完成数据的替换')
        input_img2 = ImageTk.PhotoImage(Image.open('pics/输出示例1.png').resize((250, 145)))
        img_label = ttk.Label(self.frame3, image=input_img1)
        output_img2 = ImageTk.PhotoImage(Image.open('pics/输出示例2.png').resize((250, 145)))
        img_labe2 = ttk.Label(self.frame3, image=output_img1)

        # 布局
        my_pady = 3
        self.loadflag2.grid(row=0, column=0, pady=my_pady)
        load_spot.grid(row=0, column=4, pady=my_pady)
        get_il.grid(row=0, column=5, pady=my_pady)
        lb1.grid(row=1, column=0, pady=my_pady, sticky=W)
        text1.grid(row=2, column=0, rowspan=5, columnspan=6, pady=my_pady)
        lb2.grid(row=7, column=0, pady=my_pady)
        img_label.grid(row=8, column=0, rowspan=4, columnspan=6, pady=my_pady)
        lb3.grid(row=13, column=0, pady=my_pady)
        img_labe2.grid(row=14, column=0, rowspan=4, columnspan=6, pady=my_pady)

    # 上传地理信息csv文件
    def upload_csv_file(self):
        self.address_filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes= (("CSV Files","*.csv"),))

        # dft = pd.read_csv(filename, encoding='gbk')
        self.loadflag1.config(text=os.path.basename(self.address_filename))
        print(os.path.basename(self.address_filename))

    # 将地址转换为经纬度
    # 参考来源：https://blog.csdn.net/qq_35408030 参考作者：wild_orange 非常感谢！
    def Pos2Coord(self, name, city='上海市'):
        # 地址 - > 经纬度
        url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&city=%s&output=json&ak=%s' % (name, city, AK)
        res = requests.get(url)
        if res.status_code == 200:
            val = res.json()
            if val['status'] == 0:
                retVal = {'lng': val['result']['location']['lng'], 'lat': val['result']['location']['lat'], \
                          'conf': val['result']['confidence'], 'comp': val['result']['comprehension'],
                          'level': val['result']['level']}
            else:
                retVal = None
            return retVal
        else:
            print('无法获取%s经纬度' % name)

    # 将经纬度转换为地址
    # 参考来源：https://blog.csdn.net/qq_35408030 参考作者：wild_orange 非常感谢！
    def Coord2Pos(self, lng, lat, town='true'):
        # 经纬度 - > 地址
        url = 'http://api.map.baidu.com/reverse_geocoding/v3/?output=json&ak=%s&location=%s,%s&extensions_town=%s' % (
        AK, lat, lng, town)
        res = requests.get(url)
        if res.status_code == 200:
            val = res.json()
            if val['status'] == 0:
                val = val['result']
                retVal = {'address': val['formatted_address'], 'province': val['addressComponent']['province'], \
                          'city': val['addressComponent']['city'], 'district': val['addressComponent']['district'], \
                          'town': val['addressComponent']['town'], 'adcode': val['addressComponent']['adcode'],
                          'town_code': val['addressComponent']['town_code']}
            else:
                retVal = None
            return retVal
        else:
            print('无法获取(%s,%s)的地理信息！' % (lat, lng))

    # 读取景点地址csv信息
    def get_lng_lat(self):
        # 读取名称-地址csv
        my_str = StringVar()
        try :
            print(self.address_filename)
            try:
                df_load = pd.read_csv(self.address_filename, encoding='gbk')
                spot = []
                lngs = []
                lats = []
                spot_address = list(df_load['address'])
                spot_name = list(df_load['name'])
                duration = list(df_load['duration'])
                for (address, name) in zip(spot_address, spot_name):
                    val = self.Pos2Coord(address)
                    spot.append(name)
                    lngs.append(format(val['lng'], '.6f'))
                    lats.append(format(val['lat'], '.6f'))
                df2 = pd.DataFrame({'name': spot, 'address':spot_address, 'duration':duration, 'lng': lngs, 'lat': lats})
                df2.to_csv('经纬度.csv', index=False, encoding='gbk')
                my_str.set('操作成功。文件已保存在 %s /经纬度.csv'%(self.address_filename))

            except Exception as e:
                print(str(e))
                traceback.print_exc()
                my_str.set('操作失败。请仔细阅读说明和输入示例，确保文件为csv格式；编码方式为gbk；包含name、address和city列')

        except Exception as e:
            my_str.set('操作失败。请先导入地址csv文件！')
        messagebox.showinfo(title='操作结果', message=my_str.get())

    # 计算cost matrix
    # 公交换乘时间、价格、距离
    # 参考来源：https://blog.csdn.net/qq_35408030 参考作者：wild_orange 非常感谢！
    def trainmit(self, origin_lat, origin_lng, destination_lat, destination_lng, tactics_incity=4):
        '''
        origin_lat: 出发地纬度
        origin_lng: 出发地经度
        destination_lat: 目的地纬度
        destination_lng: 目的地经度
        tactics_incity: 换乘策略。0 推荐 1 少换乘 2 少步行 3 不坐地铁 4 时间短 5 地铁优先
        '''
        origin_lat = origin_lat
        origin_lng = origin_lng
        destination_lat = destination_lat
        destination_lng = destination_lng

        url_trainmit = r"http://api.map.baidu.com/direction/v2/transit?origin={},{}&destination={},{}&tactics_incity={}&ak={}".format(
            origin_lat, origin_lng, destination_lat, destination_lng, tactics_incity, AK)
        result_trainmit = json.loads(urlopen(url_trainmit).read())  # json转dict
        status_trainmit = result_trainmit['status']
        # print(status_trainmit)
        if status_trainmit == 0:
            try:
                distance_trainmit = result_trainmit['result']['routes'][0]['distance']
                distance_time = result_trainmit['result']['routes'][0]['duration']
                price = result_trainmit['result']['routes'][0]['price']
                print(price, distance_trainmit, distance_time / 60)
            except Exception as e:
                print('距离过短')
                distance_trainmit = result_trainmit['result']['taxi']['distance']
                distance_time = result_trainmit['result']['taxi']['duration']
                price = result_trainmit['result']['taxi']['detail'][0]['total_price']
                print(price, distance_trainmit, distance_time / 60)
            return (price, distance_trainmit, distance_time / 60)
        else:
            print('error: ', result_trainmit['message'])

    # 上传经纬度CSV
    def upload_il_file(self):
        self.il_filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                           filetypes=(("CSV Files", "*.csv"),))
        # dft = pd.read_csv(filename, encoding='gbk')
        self.loadflag2.config(text=os.path.basename(self.il_filename))
        print(os.path.basename(self.il_filename))

    # 读取经纬度CSV
    def get_cost_matrix(self):
        # 读取经纬度文件
        my_str = StringVar()
        try:
            print(self.il_filename)
            try:
                df_load = pd.read_csv(self.il_filename, encoding='gbk')
                length = len(df_load)
                if length > 26:
                    my_str.set('操作失败。最多26个地点,请重新导入地址csv文件！')
                    messagebox.showinfo(title='操作结果', message=my_str.get())
                    return
                my_str.set('本操作可能会等上几分钟')
                messagebox.showinfo(title='通知', message=my_str.get())
                table = pd.DataFrame(np.array([[0] * length] * length), columns=[i for i in string.ascii_lowercase[:length]])
                for item2 in range(length):
                    for item in range(length):
                        print(item2, item)
                        if item2 == item:
                            continue
                        val = self.trainmit(df_load['lat'][item2], df_load['lng'][item2], df_load['lat'][item], df_load['lng'][item])
                        table[table.columns[item]][item2] = val[2]
                for item2 in range(length):
                    for item in range(length):
                        if item2 == item:
                            continue
                        if table[table.columns[item]][item2] < table[table.columns[item2]][item]:
                            table[table.columns[item2]][item] = table[table.columns[item]][item2]
                        else:
                            table[table.columns[item]][item2] = table[table.columns[item2]][item]
                messagebox.showinfo(title='提示', message='计算完成，请输入要保存的文件名(含后缀)')
                filename = filedialog.asksaveasfilename(filetypes=(("CSV Files", "*.csv"),))
                print(os.path.basename(filename))
                while os.path.basename(filename) == 'cost_matrix.csv':
                    messagebox.showinfo(title='提示', message='请输入其他文件名')
                    filename = filedialog.asksaveasfilename(filetypes=(("CSV Files", "*.csv"),))
                table.to_csv(filename, index=False, encoding='gbk')
                my_str.set('操作成功。文件已保存在 %s'%filename)

            except Exception as e:
                print(str(e))
                traceback.print_exc()
                my_str.set('操作失败。请仔细阅读说明和输入示例，确保文件为csv格式；编码方式为gbk；包含name、address、city和duration列;确保目标文件并未打开')

        except Exception as e:
            my_str.set('操作失败。请先导入地址csv文件！')
        messagebox.showinfo(title='操作结果', message=my_str.get())


if __name__ == '__main__':
    root = ttkthemes.ThemedTk(theme='adapta')# Tk()
    root.resizable(False, False)
    # style = ThemedStyle(root)
    # style.set_theme('Adapta')
    ttkthemes.themed_style.ThemedStyle(theme="adapta")

    NationalRoute(None)
    root.mainloop()