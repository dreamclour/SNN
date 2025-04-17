# longlonglonglong
import tonic
import numpy as np
from brian2 import *
#####################################################################################################
# dt = np.dtype([('name','S20'),('age',np.int8),('marks','f4')])
# a = np.array([('yao',10.5,'22'),('yi',20.2,'10'),('ming',30.3,'9')], dtype = dt)
# print (dt.names)
# dtype就像建表一样，可以建立一张表，这个表里面的列的数据的类型都可以定义
#####################################################################################################
#####################################################################################################
# class NMNIST(object):
#   def __init__(self,name:str='yym',age:int='30'):
#     self.name=name
#     self.age=age
# a=NMNIST
#需要在创建__init__时赋值
# class NMNIST(object):
#   def __init__(self,name:str='yym',age:int='30'):
#     self.name=None
#     self.age=None
# a=NMNIST
#初始值是None
# class NMNIST(object):
#   def __init__(self,name:str,age:int):
#     self.name=name
#     self.age=age
# NMNIST.name='yym'
#需要赋值
#在def__init__上的参数没有赋值的话，需要在调用的时候赋值，或者在def__init__内部使用None，或者在创建参数时赋值
#####################################################################################################
#####################################################################################################
# t=[0,0,0,0,1,1,2,2,2,2,3,3,4,5,6,7,7,7,7,9]
# for r in t[:]:
#   if t.count(r)>1:
#     t.remove(r)
# print(t)
# a=[0,0,0,0,1,1,0,2,2,2,3]
# a.remove(0)
# print(a)
# #删除的技巧，remove一次只能删除一个数字，count能够计算重复的数量，所以这是删除了许多次的结果，而且无法保留原有的顺序
#####################################################################################################
#####################################################################################################
# l1 = [1, 1, 2, 2, 3, 3, 3, 3, 6, 6, 5, 5, 2, 2]
# l_index=l1.index(3)
# print(l_index)
#####################################################################################################
#####################################################################################################
# np.set_printoptions(threshold=2000)
# dataset = tonic.datasets.NMNIST(save_to='./data', train=True)
# events, target = dataset[0]
# print(events[0])
# #print(type(events))
# # print(target)
# #a=np.array([0,0,0,0])
# t=[]
# a=np.zeros((34,34))
# k=0
# for i in range(5028):
#   x=events[i][0]
#   y=events[i][1]
#   t.append(events[i][2])
#   s=events[i][3]
#   a[x][y]=a[x][y]+s
#   if s!=0:
#     k=k+s
# # print(a)
# # print(k)
# print(len(t))
# imshow(a, cmap='gray', interpolation='nearest')
# plt.colorbar()
# plt.show()
##画热量图
#####################################################################################################
#####################################################################################################
##数据里面如果在校数量级，几十几百微秒不会造成时间间隔太短，而时间数量级太高，几万十几万微秒，那么它的最短间隔时间是一百微秒0.1毫秒
#####################################################################################################
#####################################################################################################
# a=[1,2,2,2,2,3,4,5,6,6]
# b=[1,2,3,5,5,6,7,8,9,10]
# for r in a[:]:
#   if a.count(r)>1:
#     # print('b[a.index(r):%d'%(b[a.index(r)]))
#     # print('b[a.index(r,a.index(r)+1)]:%d'%(b[a.index(r,a.index(r)+1)]))
#     print(a.index(r,a.index(r)+1))
#     if b[a.index(r)] == b[a.index(r,a.index(r)+1)]:
#       print(1)/
#       a.remove(r)
#       b.remove(b[a.index(r)])
# print(a,b)
#这里有一个非常隐蔽的漏洞，这个漏洞会导致无法删除不对应的重复单位，当第一个a中相同元素相等，而b中不等时，不会删除元素，导致每次检查的元素都是a中第一个相同的元素，然后a中第一个相同元素有四个，把b中相同元素遮挡
#####################################################################################################
#####################################################################################################
# a=[1,2,2,2,2,3,4,5,5,5,6,7]
# b=[1,2,3,5,5,6,7,8,10,10,11,12]
#
# chongfu=0
# a_index=0
# xunhuan=0
# zb=0
# c=[]
# for r in a[:]:
#   if a.count(r)>1:
#     chongfu=a.count(r)
#     a_index=a.index(r)
#     b_index=a_index
#     # print(a.count(r))
#     # print('b[a.index(r):%d'%(b[a.index(r)]))
#     # print('b[a.index(r,a.index(r)+1)]:%d'%(b[a.index(r,a.index(r)+1)]))
#     # print(a.index(r,a.index(r)+1))
#     if chongfu>0:
#       xunhuan=xunhuan+1
#     if chongfu==xunhuan:
#       for cf in b[a_index:a_index+xunhuan]:
#         c.append(cf)
#       for i in c[:]:
#         if c.count(i)>1:
#           a.pop(a_index+c.index(i))
#           b.pop(a_index+c.index(i))
#           c.remove(i)
#       c=[]
#       xunhuan=0
# print(a,b)
# #这个去重的方法是首先计算有多少重复的（由于重复的是相邻的，数据的特征），然后把重复的对应索引添加到一个列表中，然后去重
#####################################################################################################
#####################################################################################################
# a=[1,2,2,2,2,3,4,5,5,5,6,7]
# b=[1,2,3,5,5,6,7,8,9,10,11,12]
# c=a.index(2,4)
# print(c)
#####################################################################################################
#####################################################################################################
# import tonic
# import numpy as np
# import matplotlib.pyplot as plt
# from brian2 import *
# def get_picture(load_path):
#   img = (imread(load_path))
#   return img
#
# img=get_picture('D:/happy new year/picture2/0.jpg')
# print(img)
#
# h=img.reshape(1,784)
# r_ange=10
# tuxiangxz=28
# hh1=np.zeros((1,784))
# hh2=np.zeros((1,784))
# hh3=np.zeros((1,784))
# hh4=np.zeros((1,784))
# for i in range(700):
#   if (h[0,i]-r_ange<h[0,i+tuxiangxz+1]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+(tuxiangxz+1)*2]<h[0,i]+r_ange):
#     hh1[0,i]=h[0,i+tuxiangxz+1]
#   if (h[0,i]-r_ange<h[0,i+tuxiangxz]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+tuxiangxz*2]<h[0,i]+r_ange):
#     hh2[0,i]=h[0,i+tuxiangxz]
#   if (h[0,i]-r_ange<h[0,i+tuxiangxz-1]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+(tuxiangxz-1)*2]<h[0,i]+r_ange):
#     hh3[0,i]=h[0,i+tuxiangxz-1]
#   if (h[0,i]-r_ange<h[0,i+1]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+2]<h[0,i]+r_ange):
#     hh4[0,i]=h[0,i+1]
# for i in range(784):
#   if (hh1[0,i]==1) or (hh2[0,i]==1) or (hh3[0,i]==1) or (hh4[0,i]==1) :
#     hh1[0,i]=200
# hh1=hh1.reshape(28,28)
# imshow(hh1, cmap='gray', interpolation='nearest')
# # hh1=hh1.reshape(28,28)
# # hh2=hh2.reshape(28,28)
# # hh3=hh3.reshape(28,28)
# # hh4=hh4.reshape(28,28)
# # subplot(221)
# # imshow(hh1, cmap='gray', interpolation='nearest')
# # subplot(222)
# # imshow(hh2, cmap='gray', interpolation='nearest')
# # subplot(223)
# # imshow(hh3, cmap='gray', interpolation='nearest')
# # subplot(224)
# # imshow(hh4, cmap='gray', interpolation='nearest')
# show()
# 关于方向柱有个问题需要解决：四个方向柱应该可以把图片的完整信息拼接起来，但是实验结果好像并不是那么回事，所以这段代码保留下来
#####################################################################################################
#####################################################################################################
i=[1,2,3,4,5,6,7,8,9,0]
j=[]
for k in range(9):
  j.append(i[k]/5)
print(j)





















