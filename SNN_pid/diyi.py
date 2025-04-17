# longlonglonglong
#可训练的
import matplotlib.pyplot as plt
import nengo
from nengo.processes import Piecewise

model = nengo.Network(label="Integrator")
with model:
    # Our ensemble consists of 100 leaky integrate-and-fire neurons,
    # representing a one-dimensional signal
    A = nengo.Ensemble(100, dimensions=1)

with model:
  input = nengo.Node(Piecewise({0: 2}))

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

# Create our simulator
with nengo.Simulator(model) as sim:
    # Run it for 6 seconds
    sim.run(0.5)

plt.figure()
plt.plot(sim.trange(), sim.data[input_probe], label="Input")
plt.plot(sim.trange(), sim.data[A_probe], "k", label="Integrator output")

plt.legend()
plt.show()
print(sim.data[A_probe][-1])







