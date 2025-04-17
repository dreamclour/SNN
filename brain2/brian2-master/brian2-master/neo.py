from brian2 import *
start=time.time()
print('start:',start)

v0_max=3.
duration=1000*ms
tau=10*ms
N=100
eqs='''
dv/dt=(v0-v)/tau : 1(unless refractory)
v0:1
'''

G=NeuronGroup(N,eqs,threshold='v>1',reset='v=0',refractory=5*ms,method='exact')

G.v0='i*v0_max/(N-1)'
spikemon=SpikeMonitor(G)
run(duration)


figure(figsize=(12,4))
subplot(121)
plot(spikemon.t/ms, spikemon.i, '.k')
xlabel('Time(ms)')
ylabel('Neuron Index')
subplot(122)
plot(G.v0,spikemon.count/duration)
xlabel('v0')
ylabel('firing rate(sp/s)')

end=time.time()
print('end:',end)
show()







