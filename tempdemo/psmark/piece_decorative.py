import configparser
from win32com.client import Dispatch
from JSX2 import dxf3_jscode
from JSX3 import dxf2_jscode
from JSX1 import dxf_jscode
from JSX4 import dxf4_jscode
from JSX5 import dxf5_jscode
from JSX6 import dxf6_jscode
from JSX7 import dxf7_jscode
from JSX8 import dxf8_jscode
from JSX9 import dxf9_jscode
from JSX10 import dxf10_jscode
from JSX11 import dxf11_jscode
from JSX12 import dxf12_jscode
from JSX13 import dxf13_jscode
from JSX14 import dxf14_jscode
from JSX15 import dxf15_jscode
from JSX16 import dxf16_jscode
from JSX17 import dxf17_jscode
from JSX18 import dxf18_jscode
from JSX19 import dxf19_jscode
from JSX20 import dxf20_jscode
from JSX21 import dxf21_jscode
from JSX22 import dxf22_jscode
from JSX23 import dxf23_jscode
from JSX24 import dxf24_jscode
from JSX25 import dxf25_jscode
from JSX26 import dxf26_jscode
from JSX27 import dxf27_jscode


psapp = None
aiapp = None
config = configparser.ConfigParser()
config.read('程序配置.ini', encoding='utf-8')
PSname = config.get('程序配置', 'ps应用名')

# from datetime import datetime  # 引入datetime，获取当前日期
# import sys  # 引用退出程序方法
#
# ## 逻辑实现
# d1 = datetime.now().date()
# d2 = pd.to_datetime('2023-9-15').date()
#
# print("当前日期:", d1)
# print("限制日期:", d2)
#
# if d1 > d2:
#     print('软件已过期，请联系作者！')
#     sys.exit()
def PS_DXF_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf_jscode + '\n' + funcode)
    return res




def PS_DXF2_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf2_jscode + '\n' + funcode)
    return res


def PS_DXF3_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf3_jscode + '\n' + funcode)
    return res

def PS_DXF4_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf4_jscode + '\n' + funcode)
    return res


def PS_DXF5_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf5_jscode + '\n' + funcode)
    return res

def PS_DXF6_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf6_jscode + '\n' + funcode)
    return res


def PS_DXF7_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf7_jscode + '\n' + funcode)
    return res

def PS_DXF8_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf8_jscode + '\n' + funcode)
    return res

def PS_DXF9_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf9_jscode + '\n' + funcode)
    return res



def PS_DXF10_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf10_jscode + '\n' + funcode)
    return res


def PS_DXF11_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf11_jscode + '\n' + funcode)
    return res

def PS_DXF12_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf12_jscode + '\n' + funcode)
    return res


def PS_DXF13_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf13_jscode + '\n' + funcode)
    return res

def PS_DXF14_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf14_jscode + '\n' + funcode)
    return res



def PS_DXF15_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf15_jscode + '\n' + funcode)
    return res


def PS_DXF16_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf16_jscode + '\n' + funcode)
    return res

def PS_DXF17_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf17_jscode + '\n' + funcode)
    return res



def PS_DXF18_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf18_jscode + '\n' + funcode)
    return res


def PS_DXF19_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf19_jscode + '\n' + funcode)
    return res


def PS_DXF20_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf20_jscode + '\n' + funcode)
    return res



def PS_DXF21_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf21_jscode + '\n' + funcode)
    return res


def PS_DXF22_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf22_jscode + '\n' + funcode)
    return res



def PS_DXF23_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf23_jscode + '\n' + funcode)
    return res

def PS_DXF24_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf24_jscode + '\n' + funcode)
    return res

def PS_DXF25_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf25_jscode + '\n' + funcode)
    return res


def PS_DXF26_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf26_jscode + '\n' + funcode)
    return res

def PS_DXF27_jscode_fun(funcode):
    print(funcode)
    global psapp
    if psapp is None:
        psapp = Dispatch(PSname)
    res = psapp.DoJavaScript(dxf27_jscode + '\n' + funcode)
    return res



def main():



        pass

if __name__ == '__main__':
    main()
