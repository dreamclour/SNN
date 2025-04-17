# longlonglonglong
from brian2 import *
taupre = taupost = 20*ms
wmax = 2
Apre = 0.01
Apost = -Apre*taupre/taupost*1.05
tau=10*ms

def visualise_connectivity(S):
  Ns = len(S.source)
  Nt = len(S.target)
  figure(figsize=(10, 4))
  subplot(121)
  plot(zeros(Ns), arange(Ns), 'ok', ms=10)
  plot(ones(Nt), arange(Nt), 'ok', ms=10)
  for i, j in zip(S.i, S.j):
    plot([0, 1], [i, j], '-k')
  xticks([0, 1], ['Source', 'Target'])
  ylabel('Neuron index')
  xlim(-0.1, 1.1)
  ylim(-1, max(Ns, Nt))
  subplot(122)
  plot(S.i, S.j, 'ok')
  xlim(-1, Ns)
  ylim(-1, Nt)
  xlabel('Source neuron index')
  ylabel('Target neuron index')



P = PoissonGroup(1, rates=100*Hz)
G = NeuronGroup(1, 'dv/dt=(-v)/tau:1 (unless refractory)', threshold='v>0.5',reset='v = 0',refractory=2*ms,method='euler')

S = Synapses(P, G,
             '''
             w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             v_post += w
             apre += Apre
             w = clip(w+apost, -wmax, wmax)
             ''',
             on_post='''
             apost += Apost
             w = clip(w+apre, -wmax, wmax)
             ''', method='linear')
S.connect()
S.w=0.5
M1 = StateMonitor(S, ['w', 'apre', 'apost'], record=True)
M2 = StateMonitor(G,'v',record=True)
M3=SpikeMonitor(G)
run(50*ms)
#visualise_connectivity(S)

subplot(311)
plot(M1.t/ms, M1.apre[0], label='apre')
plot(M1.t/ms, M1.apost[0], label='apost')
legend()
subplot(312)
plot(M1.t/ms, M1.w[0], label='w')
legend(loc='best')
xlabel('Time (ms)')
subplot(313)
y=[]
plot(M2.t/ms, M2.v[0])
# for i in range(len(M2.t)):
#   for j in range(len(M3.t)):
#     if M2.t[i]==M3.t:
#       y.append(M2.t[0][i])
# print(y)
# print(M1.w[0])
# print('-------------------------------------------------------------------')
# for i in range(len(M3.t)):
#   k=int(M3.t[i]*10/ms)
#   print(M1.w[0][k])
#   print('============================================================================================================')


show()