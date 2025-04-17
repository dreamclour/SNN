from brian2 import *
duration = 50*ms
tau = 10*ms
taum,taue,taui = 20*ms,5*ms,10*ms
eqs1 = '''
dv/dt = (2-v)/tau : 1(unless refractory)
'''
eqs2 = '''
dv/dt  = (ge+gi-v)/taum : volt (unless refractory)
dge/dt = -ge/taue : volt
dgi/dt = -gi/taui : volt
'''
# group1 = NeuronGroup(1, eqs1, threshold='v >= 1', reset='v = 0',
#                     refractory=5*ms, method='exact')
# group2 = NeuronGroup(10, eqs2, threshold='v >= 1*mV', reset='v = 0*mV',
#                     refractory=5*ms, method='exact')

G1 = NeuronGroup(1, eqs1, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G2 = NeuronGroup(10, eqs2, threshold='v>1*mV', reset='v = 0*mV', refractory = 1.5*ms,method='exact')

# group.v0 = -70*mV
# S=Synapses(group1,group2,'w:1',on_pre='ge -= w*mV')
# S.connect()
# S.w=1

S=Synapses(G1,G2,'w:1',on_pre='ge+=w*mV')
S.connect()
S.w=9


monitor1 = StateMonitor(G1,'v',record=0)
monitor2 = StateMonitor(G2,'v',record=True)
#monitor2=SpikeMonitor(group2)
monitor3 = StateMonitor(G2,'ge',record=0)
run(duration)
# subplot(311)
# plot(monitor1.t/ms, monitor1.v[0])
# subplot(312)
# plot(monitor2.t/ms, monitor2.v[0])
# #plot(monitor2.t/ms,monitor2.i)
# subplot(313)
# plot(monitor3.t/ms, monitor3.ge[0])
# show()
print(monitor2.v[0])




########################################################
#-70--60
# tau = 10*ms
# eqs = '''
# dv/dt = (-80*mV-v)/tau : volt(unless refractory)
# '''
#
# G = NeuronGroup(1, eqs, threshold='v>-60*mV', reset='v = -70*mV', method='exact')
# G.v=-70*mV
# M = StateMonitor(G, 'v', record=0)
# run(500*ms)
# plot(M.t/ms, M.v[0])
# xlabel('Time (ms)')
# ylabel('v')
# show()




