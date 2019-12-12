import os, glob
import pandas as pd
import numpy as np
import tellurium as te
import site

site.addsitedir('/home/ncw135/Documents/QualitativeModelFitting')
site.addsitedir('/home/ncw135/Documents/pycotools3')
import pycotools3 as py3
import qualitative_model_fitting as qmf

model_string = """
function MM(km, Vmax, S)
    Vmax * S / (km + S)
end

function MMWithKcat(km, kcat, S, E)
    kcat * E * S / (km + S)
end

function NonCompetitiveInhibition(km, ki, Vmax, n, I, S)
    Vmax * S / ( (km + S) * (1 + (I / ki)^n ) )
end

function NonCompetitiveInhibitionWithKcat(km, ki, kcat, E, n, I, S)
    kcat * E * S / ( (km + S) * (1 + (I / ki)^n ) )
end

function NonCompetitiveInhibitionWithKcatAndExtraActivator(km, ki, kcat, E1, E2, n, I, S)
    kcat * E1 * E2 * S / ( (km + S) * (1 + (I / ki)^n ) )
end


function MA1(k, S)
    k * S
end

function MA2(k, S1, S2)
    k * S1 * S2
end

function MA1Mod(k, S, M)
    k * S * M
end

function MA2Mod(k, S1, S2, M)
    k * S1 * S2 * M
end

function CompetitiveInhibitionWithKcat(km, ki, kcat, E, I, S)
    kcat * E * S / (km + S + ((km * I )/ ki)  )
end

function CompetitiveInhibition(Vmax, km, ki, I, S)
    Vmax * S / (km + S + ((km * I )/ ki)  )
end

model Problem2
    
    // module 1
    R1f     : N -> pN                   ;   kNPhos*N*S;
    R1b     : pN -> N                   ;   kNDephos*pN*pD;
    R4f1    : G -> pG                   ;   kGPhos*G*pN;
    R4b     : pG -> G                   ;   kGDephos*pG;
    R6f     : G -> IG                   ;   kGBindI1*G*I1;
    R6b     : IG -> G                   ;   kGUnbindI1*IG;
    R7f     : K -> pK                   ;   kKPhos*K*pG*pN;
    R7b     : pK -> K                   ;   kKDephos*pK;
    // CompetitiveInhibition(Vmax, km, ki, I, S)
    R8f     : D -> pD                   ;   kDPhos*D*pK;
    R8b     : pD -> D                   ;   kDDephos*pD*K;
    R9f     : D -> DI                   ;   kDBindI2*D*I2;
    R9b     : DI -> D                   ;   kDUnbindI2*DI;
        
    // inputs 
    const S     = 0; 
    const I1     = 0; 
    const I2     = 0; 
    N           = 50   
    pN          = 0     
    G           = 50     
    pG          = 0     
    IG          = 0     
    K           = 50     
    pK          = 0     
    D           = 50
    pD          = 0
    DI          = 0
    kNPhos      = 0.1         
    kNDephos    = 0.05             
    kGPhos      = 0.001             
    kGDephos    = 0.1             
    kKPhos      = 0.0005         
    kKDephos    = 0.001             
    kDPhos      = 0.001         
    kDDephos    = 0.1
                 
    kGBindI1    = 10             
    kGUnbindI1  = 0.01   
    kDBindI2    = 10;          
    kDUnbindI2  = 0.01;          
end
"""

rr = te.loada(model_string)
site.addsitedir('..')

copasi_file = os.path.join(os.path.dirname(__file__), 'complex_model.cps')

mod = py3.model.loada(model_string, copasi_file)
mod = py3.tasks.TimeCourse(mod, start=0, end=250, step_size=0.1).model
# mod.open()

null_cond = dict(S=0, I1=0, I2=0)
S = dict(S=1, I1=0, I2=0)
SI1 = dict(S=1, I1=1, I2=0)
SI2 = dict(S=1, I1=0, I2=1)
SI = dict(S=1, I1=1, I2=1)

conditions = dict(
    S=S, SI1=SI1, SI2=SI2, SI=SI
)
# for k, v in zip(['S', 'SI1', 'SI2', 'SI'], [S, SI1, SI2, SI]):
ts = qmf.TimeSeries(model_string, conditions, 0, 120, 9)
# for k, v in ts.simulate().items():
#     fname = os.path.join(os.path.dirname(__file__), f'{k}.csv')
#     v = v[['pN', 'pG', 'pK', 'pD']]
#     v.to_csv(fname)


selection2 = {
    'pN': ['pN'],
    'pG': ['pG'],
    'pK': ['pK'],
    'pD': ['pD'],
}
import seaborn
seaborn.set_context('poster')
# fname = os.path.join(os.path.dirname(__file__, ), f'{k}.png')
for k, v in selection2.items():
    qmf.TimeSeriesPlotter(ts, plot_selection={k: v},
                          plot_dir=os.path.dirname(__file__), savefig=True,
                          fname=f'{k}.png',
                          conditions=['S', 'SI1', 'SI2', 'SI'],
                          ncols=2, legend_loc=(1, 0.1)).plot_with_conditions(
        ls="--", marker='x', markersize=15
    )
# for k, v in zip(['S', 'SI1', 'SI2', 'SI'], [S, SI1, SI2, SI]):
#     ts = qmf.TimeSeries(model_string, v, 0, 120, 9)
#     # for k, v in ts.simulate().items():
#     #     fname = os.path.join(os.path.dirname(__file__), f'{k}.csv')
#     #     v = v[['pN', 'pG', 'pK', 'pD']]
#     #     v.to_csv(fname)
#
#
#     selection2 = {
#         'N': ['N', 'pN'],
#         'G': ['G', 'pG'],
#         'K': ['K', 'pK'],
#         'D': ['D', 'pD'],
#     }
#     fname = os.path.join(os.path.dirname(__file__, ), f'{k}.png')
#     qmf.TimeSeriesPlotter(ts, plot_selection=selection2,
#                           plot_dir=os.path.dirname(__file__), savefig=True, fname=f'{k}.png',
#                           # conditions=['Off', 'SOn', 'IOn', 'SIOn'],
#                           ncols=2).plot(
#         ls="-",  # marker='.'
#     )
# # data = rr.simulate(0, 100, 11)
#
# print(ts)
