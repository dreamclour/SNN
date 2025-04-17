from brian2 import *
#在里面的函数写的非常具有迷惑性，只有prepost两个同时存在才会更新权重，单独的激活并不影响权重。

taupre=taupost=20*ms
wmax=0.01
Apre=0.01
Apost=-Apre*taupre/taupost*1.05

G=NeuronGroup(2,'v:1',threshold='t>(1+i)*10*ms',refractory=100*ms)

S=Synapses(G,G,
          '''
          w:1
          dapre/dt=-apre/taupre :1
          dapost/dt=-apost/taupost :1         
          ''',
          on_pre='''

          apre+=Apre
          w=clip(w+apost,0,wmax)
          ''',
          on_post='''
          apost+=Apost
          w=clip(w+apre,0,wmax)
          '''
           #在这里，相加的postpre和式子里的值相反，表示在权重上。
          ,method='linear'
           )

S.connect(i=0,j=1)
M=StateMonitor(S,['w','apre','apost'],record=True)

run(30*ms)
subplot(211)
plot(M.t/ms,M.apre[0],label='apre')
plot(M.t/ms,M.apost[0],label='apost')
#xlabel('time1/ms')
legend()
subplot(212)
plot(M.t/ms,M.w[0],label='w')
legend(loc='best')
xlabel('time2/ms')
show()







