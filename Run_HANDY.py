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
    for fname in sys.argv[1:]:
        model = HANDY(fname=fname)
        XC, XE, N, W = model.run_auto(norm=True)

        plt.plot(range(len(XC)), XC, label="Commoner Population", color='b')
        plt.plot(range(len(XE)), XE, label="Elite Population", color='r')
        plt.plot(range(len(N)), N, label="Nature", color='g')
        plt.plot(range(len(W)), W, label="Weatlth", color='k')
        plt.legend()
        plt.savefig('.'.join(fname.split('.')[:-1])+'.pdf')
        plt.close()
        os.system("open " + '.'.join(fname.split('.')[:-1])+'.pdf')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Provide a parameter file."
        print "Ex: ./Run_HANDY.py HANDY_params_default.txt"
        print "If multiple files are given, they will be run",
        print "sequentially"
    main()
