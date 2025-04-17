# longlonglonglong
# longlonglonglong
#lianjie:先连成1比1的连接，后面再改
#stdp
#1.2把泊松的值存储到一个列表里，这样就不用每次更新网络了，添加了stdp
# longlonglonglong
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
from brian2 import *
np.set_printoptions(threshold=2000)
start=time.time()
print(start)
def get_picture(load_path):
  img = (imread(load_path))
  return img
img=get_picture('D:/happy new year/picture2/0.jpg')
img_flatten_yi=img.flatten()
img_flatten = np.matrix(img_flatten_yi, dtype=np.int32)
#参数
tau1 = 15*ms
tau2 = 0.4*ms
run_time = 500*ms

taum2,taue2,taui2 = 20*ms,5*ms,10*ms
taum3,taue3,taui3 = 20*ms,5*ms,10*ms

Vt2,Vr2 = 10*mV,0*mV
Vt3,Vr3 = 10*mV,0*mV

taupre = taupost = 20*ms
wmax = 100
Apre2_3_e = 0.1
Apost2_3_e = -Apre2_3_e*taupre/taupost*1.05
Apre2_3_i = 0.1
Apost2_3_i = -Apre2_3_i*taupre/taupost*1.05
#连接矩阵
# juzhen=np.zeros((784,784))
# for i in range(784):
#   juzhen[i][i]=1
#   juzhen[i+1][i]=1
# sources, targets = juzhen.nonzero()

a=[]
for i in range(784):
  a.append(abs(int((img_flatten[0,i]-50)/10)))

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

G1 = NeuronGroup(784, eqs1, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G1.I=a
#G2层权重无法更改，所以为了更加区分颜色(在输入层是激活次数)，设置激活次数作为颜色的区分特征而不是电压。
G2=NeuronGroup(4000,eqs2, threshold='v>Vt2', reset='v = Vr2', refractory = 1*ms,method='exact')
G2.v=0*mV

G3_e=NeuronGroup(3920,eqs3, threshold='v>Vt3', reset='v = Vr3', refractory = 10*ms,method='exact')
G3_i=NeuronGroup(80,eqs3, threshold='v>Vt3', reset='v = Vr3', refractory = 10*ms,method='exact')
G3_e.v=0*mV
G3_i.v=0*mV
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

M_G2=SpikeMonitor(G2)
M_G3=SpikeMonitor(G3_e)
M_state_G3_e=StateMonitor(G3_e,'v',record=True)
M_state_s_e=StateMonitor(S2_3_e,['w2_3_e','apre','apost'],record=True)
M_state_G2=StateMonitor(G2,'v',record=True)
M_state_G1=StateMonitor(G1,'v',record=True)
run(run_time)
end=time.time()
print(end)
subplot(311)
plot(M_state_G2.t/ms,M_state_G3_e.v[930],label='930')
plot(M_state_G2.t/ms,M_state_G2.v[930],label='117')
legend()
subplot(312)
plot(M_G3.t/ms,M_G3.i,'.k',label='G3')
legend()
subplot(313)
plot(M_state_s_e.t/ms,M_state_s_e.apre[9300],label='apre')
plot(M_state_s_e.t/ms,M_state_s_e.apost[9300],label='apost')
plot(M_state_s_e.t/ms,M_state_s_e.w2_3_e[9300],label='we2_3')
legend()
# ooo=M.i
# lllie=[]
# for i in range(len(ooo)):
#   lllie.append(ooo[i])
# for i in lllie[:]:
#   if 926 == i:
#     print(lllie.count(i))
show()

















