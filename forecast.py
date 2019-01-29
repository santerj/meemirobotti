import numpy as np
import matplotlib.pyplot as plt
from random import randint


def forecast():

    multiplier = randint(1, 5)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 20)
    ax.set_ylim(0, multiplier*10)

    x = [0, 4, 8, 12, 16, 20]
    y = []

    for i in range(6):
        y.append(randint(1, 9) * multiplier)

    a = np.polyfit(x, y, randint(1, 5))
    p1 = np.poly1d(a)
    xp = np.linspace(0, 20, 100)
    plt.plot(xp, p1(xp), '-', color='red')

    x_labels = ('Aika (viikkoja)',
                'Aika (tunteja)',
                'Aika (minuutteja)'
                )

    y_labels = ('Promillet',
                'Känni',
                'Rahat',
                'Pulssi',
                'Ruumiinlämpö',
                'Tärinä',
                'Pärinä',
                'Verenkierto',
                'Opintopisteet',
                'Motivaatio',
                'Aivotoiminta',
                'Mayhem',
                'Sekoilu',
                'Vapina',
                'Menestys',
                'Vauhti'
                )

    # ax.set_yticklabels([])
    # ax.set_xticklabels([])

    x_label = x_labels[randint(0, len(x_labels)-1)]
    y_label = y_labels[randint(0, len(y_labels)-1)]

    ax.set(xlabel=x_label, ylabel=y_label, title='Ennuste')
    ax.grid()
    plt.savefig('ennuste.png')
