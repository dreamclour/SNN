# longlonglonglong
#这个文件包含了一些画图的讲解
from brian2 import *

N = 10
G = NeuronGroup(N, 'v:1')
S = Synapses(G, G)
S.connect(condition='i!=j', p=0.2)
def visualise_connectivity(S):
  Ns = len(S.source)
  Nt = len(S.target)
  figure(figsize=(10, 4))#指定宽和高
  subplot(221)#分格函数
  plot(zeros(Ns), arange(Ns), 'ok', ms=10)
  plot(ones(Nt), arange(Nt), 'ok', ms=10)#ms尺寸
  for i, j in zip(S.i, S.j):
    plot([0, 1], [i, j], '-k')
  xticks([0, 1], ['Source', 'Target'])
  ylabel('Neuron index')
  xlim(-0.1, 1.1)
  ylim(-1, max(Ns, Nt))
  subplot(212)
  plot(S.i, S.j, 'ok')
  xlim(-1, Ns)
  ylim(-1, Nt)
  xlabel('Source neuron index')
  ylabel('Target neuron index')
  show()

visualise_connectivity(S)