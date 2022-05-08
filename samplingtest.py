import numpy as np
import matplotlib.pyplot as plt
w = np.random.randn(300).reshape(100,3)
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(w[:,0],w[:,1],w[:,2])
plt.show()
