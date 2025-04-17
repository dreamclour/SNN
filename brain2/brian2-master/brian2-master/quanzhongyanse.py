# longlonglonglong
#后面做，使用scatter
from brian2 import *
N=10
G=NeuronGroup(N,'v:1')
S=Synapses(G,G)
S.connect(condition='i!=j', p=0.2)


def visualise_connectivity(S):
  Ns=len(S.source)
  Nt=len(S.target)
  figure(figsize=(10,4))
  subplot(121)
  plot(zeros(Ns),arange(Ns),'ok',ms=10)
  plot(ones(Nt),arange(Nt),'ok',ms=10)
  for i,j in zip(S.i,S.j):
    plot([0,1],[i,j],'-k')
  xticks([0, 1], ['Source', 'Target'])
  ylabel('Neuron index')
  xlim(-0.1, 1.1)
  ylim(-1,max(Ns,Nt))
  subplot(122)
  plot(S.i,S.j,'ok')
  xlabel('Source')
  ylabel('target')


visualise_connectivity(S)

show()





