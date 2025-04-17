# longlonglonglong
import time

from brian2 import *
start=time.time()
print(start)
num_inputs=100
input_rate=10*Hz
weight=0.1
tau_range=linspace(1,10,30)*ms
output_rates=[]
P=PoissonGroup(num_inputs,rates=input_rate)
eqs='''
dv/dt=-v/tau :1
'''
G=NeuronGroup(1,eqs,threshold='v>1',reset='v=0',method='exact')
S=Synapses(P,G,on_pre='v+=weight')
S.connect()
M=SpikeMonitor(G)
store()
for tau in tau_range:
    restore()
    run(1*second)
    output_rates.append(M.num_spikes/second)
plot(tau_range/ms,output_rates)
xlabel(r'$/tau$(ms)')
ylabel('Firing rate(sp/s)')
end=time.time()
print(end)

show()



















