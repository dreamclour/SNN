#lianjie:先连成1比1的连接，后面再改
#stdp
#1.2把泊松的值存储到一个列表里，这样就不用每次更新网络了，添加了stdp
#lianjie:先连成1比1的连接，后面再改
#stdp#
#1.2使用timedArray，这样就不用每次更新网络了，添加了stdp
#1.3更改神经元，更改连接
#2更改输入神经元更改数据集，开始训练！
#2.1添加的眼方向柱还不满意，从2.1开始放弃使用泊松输入，改用普通神经元输入，使用mnist数据集。分为两支，一支不使用方向柱，另一支使用方向柱，2.1是不加方向柱的
#2.1下面建立一个有四层网络的结构，输入层和三层中间层（仿照皮层结构），有激发神经元和抑制神经元
#2.1先搁置前后神经元tau不相等的事情。
#2.2在2.1中还是建立在有横向链接的结构中吧，2.2就是直接连接。
#2.2任务测试apreapost
#整一个可以归档的，shi3放2-3层，shishi3放3-4层shishishi3放4-5层
#网络跑通了，现在的任务是调整网络权重和一些连接，使其达到理想状态
#权重调整暂时结束，进行神经细胞的可视化，或者增加程序的结构化。
from brian2 import *
np.set_printoptions(threshold=2000)
start=time.time()
print(start)
def get_picture(load_path):
  img = (imread(load_path))
  return img
img=get_picture('D:/happy new year/picture2/9.jpg')
img_flatten_yi=img.flatten()
img_flatten = np.matrix(img_flatten_yi, dtype=np.int32)

a=[]
for i in range(784):
  if img_flatten[0,i]>=50:
    a.append(int((img_flatten[0,i]-50)/10))
  if img_flatten[0,i]<50:
    a.append(0)

#参数
tau1 = 15*ms
tau2 = 0.4*ms
run_time = 500*ms

taum2,taue2,taui2 = 20*ms,5*ms,10*ms
taum3,taue3,taui3 = 20*ms,5*ms,10*ms
taum4,taue4,taui4 = 20*ms,5*ms,10*ms
taum5,taue5,taui5 = 20*ms,5*ms,10*ms

Vt2,Vr2 = 10*mV,0*mV
Vt3,Vr3 = 10*mV,0*mV
Vt4,Vr4 = 10*mV,0*mV
Vt5,Vr5 = 10*mV,0*mV

taupre = taupost = 20*ms
wmax = 2000
Apre2_3_e = 0.1
Apost2_3_e = -Apre2_3_e*taupre/taupost*1.05
Apre2_3_i = 0.1
Apost2_3_i = -Apre2_3_i*taupre/taupost*1.05

Apre3_4_ee = 0.1
Apost3_4_ee = -Apre3_4_ee*taupre/taupost*1.05
Apre3_4_ei = 0.1
Apost3_4_ei = -Apre3_4_ei*taupre/taupost*1.05
# Apre3_4_ie = 0.1
# Apost3_4_ie = -Apre3_4_ie*taupre/taupost*1.05
# Apre3_4_ii = 0.1
# Apost3_4_ii = -Apre3_4_ii*taupre/taupost*1.05

Apre4_5_ee = 0.1
Apost4_5_ee = -Apre4_5_ee*taupre/taupost*1.05
Apre4_5_ei = 0.1
Apost4_5_ei = -Apre4_5_ei*taupre/taupost*1.05

#a=[x for x in range(20)]
#a=10//17在参数为tau1=15tau2=0.4threshold=0.15run_time=50ms的时候
#a=0//0
#a=1//0
#a=2//4
#a=3//6
#a=4//8
#a=5//10
#a=6//12
#a=7//13
#a=8//14
#a=9//16
#a=10//17
#a=11//17
#a=12//18
#a=13//19
#a=14//19
#a=15//20
#a=16//21
#a=17//21
#a=18//22
#a=19//22
#a=20//23

eqs1='''
dv/dt=(I-v)/tau1 :1(unless refractory)
I:1
'''

eqs2='''
dv/dt  = (ge2+gi2-v)/taum2 : volt (unless refractory)
dge2/dt = -ge2/taue2 : volt
dgi2/dt = -gi2/taui2 : volt
'''

eqs3='''
dv/dt  = (ge3+gi3-v)/taum3 : volt (unless refractory)
dge3/dt = -ge3/taue3 : volt
dgi3/dt = -gi3/taui3 : volt
'''

eqs4='''
dv/dt  = (ge4+gi4-v)/taum4 : volt (unless refractory)
dge4/dt = -ge4/taue4 : volt
dgi4/dt = -gi4/taui4 : volt
'''

eqs5='''
dv/dt  = (ge5+gi5-v)/taum5 : volt (unless refractory)
dge5/dt = -ge5/taue5 : volt
dgi5/dt = -gi5/taui5 : volt
'''

G1 = NeuronGroup(784, eqs1, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G1.I=a
#G2层权重无法更改，所以为了更加区分颜色(在输入层是激活次数)，设置激活次数作为颜色的区分特征而不是电压。
G2=NeuronGroup(4000,eqs2, threshold='v>Vt2', reset='v = Vr2', refractory = 1*ms,method='exact')
G2.v=0*mV

G3_e=NeuronGroup(3920,eqs3, threshold='v>Vt3', reset='v = Vr3', refractory = 10*ms,method='exact')
G3_i=NeuronGroup(80,eqs3, threshold='v>Vt3', reset='v = Vr3', refractory = 10*ms,method='exact')
G3_e.v=0*mV
G3_i.v=0*mV

G4_e=NeuronGroup(3920,eqs4, threshold='v>Vt4', reset='v = Vr4', refractory = 10*ms,method='exact')
G4_i=NeuronGroup(80,eqs4, threshold='v>Vt4', reset='v = Vr4', refractory = 10*ms,method='exact')
G4_e.v=0*mV
G4_i.v=0*mV

G5_e=NeuronGroup(3920,eqs5, threshold='v>Vt5', reset='v = Vr5', refractory = 10*ms,method='exact')
G5_i=NeuronGroup(80,eqs5, threshold='v>Vt5', reset='v = Vr5', refractory = 10*ms,method='exact')
G5_e.v=0*mV
G5_i.v=0*mV

#这里精确的激活已经不在有意义了，或者说有意义，留作以后网络结构的更改吧。
we1_2= 2
S1_2=Synapses(G1, G2, 'w : 1', on_pre='ge2 += we1_2*mV')
jz1_2=np.zeros((784,4000))
for i in range(784):
  for j in range(20):
    jz1_2[i][5*i+j]=1
sources1_2,targets1_2=jz1_2.nonzero()
S1_2.connect(i=sources1_2,j=targets1_2)

S2_3_e=Synapses(G2, G3_e,
             '''
             w2_3_e : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             ge3 += w2_3_e *mV
             apre += Apre2_3_e
             w2_3_e = clip(w2_3_e+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost2_3_e
             w2_3_e = clip(w2_3_e+apre, 0, wmax)
             ''', method='linear')

S2_3_i=Synapses(G2, G3_i,
             '''
             w2_3_i : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             ge3 += w2_3_i *mV
             apre += Apre2_3_i
             w2_3_i = clip(w2_3_i+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost2_3_i
             w2_3_i = clip(w2_3_i+apre, 0, wmax)
             ''', method='linear')

jz2_3_e=np.zeros((4000,3920))
jz2_3_i=np.zeros((4000,80))
for i in range(3920):
  for j in range(10):
    jz2_3_e[i+j][i]=1
sources2_3_e,targets2_3_e=jz2_3_e.nonzero()
S2_3_e.connect(i=sources2_3_e,j=targets2_3_e)
k=0
for i in range(3900):
  if (i + 50) % 50 == 0:
    k += 1
    for j in range(20):
      jz2_3_i[i+j][k]=1
sources2_3_i,targets2_3_i=jz2_3_i.nonzero()
S2_3_i.connect(i=sources2_3_i,j=targets2_3_i)

S2_3_e.w2_3_e= 5
S2_3_i.w2_3_i = 5

S3_4_ee=Synapses(G3_e, G4_e,
             '''
             w3_4_ee : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             ge4 += w3_4_ee*mV
             apre += Apre3_4_ee
             w3_4_ee = clip(w3_4_ee+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost3_4_ee
             w3_4_ee = clip(w3_4_ee+apre, 0, wmax)
             ''', method='linear')

S3_4_ei=Synapses(G3_e, G4_i,
             '''
             w3_4_ei : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             ge4 += w3_4_ei*mV
             apre += Apre3_4_ei
             w3_4_ei = clip(w3_4_ei+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost3_4_ei
             w3_4_ei = clip(w3_4_ei+apre, 0, wmax)
             ''', method='linear')

S3_4_ie=Synapses(G3_i, G4_e,'w3_4_ie:1',on_pre='gi4 -= w3_4_ie*mV')
S3_4_ii=Synapses(G3_i, G4_i,'w3_4_ii:1',on_pre='gi4 -= w3_4_ii*mV')

jz3_4_ee=np.zeros((3920,3920))
jz3_4_ei=np.zeros((3920,80))
jz3_4_ie=np.zeros((80,3920))
jz3_4_ii=np.zeros((80,80))
#记住四对关系，ee、ei、ie、ii
for i in range(3910):
  for j in range(10):
    jz3_4_ee[i][i+j]=1
sources3_4_ee,targets3_4_ee=jz3_4_ee.nonzero()
for i in range(77):
  for j in range(20):
    jz3_4_ei[i*50+j+20][i]=1
sources3_4_ei,targets3_4_ei=jz3_4_ei.nonzero()
for i in range(78):
  for j in range(20):
    jz3_4_ie[i][i*50+j]=1
sources3_4_ie,targets3_4_ie=jz3_4_ie.nonzero()
for i in range(80):
  jz3_4_ii[i][i]=1
sources3_4_ii,targets3_4_ii=jz3_4_ii.nonzero()

S3_4_ee.connect(i=sources3_4_ee,j=targets3_4_ee)
S3_4_ei.connect(i=sources3_4_ei,j=targets3_4_ei)
S3_4_ie.connect(i=sources3_4_ie,j=targets3_4_ie)
S3_4_ii.connect(i=sources3_4_ii,j=targets3_4_ii)

S3_4_ee.w3_4_ee=10
S3_4_ei.w3_4_ei=10
S3_4_ie.w3_4_ie=0
S3_4_ii.w3_4_ii=0

S4_5_ee=Synapses(G4_e, G5_e,
             '''
             w4_5_ee : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             ge5 += w4_5_ee*mV
             apre += Apre4_5_ee
             we4_5 = clip(w4_5_ee+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost4_5_ee
             we4_5 = clip(w4_5_ee+apre, 0, wmax)
             ''', method='linear')

S4_5_ei=Synapses(G4_e, G5_i,
             '''
             w4_5_ei : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             ge5 += w4_5_ei*mV
             apre += Apre4_5_ei
             we4_5 = clip(w4_5_ei+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost4_5_ei
             we4_5 = clip(w4_5_ei+apre, 0, wmax)
             ''', method='linear')
S4_5_ie=Synapses(G4_i, G5_e,'w4_5_ie:1',on_pre='gi5 -= w4_5_ie*mV')
S4_5_ii=Synapses(G4_i, G5_i,'w4_5_ii:1',on_pre='gi5 -= w4_5_ii*mV')

jz4_5_ee=np.zeros((3920,3920))
jz4_5_ei=np.zeros((3920,80))
jz4_5_ie=np.zeros((80,3920))
jz4_5_ii=np.zeros((80,80))

for i in range(3910):
  for j in range(10):
    jz4_5_ee[i][i+j]=1
sources4_5_ee,targets4_5_ee=jz4_5_ee.nonzero()
for i in range(77):
  for j in range(20):
    jz4_5_ei[i*50+j][i]=1
sources4_5_ei,targets4_5_ei=jz4_5_ei.nonzero()
for i in range(78):
  for j in range(20):
    jz4_5_ie[i][i*50+j+20]=1
sources4_5_ie,targets4_5_ie=jz4_5_ie.nonzero()
for i in range(80):
  jz4_5_ii[i][i]=1
sources4_5_ii,targets4_5_ii=jz4_5_ii.nonzero()

S4_5_ee.connect(i=sources4_5_ee,j=targets4_5_ee)
S4_5_ei.connect(i=sources4_5_ei,j=targets4_5_ei)
S4_5_ie.connect(i=sources4_5_ie,j=targets4_5_ie)
S4_5_ii.connect(i=sources4_5_ii,j=targets4_5_ii)

S4_5_ee.w4_5_ee=10
S4_5_ei.w4_5_ei=10
S4_5_ie.w4_5_ie=10
S4_5_ii.w4_5_ii=20

M_G1=SpikeMonitor(G1)
M_G2=SpikeMonitor(G2)
M_G3_e=SpikeMonitor(G3_e)
M_G3_i=SpikeMonitor(G3_i)
M_G4_e=SpikeMonitor(G4_e)
M_G4_i=SpikeMonitor(G4_i)
M_G5_e=SpikeMonitor(G5_e)
M_G5_i=SpikeMonitor(G5_i)

M_state_G3_e=StateMonitor(G3_e,'v',record=True)
M_state_G4_e=StateMonitor(G4_e,'v',record=True)
M_state_G3_s_e=StateMonitor(S2_3_e,['w2_3_e','apre','apost'],record=True)
M_state_G4_s_e=StateMonitor(S3_4_ee,['w3_4_ee','apre','apost'],record=True)
M_state_G2=StateMonitor(G2,'v',record=True)
M_state_G1=StateMonitor(G1,'v',record=True)
run(run_time,report='text')
end=time.time()
print(end)
# subplot(311)
# plot(M_state_G2.t/ms,M_state_G3_e.v[930],label='930')
# plot(M_state_G2.t/ms,M_state_G2.v[930],label='117')
# legend()
# subplot(312)
# plot(M_G5_e.t/ms,M_G5_e.i,'.k',label='G5')
# legend()
# subplot(313)
# # plot(M_state_G3_s_e.t/ms,M_state_G3_s_e.apre[9300],label='apre')
# # plot(M_state_G3_s_e.t/ms,M_state_G3_s_e.apost[9300],label='apost')
# # plot(M_state_G3_s_e.t/ms,M_state_G3_s_e.w2_3_e[9300],label='we2_3')
# plot(M_state_G4_s_e.t/ms,M_state_G4_s_e.apre[9300],label='apre')
# plot(M_state_G4_s_e.t/ms,M_state_G4_s_e.apost[9300],label='apost')
# plot(M_state_G4_s_e.t/ms,M_state_G4_s_e.w3_4_ee[9300],label='we3_4_ee')
# legend()

# subplot(511)
# plot(M_G1.t/ms,M_G1.i,',k',color='black',label='G1')
# legend()
# subplot(512)
# plot(M_G2.t/ms,M_G2.i,'.k',color='black',label='G2')
# legend()
# subplot(513)
# plot(M_G3_e.t/ms,M_G3_e.i,'.k',color='black',label='G3')
# plot(M_G3_i.t/ms,M_G3_i.i*50,'.k',color='red',label='G3')
# legend()
# subplot(514)
# plot(M_G4_e.t/ms,M_G4_e.i,'.k',color='black',label='G4')
# plot(M_G4_i.t/ms,M_G4_i.i*50,'.k',color='red',label='G4')
# legend()
# subplot(515)
# plot(M_G5_e.t/ms,M_G5_e.i,'.k',color='black',label='G5')
# plot(M_G5_i.t/ms,M_G5_i.i*50,',k',color='red',label='G5')
# legend()

k=np.zeros((28,28))
for i in M_G1.i:
  k[int(i/28),i%28] += 1

k2list=[]
k2list_2=[]
k2=np.zeros((28,28))
k2list=M_G2.i
for i in range(len(k2list)):
  k2list_2.append(int(k2list[i]/5))
for i in k2list_2:
  k2[int(i/28),i%28] += 1

k3list=[]
k3list_2=[]
k3=np.zeros((28,28))
k3list=M_G3_e.i
for i in range(len(k3list)):
  k3list_2.append(int(k3list[i]/5))
for i in k3list_2:
  k3[int(i/28),i%28] += 1


k4list=[]
k4list_2=[]
k4=np.zeros((28,28))
k4list=M_G4_e.i
for i in range(len(k4list)):
  k4list_2.append(int(k4list[i]/5))
for i in k3list_2:
  k4[int(i/28),i%28] += 1

k5list=[]
k5list_2=[]
k5=np.zeros((28,28))
k5list=M_G5_e.i
for i in range(len(k5list)):
  k5list_2.append(int(k5list[i]/5))
for i in k5list_2:
  k5[int(i/28),i%28] += 1

subplot(151)
plt.imshow(k)
plt.colorbar()
plt.tight_layout()

subplot(152)
plt.imshow(k2)
plt.colorbar()
plt.tight_layout()

subplot(153)
plt.imshow(k3)
plt.colorbar()
plt.tight_layout()

subplot(154)
plt.imshow(k4)
plt.colorbar()
plt.tight_layout()

subplot(155)
plt.imshow(k5)
plt.colorbar()
plt.tight_layout()

show()

















