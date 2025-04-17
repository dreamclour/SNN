import matplotlib.pyplot as plt
import nengo
from nengo.processes import Piecewise
import matplotlib.pyplot as plt
import numpy as np

Time_interval=0.5
a_error=0

model = nengo.Network(label="Integrator")
with model:
    # Our ensemble consists of 100 leaky integrate-and-fire neurons,
    # representing a one-dimensional signal
    A = nengo.Ensemble(100, dimensions=1)

with model:
  input = nengo.Node(Piecewise({0: a_error}))

  with model:
    # Connect the population to itself
    tau = 0.1
    nengo.Connection(
      A, A, transform=[[1]], synapse=tau
    )  # Using a long time constant for stability

    # Connect the input
    nengo.Connection(
      input, A, transform=[[tau]], synapse=tau
    )  # The same time constant as recurrent to make it more 'ideal'

  with model:
    # Add probes
    input_probe = nengo.Probe(input)
    A_probe = nengo.Probe(A, synapse=0.01)


class PositionPID(object):
  """位置式PID算法实现"""

  def __init__(self, target, cur_val, dt, max, min, p, i, d) -> None:
    self.dt = dt  # 循环时间间隔
    self._max = max  # 最大输出限制，规避过冲
    self._min = min  # 最小输出限制
    self.k_p = p  # 比例系数
    self.k_i = i  # 积分系数
    self.k_d = d  # 微分系数

    self.target = target  # 目标值
    self.cur_val = cur_val  # 算法当前PID位置值，第一次为设定的初始位置
    self._pre_error = 0  # t-1 时刻误差值
    self._integral = 0  # 误差积分值

  def calculate(self):
    """
    计算t时刻PID输出值cur_val
    """
    error = self.target - self.cur_val  # 计算当前误差
    a_error=error
    # 比例项
    p_out = self.k_p * error
    # 积分项
    # Create our simulator
    with nengo.Simulator(model) as sim:
      # Run it for 0.5 seconds
      sim.run(0.5)
    self._integral += (error * self.dt)
    i_out = self.k_i * 10*sim.data[A_probe][-1]
    #i_out = self.k_i * self._integral
    #i_out = self.k_i * 0
    print(a_error)
    # 微分项
    derivative = (error - self._pre_error) / self.dt
    d_out = self.k_d * derivative

    # t 时刻pid输出
    output = p_out + i_out + d_out

    # 限制输出值
    if output > self._max:
      output = self._max
    elif output < self._min:
      output = self._min

    self._pre_error = error
    self.cur_val += output
    return self.cur_val

  def fit_and_plot(self, count=50):
    """
    使用PID拟合setPoint
    """
    counts = np.arange(count)
    outputs = []
    outputs2 = []

    for i in counts:
      a=float(self.calculate())
      outputs2.append(a)
      print('Count %3d: output: %f' % (i, outputs2[-1]))

    print('Done')
    # print(outputs)
    print(outputs2)
    print(outputs)
    plt.figure()
    plt.axhline(self.target, c='red')
    plt.plot(counts, np.array(outputs2), 'b.')
    #plt.ylim(min(outputs) - 0.1 * min(outputs), max(outputs) + 0.1 * max(outputs))
    plt.plot(outputs2)

    plt.show()


pid = PositionPID(10, -5, 0.5, 100, -100, 0.2, 0.1, 0.01)
pid.fit_and_plot(50)



