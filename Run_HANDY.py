#! /usr/bin/env python

""" This is a Saturday-Morning-just-for-kicks implementation
 of the HANDY model for economic collapse.

 See "A Minimal Model for Human and Nature Interaction",
 Safa Motesharrei, Jorge Rivas, Eugenia Kalnay,
 November 13, 2012"""

import sys
import os
import matplotlib.pyplot as plt
from HANDY import Model as HANDY


def main():
    """ Main loop for code execution"""

    model = HANDY(fname=sys.argv[1])
    XC, XE, N, W = model.run_auto(norm=True)

    plt.plot(range(len(XC)), XC, label="Commoner Population", color='b')
    plt.plot(range(len(XE)), XE, label="Elite Population", color='r')
    plt.plot(range(len(N)), N, label="Nature", color='g')
    plt.plot(range(len(W)), W, label="Weatlth", color='k')
    plt.legend()
    plt.savefig('.'.join(sys.argv[1].split('.')[:-1])+'.pdf')
    os.system("open " + '.'.join(sys.argv[1].split('.')[:-1])+'.pdf')


if __name__ == '__main__':
    main()
