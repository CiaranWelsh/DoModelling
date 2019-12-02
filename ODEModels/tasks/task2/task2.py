import tellurium as te
import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import matplotlib
import sys
sys.path.append('..')
from functions import FUNCTIONS
import pandas

matplotlib.use('Qt5Agg')
seaborn.set_context(context='talk')


ant = f"""

{FUNCTIONS}

model model1
    compartment cell = 1
    A in cell
    B in cell 
    C in cell

    A = 0;
    B = 0;
    C = 0;
    D = 5;
    E = 0;
    F = 0;
    G = 0;
    S = 1;
    I1 = 0;
    I2 = 0;

    k1       = 0.05;
    k2       = 0.25;
    r3vmax   = 93;
    r3km     = 125;
    r3ki     = 0.01;
    r4km     = 155;
    r4vmax   = 355;
    r4km     = 35;
    r4ki     = 0.001;
    r5vmax   = 50;
    r5km     = 35;
    r5ki     = 0.05;
    r6km     = 95;
    v6vmax   = 45;
    k7       = 30;
    k8       = 1;
    k9       = 30;
    k10      = 1;
    k11      = 5;
    k12      = 5;
    k13km    = 10;
    k13beta  = 50;
    k13n     = 2;
    k14km    = 40;
    k14kcat  = 250;

    R1 : => A ; k1*S;
    R2 : A => ; k2*A;
    R3 : A => B; CompetitiveInhibition(r3vmax, r3km, r3ki, I1, A);
    R4 : B => A; MM(r4km, r4vmax, B);
    R5 : A => C; CompetitiveInhibition(r5vmax, r5km, r5ki, I2, A);
    R6 : C => A; MM(r6km, v6vmax, C);
    R7 : B + D => E; MA2(k7, B, D);
    R8 : E => B + D; MA1(k8, E);
    R9 : C + D => F; MA2(k9, C, D);
    R10: F => C + D; MA1(k10, F);
    R11: E => ; MA1(k11, E);
    R12: F => ; MA1(k12, F);
    R13: => G ; Hill(k13km, k13beta, k13n, E);
    R14: G => ; MMWithKcat(k14km, k14kcat, G, F);

end

"""


# model = te.loada(ant)
# sim = model.simulate(0, 1000, 101)
#
#
# print(sim.colnames)



# plot(sim, selections=['[A]', '[B]', '[C]'])
# plot(sim, selections=['[E]', '[F]'])
# plot(sim, selections=['[D]'])
# plot(sim, selections=['[G]'])
#
# plt.show()



model2b = f"""

{FUNCTIONS}

model model2b
    compartment cell = 1
    A in cell
    B in cell 
    C in cell

    A = 50;
    B = 35;
    C = 10;
    Ap = 0;
    Bp = 0;
    Cp = 0;
    I = 0;
    S = 1;
    
    r1km        = 60;
    r1kcat      = 0.5;
    r1n         = 2;
    r2km        = 30;
    r2kcat      = 4;
    r3vmax      = 50;
    r3km        = 90;
    r3ki        = 0.5;
    r3kcat      = 0.5;
    r4km        = 30;
    r4vmax      = 5;
    r5km       = 50;
    r5kcat     = 0.5;
    r6km        = 60;
    r6vmax      = 3.5;

    
    R1 : A => Ap ;  HillWithKcat(r1km, r1kcat, r1n, A, S); 
    R2 : Ap => A ;  MMWithKcat(r2km, r2kcat, Ap, Cp);
    R3 : B => Bp ;  CompetitiveInhibitionWithKcat(r3km, r3ki, r3kcat, Ap, I, B);
    R4 : Bp => B ;  MM(r4km, r4vmax, Bp);
    R5 : C => Cp ;  MMWithKcat(r5km, r5kcat, C, Bp)
    R6 : Cp => C ;  MM(r6km, r6vmax, Cp);
    
end

"""


model = te.loada(model2b)
# sim = model.simulate(0, 30, 300)


# plot(sim, selections=['[Ap]', '[Bp]', '[Cp]'])
# plot(sim, selections=['[Ap]', '[A]'])
# plot(sim, selections=['[Bp]', '[B]'])
# plot(sim, selections=['[Cp]', '[C]'])

# plt.show()


# dct = {}
# for i in [0.01, 0.1, 1, 10]:
#     model.S = i
#     sim_data = model.simulate(0, 60*60*24, 1000)
#     df = pandas.DataFrame(sim_data, columns=sim_data.colnames)
#     df = df[['time', '[Ap]']]
#     dct[i] = df.loc[1, '[Ap]']
    # plot(sim_data, selections=['[Ap]'])
    # df = df.iloc[1:, 1:]
    # dct[i] = df.loc[1].values
#
# print(dct)

# model.S = 1

# for i in [0.0001, 0.001, 0.005, 0.01]:
#     model.S = i
#     model.I = 0.1
#     sim_data = model.simulate(0, 20, 100)
#
#     plot(sim_data, selections=['[Ap]', '[Bp]', '[Cp]'])
#
# plt.show()
dct = {}
#s I
for i in [0.1, 1]:
    dct[i] = {}
    for j in [0, 1]:
        model.S = i
        model.I = j
        sim_data = model.simulate(0, 25, 51)
        dct[i][j] = pandas.DataFrame(sim_data, columns=sim_data.colnames)
        # plot(sim_data, selections=['[Ap]', '[Bp]', '[Cp]'], title=(i, j))
        model.reset()
    dct[i] = pandas.concat(dct[i])

plt.show()

df = pandas.concat(dct)
df.index = df.index.droplevel(2)
df.index.names = ['S', 'I']
df = df.reset_index().set_index(['S', 'I', 'time'])
print(df)
fname = 'task2_experimental_data.csv'
df.to_csv(fname)



