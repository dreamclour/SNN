#NMNIST数据集中有错误，所以要去重。
from brian2 import *
import tonic
np.set_printoptions(threshold=2000)
start=time.time()
print(start)
run_time=1*second
tau=0.5*ms
dataset = tonic.datasets.NMNIST(save_to='./data', train=True)
events, target = dataset[0]
t=[]
zuobiao=[]
s=[]
chongfu=0
cf=[]
t_index=0
xunhuan=0
reliang=np.zeros((34,34))
#连接画图
def visualise_connectivity(S):
  Ns = len(S.source)
  Nt = len(S.target)
  figure(figsize=(10, 4))
  subplot(121)
  plot(zeros(Ns), arange(Ns), 'ok', ms=10)
  plot(ones(Nt), arange(Nt), 'ok', ms=10)
  for i, j in zip(S.i, S.j):
    plot([0, 1], [i, j], '-k')
  xticks([0, 1], ['Source', 'Target'])
  ylabel('Neuron index')
  xlim(-0.1, 1.1)
  ylim(-1, max(Ns, Nt))
  subplot(122)
  plot(S.i, S.j, 'ok')
  xlim(-1, Ns)
  ylim(-1, Nt)
  xlabel('Source neuron index')
  ylabel('Target neuron index')

#读取数据
for i in range(5028):
  if events[i][3] != 0:
    x=events[i][0]
    y=events[i][1]
    zuobiao.append(x+y*34)
    t.append(int(events[i][2]*0.01))
    s.append(events[i][3])


#去重
for i in t[:]:
  if i== 1486:
    print(1)
  if t.count(i)>1:
    chongfu=t.count(i)
    t_index=t.index(i)
    if chongfu>0:
      xunhuan=xunhuan+1
    if xunhuan==chongfu:
      for j in zuobiao[t_index:t_index+xunhuan]:
        cf.append(j)
      for k in cf[:]:
        if cf.count(k)>1:
          zuobiao.pop(t_index+cf.index(k))
          t.pop(t_index + cf.index(k))
          cf.pop(cf.index(k))
      cf=[]
      xunhuan=0

#连接数组
lianjie1=[]
r_ange=1
h=np.zeros((1,1156))
hh1=np.zeros((1,1156))
hh2=np.zeros((1,1156))
hh3=np.zeros((1,1156))
hh4=np.zeros((1,1156))
for i in range(len(t)):
  h[0,zuobiao[i]]=h[0,zuobiao[i]]+1
for i in range(1080):
  if (h[0,i]-r_ange<h[0,i+35]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+70]<h[0,i]+r_ange):
    hh1[0,i]=1
  if (h[0,i]-r_ange<h[0,i+34]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+68]<h[0,i]+r_ange):
    hh2[0,i]=1
  if (h[0,i]-r_ange<h[0,i+33]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+66]<h[0,i]+r_ange):
    hh3[0,i]=1
  if (h[0,i]-r_ange<h[0,i+1]<h[0,i]+r_ange) & (h[0,i]-r_ange<h[0,i+2]<h[0,i]+r_ange):
    hh4[0,i]=1
for i in range(1156):
  if (hh1[0,i]==1) or (hh2[0,i]==1) or (hh3[0,i]==1) or (hh4[0,i]==1) :
    hh1[0,i]=1
hh1=hh1.reshape(34,34)
imshow(hh1, cmap='gray', interpolation='nearest')
# hh1=hh1.reshape(34,34)
# hh2=hh2.reshape(34,34)
# hh3=hh3.reshape(34,34)
# hh4=hh4.reshape(34,34)
# subplot(221)
# imshow(hh1, cmap='gray', interpolation='nearest')
# subplot(222)
# imshow(hh2, cmap='gray', interpolation='nearest')
# subplot(223)
# imshow(hh3, cmap='gray', interpolation='nearest')
# subplot(224)
# imshow(hh4, cmap='gray', interpolation='nearest')
##连接
juzhen=np.zeros((1156,1156))
for i in range(1000):
  juzhen[i][i]=1
  juzhen[i][i+35]=1
  juzhen[i][i+70]=1

sources, targets = juzhen.nonzero()

for i in range(len(t)):
  reliang[zuobiao[i]%34,int(zuobiao[i]/34)]= reliang[zuobiao[i]%34,int(zuobiao[i]/34)]+1
for i in range(len(t)):
  t[i] = t[i] * 0.1 * ms

# zuobiaonp=np.array(zuobiao)
# tnp=np.array(t)*us
# ooo=np.ones([300])
# bbb=np.array([x for x in range(300)])*ms
d=SpikeGeneratorGroup(1156,zuobiao,t)
######要考虑shishi3的情况
G=NeuronGroup(1156,'dv/dt=(-v)/tau:1',threshold='v>0.1', reset='v = 0', refractory = 0.5*ms,method='exact')
S = Synapses(d,G,'w:1',on_pre='v_post +=0.2')
S.connect(i=sources,j=targets)
S.w=0.5
M=SpikeMonitor(d)
M1=SpikeMonitor(G)
M2=StateMonitor(G,'v',record=True)
run(run_time)
end=time.time()
print(end)
# subplot(311)
# plot(M.t/ms,M.i,'.k')
# subplot(312)
# for i in range(50):
#   plot(M2.t/ms,M2.v[i])
# print(M.count == M1.count)
# subplot(313)
# visualise_connectivity(S)
show()
















