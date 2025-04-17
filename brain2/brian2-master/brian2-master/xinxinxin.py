# longlonglonglong
from brian2 import *
def get_picture(load_path):
  img = (imread(load_path))
  return img
img=get_picture('D:/happy new year/picture2/3.jpg')
img1=((img.flatten())/25)
print(img1)
long = [list(img1)]
stimulus = TimedArray(long*Hz, dt=3*ms)
P = PoissonGroup(784, rates='stimulus(t,i)')
M=SpikeMonitor(P)
run(1*second)
plot(M.t/ms,M.i,'.k')
show()







