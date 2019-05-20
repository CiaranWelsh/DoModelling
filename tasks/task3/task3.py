import tellurium as te
import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
from utils import FUNCTIONS, plot, list_attrs





model3a_ant = f"""

{FUNCTIONS}

model model3a
    compartment cell = 1;
    
    A in cell;
    B in cell;
    S1 in cell;
    S2 in cell;
    
    A = 50;
    B = 50;
    S1 = 0.1;
    S2 = 0.1;
    
    r1km    = 50;
    r1kcat  = 100;
    r2km    = 50;
    r2kcat  = 100;
    
    R1 : A => B ; MMWithKcat(r1km, r1kcat, A, S1);
    R2 : B => A ; MMWithKcat(r2km, r2kcat, B, S2);

end    

"""



model3a = te.loada(model3a_ant)
model3a.conservedMoeityAnalysis = True
# sim = model3a.simulate(0, 50, 100)
#
# plot(sim)
#
# print(sim)

# plt.show()


ss = model3a.getSteadyStateValues()
# indep vars:
s1 = [0, 0.001, 0.01, 0.1, 1]
s2 = [0, 0.001, 0.01, 0.1, 1]

# for i in sorted(dir(model3a)):
#     print(i)
dr1 = {}
for i in s1:
    model3a.reset()
    model3a.S1 = i
    ss = model3a.getSteadyStateValues()
    ss = model3a.steadyStateNamedArray()
    print(ss)
    dr1[i] = ss


# print(dr1)
print(list_attrs(ss))


# print(ss.rownamese)
















