#使用普通的输入，不使用泊松分布
from brian2 import *
import tonic
np.set_printoptions(threshold=2000)
start=time.time()
print(start)
def get_picture(load_path):
  img = (imread(load_path))
  return img
img=get_picture('D:/happy new year/picture2/0.jpg')
img_flatten_yi=img.flatten()
img_flatten = np.matrix(img_flatten_yi, dtype=np.int32)
tau1=15*ms
tau2=0.4*ms
run_time=50*ms

#连接矩阵
juzhen=np.zeros((784,784))
for i in range(784):
  juzhen[i][i]=1
  juzhen[i+1][i]=1
sources, targets = juzhen.nonzero()

a=[]
for i in range(784):
  a[i]=abs(int((img_flatten[0,i]-50)/10))
  #img_flatten[i]=int(img_flatten[i])
#print(img_flatten)
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
dv/dt  = (ge+gi-(v-El))/taum : volt (unless refractory)
dge/dt = -ge/taue : volt
dgi/dt = -gi/taui : volt
'''

G1 = NeuronGroup(784, eqs1, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G1.I=a
G2=NeuronGroup(784, eqs2, threshold='v>0.15', reset='v = 0', refractory = 1*ms,method='exact')
S=Synapses(G1, G2, 'w : 1', on_pre='v_post += 0.1')
S.connect(i=sources,j=targets)
M=SpikeMonitor(G2)
M_state=StateMonitor(G2,'v',record=True)
run(run_time)
subplot(211)
for i in range(20):
  plot(M_state.t/ms,M_state.v[i])
#plot(M_state.t/ms,M_state.v[18])
subplot(212)
plot(M.t/ms,M.i,'.k')
print(M.count)
print(M_state.v[17])
show()
















