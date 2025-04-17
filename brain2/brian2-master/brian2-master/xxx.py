from brian2 import *

eqs = '''
dv/dt = (I-v)/tau : volt
I : volt
tau : second
'''
G = NeuronGroup(3, eqs, threshold='v>1*mV', reset='v = 0*mV', method='exact')
G.I = [2, 0, 0]*mV
G.tau = [10, 100, 100]*ms

# Comment these two lines out to see what happens without Synapses
S = Synapses(G, G, 'w : 1', on_pre='v_post += w*mV')
S.connect(i=0, j=[1, 2])
S.w = [1,2]

M = StateMonitor(G, 'v', record=True)

run(50*ms)

plot(M.t/ms, M.v[0], label='Neuron 0')
plot(M.t/ms, M.v[1], label='Neuron 1')
plot(M.t/ms, M.v[2], label='Neuron 2')
xlabel('Time (ms)')
ylabel('v')
legend()
show()