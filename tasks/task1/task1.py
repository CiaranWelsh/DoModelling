import tellurium as te
import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import matplotlib

matplotlib.use('Qt5Agg')
seaborn.set_context(context='talk')


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
    k3 = 0.1;
    k4 = 0.1;
    k5 = 0.1;
    k6 = 0.1;
    k7 = 0.1;
    
    R1: => A ; cell * k1;
    R2: A => ; cell * A * k2
    R3: A => B ; cell * k3*A*S;
    R4: B => A ; cell * k4*B;
    R5: B => ; cell * k5*B*C;
    R6: => C ; cell * k6*B;
    R7: C => ; cell * k7*C;
    
end

"""


def sim_without_s():
    model = te.loada(ant)
    model.S = 0
    sim = model.simulate(0, 100, 101)

    fig = plt.figure()
    plt.plot(sim['time'], sim[:, 1], label='A')
    plt.plot(sim['time'], sim[:, 2], label='B')
    plt.plot(sim['time'], sim[:, 3], label='C')

    plt.legend(loc='best')
    seaborn.despine(fig=fig, top=True, right=True)
    plt.title('S=0')
    plt.xlabel('Time (s)')
    plt.ylabel('Concentration (nmol/ml)')
    fname = os.path.join(figures_dir, 'WithoutS.png')
    plt.savefig(fname, bbox_inches='tight', dpi=200)
    return fig

def sim_with_s():
    model = te.loada(ant)
    model.S = 1
    sim = model.simulate(0, 100, 101)

    fig = plt.figure()
    plt.plot(sim['time'], sim[:, 1], label='A')
    plt.plot(sim['time'], sim[:, 2], label='B')
    plt.plot(sim['time'], sim[:, 3], label='C')

    plt.legend(loc='best')
    plt.title('S=1')
    plt.xlabel('Time (s)')
    plt.ylabel('Concentration (nmol/ml)')
    seaborn.despine(fig=fig, top=True, right=True)
    fname = os.path.join(figures_dir, 'WithS.png')
    plt.savefig(fname, bbox_inches='tight', dpi=200)
    return fig

if __name__ == '__main__':
    wd = os.path.dirname(__file__)
    figures_dir = os.path.join(wd, 'figures')

    sim_without_s()
    sim_with_s()



