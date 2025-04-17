#1.3更改神经元

from brian2 import *
start=time.time()
print(start)
tau=10*ms
taupre = taupost = 20*ms
wmax = 1.2
Apre = 0.001
Apost = -Apre*taupre/taupost*1.05
run_time=5*second

def get_picture(load_path):
  img = (imread(load_path))
  return img

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

juzhen1=np.zeros((784,784))
juzhen2=np.array(())
juzhen3=np.array(())
juzhen4=np.array(())

for i in range(90):
  juzhen1[i][i]=1
  juzhen1[i+29][i]=1
  juzhen1[i+58][i]=1

sources, targets = juzhen1.nonzero()

img=get_picture('D:/happy new year/picture2/h.jpg')

img1=((img.flatten()))
for q in range(784):
  img1[q]=int(img1[q])
eqs = '''
dv/dt = -v/tau : 1(unless refractory)
'''
stimulus = TimedArray([img1]*Hz, dt=run_time)
P1 = PoissonGroup(300, rates='stimulus(t,i)')
G1_1 = NeuronGroup(150, eqs, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G1_2 = NeuronGroup(784, eqs, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G1_3 = NeuronGroup(784, eqs, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')
G1_4 = NeuronGroup(784, eqs, threshold='v>1', reset='v = 0', refractory = 1.5*ms,method='exact')


S_initial = np.random.uniform(low=0,high=0.7,size=(1,1))
S = Synapses(G1_1,G1_1,'w:1',on_pre='v_post +=0.01')
S.connect(i=sources,j=targets)
S.w = 0.5
M1 = StateMonitor(S, ['w', 'apre', 'apost'], record=True)
M2=SpikeMonitor(G1_1)
run(10*ms)
subplot(311)
plot(M1.t/ms, M1.apre[0], label='apre')
plot(M1.t/ms, M1.apost[0], label='apost')
legend()
subplot(312)
plot(M1.t/ms, M1.w[0], label='w')
legend()
subplot(313)
plot(M2.t/ms, M2.i, '.k',label='Neuron 0')
xlabel('Time (ms)')
ylabel('v')
legend()

#visualise_connectivity(S)
show()











