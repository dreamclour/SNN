# longlonglonglong
#这个程序结合了SNN的手写识别网络，就是网络部分和故障检测的数据处理部分。
# -*- coding: utf-8 -*-
# import matplotlib
# matplotlib.use('QT5Agg')
import os
#os.environ[‘HDF5_DISABLE_VERSION_CHECK’] = ‘2’
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

config = tf.compat.v1.ConfigProto(gpu_options=tf.compat.v1.GPUOptions(allow_growth=True))
sess = tf.compat.v1.Session(config=config)
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import scipy.io as scio
import pandas as pd


def data_load(filepath, labelname, csv_name):
  data = scio.loadmat(filepath)
  for name in data.keys():
    print(name.title())
  data_train = data['train_data']
  data_label = data['label_data']
  data_label_1 = np.full((10000, 1), data_label[0, 0])  # 标签填充（10000，1）shape
  row = len(data_label) - 1
  data_label1 = data_label[0]  # 表示真正的label
  data_train_pin = np.append(data_train[0, :, :], data_label_1, axis=1)
  # print('len(data_train[0])')
  # print(len(data_train))
  for i in range(row):
    data_train_1 = data_train[i + 1, :, :]
    data_train_2 = np.append(data_train_1, data_label_1, axis=1)
    data_train_pin = np.append(data_train_pin, data_train_2, axis=0)
  data = pd.DataFrame(data_train_pin, \
                      columns=['Voltage_0', 'Voltage_1', 'Voltage_2', 'Current_0', \
                               'Current_1', 'Current_2', 'Rotor_Current', 'Speed', \
                               'Failde', labelname])
  data.to_csv(csv_name, index=False)
  # print(type(data))
  return data


filepath = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Disconnect_Phase_10_11_21_.mat'
labelname = 'Disconnect_Phase_10_11_21_'
csv_name = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Disconnect_Phase_10_11_21_c.csv'
# data_load(filepath,labelname,csv_name)
data_Preprocessed_Disconnect_Phase_10_11_21 = pd.read_csv(csv_name)

filepath = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_No_failed.mat'
labelname = 'No_failed'
csv_name = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_No_failed_c.csv'
# data_load(filepath,labelname,csv_name)
data_Preprocessed_No_failed = pd.read_csv(csv_name)

filepath = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Rotor_Current_Failed_R_.mat'
labelname = 'Rotor_Current_Failed_R_'
csv_name = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Rotor_Current_Failed_R_c.csv'
# data_load(filepath,labelname,csv_name)
data_Preprocessed_Rotor_Current_Failed_R = pd.read_csv(csv_name)

filepath = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Short_between_two_phases_.mat'
labelname = 'Short_between_two_phases_'
csv_name = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Short_between_two_phases_c.csv'
# data_load(filepath,labelname,csv_name)
data_Preprocessed_Short_between_two_phases = pd.read_csv(csv_name)

filepath = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Test_Data_Rotor_Current_Faild.mat'
labelname = 'Test_Data_Rotor_Current_Faild'
csv_name = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Test_Data_Rotor_Current_Faild_c.csv'
# data_load(filepath,labelname,csv_name)
data_Preprocessed_Test_Data_Rotor_Current_Faild = pd.read_csv(csv_name)

filepath = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Test_Data_Short_phases_Ln_G_.mat'
labelname = 'Test_Data_Short_phases_Ln_G_'
csv_name = 'D:/2024/guzhangjianceshuju/shuju/motor-faults-main/motor-faults-main/Preprocessed_Test_Data_Short_phases_Ln_G_c.csv'
# data_load(filepath,labelname,csv_name)
data_Preprocessed_Test_Data_Short_phases_Ln_G = pd.read_csv(csv_name)


# dataframe data/  array label
# 这是二维的一个数据处理，data.iloc。将二维变成三维的空间，为下一步做准备，一次实验的准备。
def data_processing(data):
  data = data.iloc[:, 0:8]  # 把标签去掉
  row = data.shape[0]
  data = np.array(data)
  data = data.reshape(int(row / 10000), 10000, 8)  # 是最初的去掉标签的
  return data


def downsample(data, sample_time=4):  # 这里有个采样时间
  row = int(data.shape[0])  # 试验次数
  data1 = np.zeros(
    shape=(int(data.shape[0] * sample_time), int(data.shape[1] / sample_time), data.shape[2]))  # 这是一个加厚了实验次数那一维度
  x1 = np.arange(0, int(data.shape[1]), sample_time)
  x2 = np.arange(1, int(data.shape[1]), sample_time)
  x3 = np.arange(2, int(data.shape[1]), sample_time)
  x4 = np.arange(3, int(data.shape[1]), sample_time)
  for i in range(0, row):
    data1[sample_time * i:sample_time * i + 1, :, :] = data[i:i + 1, x1, :]
    data1[sample_time * i + 1:sample_time * i + 2, :, :] = data[i:i + 1, x2, :]
    data1[sample_time * i + 2:sample_time * i + 3, :, :] = data[i:i + 1, x3, :]
    data1[sample_time * i + 3:sample_time * i + 4, :, :] = data[i:i + 1, x4, :]
  return data1


# 和4相关了，加厚实验和采样时间减少了一万那个维度的数据，相当于产生了多次实验


'''
label 0  / Test_Data_Rotor_Current_Faild
'''

data_Preprocessed_Test_Data_Rotor_Current_Faild = data_processing(data_Preprocessed_Test_Data_Rotor_Current_Faild)
data_Preprocessed_Test_Data_Rotor_Current_Faild = downsample(data_Preprocessed_Test_Data_Rotor_Current_Faild)
row0 = data_Preprocessed_Test_Data_Rotor_Current_Faild.shape[0]  # 试验次数还是加厚过的
label_data_Preprocessed_Test_Data_Rotor_Current_Faild = 0 * np.ones(shape=(int(row0), 1))  # 打上标签

'''
label 1  / Disconnect_Phase_10_11_21
'''

data_Preprocessed_Disconnect_Phase_10_11_21 = data_processing(data_Preprocessed_Disconnect_Phase_10_11_21)
data_Preprocessed_Disconnect_Phase_10_11_21 = downsample(data_Preprocessed_Disconnect_Phase_10_11_21)
row1 = data_Preprocessed_Disconnect_Phase_10_11_21.shape[0]
label_data_Preprocessed_Disconnect_Phase_10_11_21 = 1 * np.ones(shape=(int(row1), 1))

'''
label 2 / Rotor_Current_Failed_R
'''
data_Preprocessed_Rotor_Current_Failed_R = data_processing(data_Preprocessed_Rotor_Current_Failed_R)
data_Preprocessed_Rotor_Current_Failed_R = downsample(data_Preprocessed_Rotor_Current_Failed_R)
row2 = data_Preprocessed_Rotor_Current_Failed_R.shape[0]
label_data_Preprocessed_Rotor_Current_Failed_R = 2 * np.ones(shape=(int(row2), 1))

'''
label 3 / Short_between_two_phases
'''
data_Preprocessed_Short_between_two_phases = data_processing(data_Preprocessed_Short_between_two_phases)
data_Preprocessed_Short_between_two_phases = downsample(data_Preprocessed_Short_between_two_phases)
row3 = data_Preprocessed_Short_between_two_phases.shape[0]
label_data_Preprocessed_Short_between_two_phases = 3 * np.ones(shape=(int(row3), 1))

'''
label 4 / Test_Data_Short_phases_Ln_G
'''
data_Preprocessed_Test_Data_Short_phases_Ln_G = data_processing(data_Preprocessed_Test_Data_Short_phases_Ln_G)
data_Preprocessed_Test_Data_Short_phases_Ln_G = downsample(data_Preprocessed_Test_Data_Short_phases_Ln_G)
row4 = data_Preprocessed_Test_Data_Short_phases_Ln_G.shape[0]
label_data_Preprocessed_Test_Data_Short_phases_Ln_G = 4 * np.ones(shape=(int(row4), 1))

'''
label 5 / No_failed
'''
data_Preprocessed_No_failed = data_processing(data_Preprocessed_No_failed)
data_Preprocessed_No_failed = downsample(data_Preprocessed_No_failed)
row5 = data_Preprocessed_No_failed.shape[0]
label_data_Preprocessed_No_failed = 5 * np.ones(shape=(int(row5), 1))

# pick up the minimum row / rebulid data
row_for_all = int(np.min([row0, row1, row2, row3, row4, row5])) - int(
  0.1 * np.min([row0, row1, row2, row3, row4, row5]))
data_Preprocessed_Test_Data_Rotor_Current_Faild_ = data_Preprocessed_Test_Data_Rotor_Current_Faild[0:row_for_all, :, :]
data_Preprocessed_Disconnect_Phase_10_11_21_ = data_Preprocessed_Disconnect_Phase_10_11_21[0:row_for_all, :, :]
data_Preprocessed_Rotor_Current_Failed_R_ = data_Preprocessed_Rotor_Current_Failed_R[0:row_for_all, :, :]
data_Preprocessed_Short_between_two_phases_ = data_Preprocessed_Short_between_two_phases[0:row_for_all, :, :]
data_Preprocessed_Test_Data_Short_phases_Ln_G_ = data_Preprocessed_Test_Data_Short_phases_Ln_G[0:row_for_all, :, :]
data_Preprocessed_No_failed_ = data_Preprocessed_No_failed[0:row_for_all, :, :]
label_data_Preprocessed_Test_Data_Rotor_Current_Faild_ = label_data_Preprocessed_Test_Data_Rotor_Current_Faild[
                                                         0:row_for_all, :]
label_data_Preprocessed_Disconnect_Phase_10_11_21_ = label_data_Preprocessed_Disconnect_Phase_10_11_21[0:row_for_all, :]
label_data_Preprocessed_Rotor_Current_Failed_R_ = label_data_Preprocessed_Rotor_Current_Failed_R[0:row_for_all, :]
label_data_Preprocessed_Short_between_two_phases_ = label_data_Preprocessed_Short_between_two_phases[0:row_for_all, :]
label_data_Preprocessed_Test_Data_Short_phases_Ln_G_ = label_data_Preprocessed_Test_Data_Short_phases_Ln_G[
                                                       0:row_for_all, :]
label_data_Preprocessed_No_failed_ = label_data_Preprocessed_No_failed[0:row_for_all, :]

data_for_train = np.concatenate(
  [data_Preprocessed_Test_Data_Rotor_Current_Faild_, data_Preprocessed_Disconnect_Phase_10_11_21_,\
   data_Preprocessed_Rotor_Current_Failed_R_, data_Preprocessed_Short_between_two_phases_,\
   data_Preprocessed_Test_Data_Short_phases_Ln_G_, data_Preprocessed_No_failed_], axis=0)
label_for_train = np.concatenate(
  [label_data_Preprocessed_Test_Data_Rotor_Current_Faild_, label_data_Preprocessed_Disconnect_Phase_10_11_21_,\
   label_data_Preprocessed_Rotor_Current_Failed_R_, label_data_Preprocessed_Short_between_two_phases_,\
   label_data_Preprocessed_Test_Data_Short_phases_Ln_G_, label_data_Preprocessed_No_failed_], axis=0)
print(data_for_train.shape[0])
print(data_for_train.shape[1])
print(data_for_train.shape[2])

# for test
data_Preprocessed_Test_Data_Rotor_Current_Faild_ = data_Preprocessed_Test_Data_Rotor_Current_Faild[row_for_all:row0 + 1,
                                                   :, :]
data_Preprocessed_Disconnect_Phase_10_11_21_ = data_Preprocessed_Disconnect_Phase_10_11_21[row_for_all:row1 + 1, :, :]
data_Preprocessed_Rotor_Current_Failed_R_ = data_Preprocessed_Rotor_Current_Failed_R[row_for_all:row2 + 1, :, :]
data_Preprocessed_Short_between_two_phases_ = data_Preprocessed_Short_between_two_phases[row_for_all:row3 + 1, :, :]
data_Preprocessed_Test_Data_Short_phases_Ln_G_ = data_Preprocessed_Test_Data_Short_phases_Ln_G[row_for_all:row4 + 1, :,
                                                 :]
data_Preprocessed_No_failed_ = data_Preprocessed_No_failed[row_for_all:row5 + 1, :, :]
label_data_Preprocessed_Test_Data_Rotor_Current_Faild_ = label_data_Preprocessed_Test_Data_Rotor_Current_Faild[
                                                         row_for_all:row0 + 1, :]
label_data_Preprocessed_Disconnect_Phase_10_11_21_ = label_data_Preprocessed_Disconnect_Phase_10_11_21[
                                                     row_for_all:row1 + 1, :]
label_data_Preprocessed_Rotor_Current_Failed_R_ = label_data_Preprocessed_Rotor_Current_Failed_R[row_for_all:row2 + 1,
                                                  :]
label_data_Preprocessed_Short_between_two_phases_ = label_data_Preprocessed_Short_between_two_phases[
                                                    row_for_all:row3 + 1, :]
label_data_Preprocessed_Test_Data_Short_phases_Ln_G_ = label_data_Preprocessed_Test_Data_Short_phases_Ln_G[
                                                       row_for_all:row4 + 1, :]
label_data_Preprocessed_No_failed_ = label_data_Preprocessed_No_failed[row_for_all:row5 + 1, :]

data_for_test = np.concatenate(
  [data_Preprocessed_Test_Data_Rotor_Current_Faild_, data_Preprocessed_Disconnect_Phase_10_11_21_, \
   data_Preprocessed_Rotor_Current_Failed_R_, data_Preprocessed_Short_between_two_phases_, \
   data_Preprocessed_Test_Data_Short_phases_Ln_G_, data_Preprocessed_No_failed_], axis=0)
label_for_test = np.concatenate(
  [label_data_Preprocessed_Test_Data_Rotor_Current_Faild_, label_data_Preprocessed_Disconnect_Phase_10_11_21_, \
   label_data_Preprocessed_Rotor_Current_Failed_R_, label_data_Preprocessed_Short_between_two_phases_, \
   label_data_Preprocessed_Test_Data_Short_phases_Ln_G_, label_data_Preprocessed_No_failed_], axis=0)

# Nomalizaiton for x_train
row = data_for_train.shape[0]
for i in range(row):
  data_for_train[i:i + 1, :, :] = \
    (data_for_train[i:i + 1, :, :] - np.min(data_for_train[i:i + 1, :, :], axis=1)) / \
    (np.max(data_for_train[i:i + 1, :, :], axis=1) - np.min(data_for_train[i:i + 1, :, :], axis=1))
data_for_train = data_for_train.reshape(data_for_train.shape[0], data_for_train.shape[1], data_for_train.shape[2], 1)

num = np.random.permutation(data_for_train.shape[0])  # 打乱index
data_for_train = data_for_train[num, :]  # 打乱数据
label_for_train = label_for_train[num, :]




