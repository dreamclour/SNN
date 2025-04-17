# longlonglonglong
from brian2 import *
num_inputs=100
input_rate=10*Hz
tau_range=linspace(1,10,30)*ms
P = PoissonGroup(num_inputs, rates=input_rate)
M=SpikeMonitor(P)
tt=[]
store()
for t in tau_range:
  restore()
  run(1*second)
  tt.append(M.num_spikes/second)

plot(arange(num_inputs),tt,'--C')
xlabel('Number')
ylabel('Hz')
show()








