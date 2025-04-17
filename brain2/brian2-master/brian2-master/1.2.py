#1.2使用timedArray，这样就不用每次更新网络了，添加了stdp
from brian2 import *
start=time.time()
print(start)
tau=10*ms
vt=1*mV
vr=0*mV
taupre = taupost = 20*ms
wmax = 1.2
Apre = 0.01
Apost = -Apre*taupre/taupost*1.05
run_time=500*ms

def get_picture(load_path):
  img = (imread(load_path))
  return img

img=get_picture('D:/happy new year/picture2/h.jpg')

img1=((img.flatten())*10)


for q in range(100):
  img1[q]=int(img1[q])


eqs = '''
dv/dt = -v/tau : volt(unless refractory)
'''

stimulus = TimedArray([img1]*Hz, dt=run_time)
P = PoissonGroup(7, rates='stimulus(t,i)')
G = NeuronGroup(7, eqs, threshold='v>vt', reset='v=vr', refractory = 1.5*ms,method='euler')
S_initial = np.random.uniform(low=0,high=0.1,size=(1,49))
S = Synapses(P,G,
             '''
             w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             v_post += w *mV
             apre += Apre
             w = clip(w+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost
             w = clip(w+apre, 0, wmax)
             ''')

S.connect()
S.w = 0.05
M1 = StateMonitor(S, ['w', 'apre', 'apost'], record=True)
M2=SpikeMonitor(G)
run(run_time)
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
end=time.time()
print(end)
show()











