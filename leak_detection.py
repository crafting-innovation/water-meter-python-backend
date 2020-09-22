from PyEMD import EEMD 
import numpy  as np
t = np.linspace(0, 1, 200)
s = np.cos(11*2*np.pi*t*t) + 6*t*t
print(t,type(t))
