# longlonglonglong
#不使用ge了，直接将240分成16份，因为不需要抑制
#先试试只用风车神经元不用视锥视杆
#如果膝状体接收视觉细胞一手信息，视觉皮层是二手2，然后反馈膝状体，这之间的联系是什么，论文，也许真的像cnn呢，每个视觉皮层都是碎片的特征
import numpy as np
from brian2 import *
#在50ms之内激活次数
run_time=50*ms
tau=10*ms
taum,taue,taui=2*ms,3*ms,3*ms
kk = np.linspace(1,9,17)
qq = np.linspace(1,9,17)
vv = np.linspace(1,9,17)
eqs='''
dv/dt=(I-v)/tau :1(unless refractory)
I:1
'''

eqs2 = '''
dv/dt  = (ge+gi-v)/taum : 1 (unless refractory)
dge/dt = -ge/taue : 1
dgi/dt = -gi/taui : 1
'''

# for l1 in kk:
#     for l2 in qq:
#         for l3 in vv:
#             G = NeuronGroup(3, eqs, threshold='v>1', reset='v = 0', refractory = 0.5*ms,method='exact')
#             G2= NeuronGroup(1, eqs2, threshold='v>3', reset='v = 0', refractory = 0.5*ms,method='exact')
#             G.I[0] = l1
#             G.I[1] = l2
#             G.I[2] = l3
#             S=Synapses(G,G2,'w:1',on_pre='ge += w')
#             S.connect()
#             S.w=1
#             M=StateMonitor(G,'v',record=True)
#             M_G_spike=SpikeMonitor(G)
#             M_G2_spike = SpikeMonitor(G2)
#             run(run_time)
#             #plot(M.t/ms,M.v[0])
#             #print('G_spike%d' %len(M_G_spike.i))
#             print('l1:%d\tl2:%d\tl3:%d\t' %(l1,l2,l3))
#             print('G2_spike%d\n' % (len(M_G2_spike.i)))
#             show()

G = NeuronGroup(3, eqs, threshold='v>1', reset='v = 0', refractory=0.5 * ms, method='exact')
G2 = NeuronGroup(1, eqs2, threshold='v>3', reset='v = 0', refractory=0.5 * ms, method='exact')
G.I[0] = 8
G.I[1] = 8
G.I[2] = 8
S = Synapses(G, G2, 'w:1', on_pre='ge += w')
S.connect()
S.w = 1
M = StateMonitor(G, 'v', record=True)
M_G_spike = SpikeMonitor(G)
M_G2_spike = SpikeMonitor(G2)
M_G2_state=StateMonitor(G2,['v','ge'],record=True)
run(run_time)
subplot(311)
plot(M.t/ms,M.v[0],label='M_v')
legend()
print('G_spike%d' % len(M_G_spike.i))
print('G2_spike%d' % len(M_G2_spike.i))
subplot(312)
plot(M_G2_state.t/ms,M_G2_state.v[0],label='M_G2_state_v')
legend()
subplot(313)
plot(M_G2_state.t/ms,M_G2_state.ge[0],label='M_G2_state_ge')
legend()
show()






