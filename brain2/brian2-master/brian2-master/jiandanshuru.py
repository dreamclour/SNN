# longlonglonglong
from brian2 import *
A=2.5
tau=5*ms
f=10*Hz
# t_recorded=arange(int(200*ms/defaultclock.dt))*defaultclock.dt
# I_recorded=TimedArray(A*sin(2*pi*f*t_recorded),dt=defaultclock.dt)

eqs='''
dv/dt=(I-v)/tau :1
I=A*sin(2*pi*f*t) :1
'''

G=NeuronGroup(1,eqs,threshold='v>1',reset='v=0',method='euler')
M=StateMonitor(G,variables=True,record=True)
run(200*ms)

plot(M.t/ms,M.v[0],label='v')
plot(M.t/ms,M.I[0],label='I')

xlabel('time/ms')
show()















