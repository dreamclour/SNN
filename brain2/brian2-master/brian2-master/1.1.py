# longlonglonglong
#stdp
from brian2 import *
start=time.time()
print(start)
num_inputs=100
input_rate=1*Hz

def get_picture(load_path):
  img = (imread(load_path))
  return img

img=get_picture('D:/happy new year/picture2/27.jpg')

img1=((img.flatten())/25)

for q in range(784):
  img1[q]=int(img1[q])
img1=img1*Hz
tt=[]


for u in range(200):
  P = PoissonGroup(200, img1[u])
  G = NeuronGroup(200, 'dv/dt = -v / (10*ms) : 1', threshold='v>1', reset='v=0', method='exact')
  S = Synapses(P, G, on_pre='v+=0.51')
  S.connect(j='i')
  M = SpikeMonitor(P)
  run(1*second)

  #tt.append(M.num_spikes/second)


plot(M.t/ms,M.i)
xlabel('Time/ms')
ylabel('V')

end=time.time()
print(end)
show()








