import matplotlib.pyplot as plt
import matplotlib
import pandas
matplotlib.use('TkAgg')
import seaborn

def plot(data, selections=None, **kwargs):

    if not selections:
        selections = data.colnames
        selections = [i for i in selections if i not in ['time']]
    else:
        assert isinstance(selections, list)

    df = pandas.DataFrame(data, columns=data.colnames)
    df = df[selections]

    fig = plt.figure()

    if kwargs.get('title'):
        plt.title(kwargs['title'])

    for i in selections:
        plt.plot(data['time'], df[i], label=i)

    plt.legend(loc='best')
    # plt.legend(loc=(1, 0.1))
    seaborn.despine(fig=fig, top=True, right=True)
    plt.xlabel('Time(s)')
    plt.ylabel('Concentration nmol/ml')


FUNCTIONS = """

function MM(km, Vmax, S)
        Vmax * S / (km + S)
    end

    function MMWithKcat(km, kcat, S, E)
        kcat * E * S / (km + S)
    end

    function NonCompetitiveInhibition(km, ki, Vmax, n, I, S)
        Vmax * S / ( (km + S) * (1 + (I / ki)^n ) )
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
        (kcat * E * S) / (km + S + ((km * I )/ ki)  )
    end    

    function CompetitiveInhibition(Vmax, km, ki, I, S)
        Vmax * S / (km + S + ((km * I )/ ki)  )
    end

    function Hill(km, beta, n, X)
        beta * X^n / (km*n + X*n)
    end

    function HillWithKcat(km, kcat, n, X, E)
        kcat*E* X^n / (km*n + X*n)
    end
"""


def list_attrs(x):
    for i in sorted(dir(x)):
        print(i)