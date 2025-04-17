# longlonglonglong
import snntorch as snn
from torch.utils.data import DataLoader
from snntorch.spikevision import spikedata
train_ds = spikedata.NMNIST("dataset/nmnist", train=True)
test_ds = spikedata.NMNIST("dataset/nmnist", train=False)





