# longlonglonglong
from brian2 import *
P = PoissonGroup(10, 10*Hz)
M=SpikeMonitor(P)
run(100*ms)
plot(M.t/ms,M.i,'.k')
show()


