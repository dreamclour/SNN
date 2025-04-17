# longlonglonglong
from brian2 import *
stimulus = TimedArray(np.tile([100., 0.], 5)*Hz, dt=100.*ms)
P = PoissonGroup(1, rates='stimulus(t)')
M=StateMonitor(P)
print(M.t/ms,M.i,'.k')
show()