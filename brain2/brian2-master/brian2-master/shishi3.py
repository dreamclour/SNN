from brian2 import *
start=time.time()
print(start)

#参数
tau1 = 30*ms
run_time = 50*ms
taum2,taue2,taui2 = 20*ms,5*ms,10*ms

eqs1='''
dv/dt=(2-v)/tau1 :1(unless refractory)
'''
eqs2='''
dv/dt  = (ge2+gi2-v)/taum2 : volt (unless refractory)
dge2/dt = -ge2/taue2 : volt
dgi2/dt = -gi2/taui2 : volt
'''

G1 = NeuronGroup(1, eqs1, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G2 = NeuronGroup(10, eqs2, threshold='v>1*mV', reset='v = 0*mV', refractory = 1.5*ms,method='exact')
#G3 = NeuronGroup(1, 'dv/dt=-v:1', threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')

S=Synapses(G1,G2,'w:1',on_pre='ge2+=w*mV')
S.connect()
S.w=9

M=SpikeMonitor(G1)
M_state=StateMonitor(G2,'v',record=True)
run(run_time)
subplot(211)
plot(M_state.t/ms,M_state.v[0],label='G2')
subplot(212)
plot(M.t/ms,M.i,'.k',color='b',label='G1')
print(G2.i)
plt.show()



