import tellurium as te
import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

import matplotlib

matplotlib.use('Qt5Agg')

ant = """
model model1
    compartment cell = 1
    A in cell
    B in cell 
    C in cell
    
    A = 0;
    B = 0;
    C = 0;
    S = 0;
    
    k1 = 0.1;
    k2 = 0.1;
    k3f = 0.1;
    k3b = 0.1;
    k3 = 0.1;
    k4 = 0.1;
    k5 = 0.1;
    k6 = 0.1; 
    
    R1: => A ; cell * k1;
    R2: A => ; cell * A * k2
    R3: A => B ; cell * k3f*A*S;
    R4: B => A ; cell * k3b*B;
    R5: B => ; cell * k4*B*C;
    R6: => C ; cell * k5*B;
    R7: C => ; cell * k6*C;
    
end

"""

model = te.loada(ant)

sim = model.simulate(0, 100, 101)

fig = plt.figure()
plt.plot(sim['time'], sim[:, 1], label='A')
plt.plot(sim['time'], sim[:, 2], label='B')
plt.plot(sim['time'], sim[:, 3], label='C')

plt.legend(loc='best')
seaborn.despine(fig=fig, top=True, right=True)
plt.show()
