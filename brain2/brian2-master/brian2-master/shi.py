# longlonglonglong
#lianjie:先连成1比1的连接，后面再改
#stdp
#1.2把泊松的值存储到一个列表里，这样就不用每次更新网络了，添加了stdp
#调试了不同tau的神经元的激活，tau越大神经元回到初始值的速度越慢，tau越小恢复初值的速度越快
from brian2 import *
start=time.time()
print(start)
tau=0.1*ms
run_time=0.2*second
eqs1='''
dv/dt=(2-v)/(10*ms) :1 (unless refractory)
'''
eqs2='''
dv/dt=(-v)/tau :1 (unless refractory)
tau: second
'''
#P=PoissonGroup(10,rates='100*Hz')
G1=NeuronGroup(3,eqs1,threshold='v>1',refractory=20*ms,reset='v=0',method='exact')
G2=NeuronGroup(4,eqs2,threshold='v>1',refractory=20*ms,reset='v=0',method='exact')
G2.tau=[0.1,10,1000,2000]*ms
S=Synapses(G1,G2,on_pre='v_post += 0.1')
S.connect()
M1=StateMonitor(G1,'v',record=True)
M2=StateMonitor(G2,'v',record=True)
run(run_time)
subplot(311)
plot(M1.t/ms,M1.v[0])
subplot(312)
plot(M1.t/ms,M1.v[1])
subplot(313)
plot(M2.t/ms,M2.v[0],'red')
plot(M2.t/ms,M2.v[1],'blue')
plot(M2.t/ms,M2.v[2],'yellow')
plot(M2.t/ms,M2.v[3],'black')
show()






