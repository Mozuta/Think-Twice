import tkinter as tk
from tkinter import filedialog
import os
import shutil
from glob import glob


def mycopyfile(srcfile, dstpath):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + fname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + fname))

def picselect():
    # 获取选择文件路径
    # 实例化
    root = tk.Tk()
    root.withdraw()

    # 获取文件夹路径
    f_path = filedialog.askopenfilename(title='Select the picture file', filetypes=[('PNG', '*.png'), ('JPG', '*.jpg')],
                                        initialdir='C:\\Windows')
    print('\n获取的文件地址：', f_path)

    index = f_path.rfind('/') + 1
    pic_path = 'assets/pictures/puzzle/' + f_path[index:]
    print(pic_path)
    # srcfile 需要复制、移动的文件
    # dstpath 目的地址
    src_dir = './'
    dst_dir = './assets/pictures/puzzle/'  # 目的路径记得加斜杠
    src_file_list = glob(f_path)  # glob获得路径下所有文件，可根据需要修改
    for srcfile in src_file_list:
        mycopyfile(srcfile, dst_dir)  # 复制文件

