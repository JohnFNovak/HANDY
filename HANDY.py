#! /usr/bin/env python

""" This is a Saturday-Morning-just-for-kicks implementation
 of the HANDY model for economic collapse.

 See "A Minimal Model for Human and Nature Interaction",
 Safa Motesharrei, Jorge Rivas, Eugenia Kalnay,
 November 13, 2012"""

import os


class Model():
    """ Base class for HANDY model"""
    def __init__(self, default=False, fname='', xc=1e2, xe=0, y=100, w=0,
                 am=1e-2, aM=7e-2, bc=3e-2, be=3e-2, g=1e-2, l=100, s=5e-4,
                 d=6.67e-6, k=0, r=5e-3, t=1000):
        if not default:
            self.load_params(fname)
        else:
            self.parameters = [am, aM, bc, be, g, l, s, d, k, r]
            self.metrics = [xc, xe, y, w]
            self.runtime = t

    def reset_params(self, xc=1e2, xe=0, y=100, w=0, am=1e-2, aM=7e-2, bc=3e-2,
                     be=3e-2, g=1e-2, l=100, s=5e-4, d=6.67e-6, k=0, r=5e-3,
                     t=1000):
        self.parameters = [am, aM, bc, be, g, l, s, d, k, r]
        self.metrics = [xc, xe, y, w]
        self.runtime = t

    def set_params(self, xc='', xe='', y='', w='', am='', aM='', bc='', be='',
                   g='', l='', s='', d='', k='', r='', t=''):

        Mam, MaM, Mbc, Mbe, Mg, Ml, Ms, Md, Mk, Mr = self.parameters
        Mxc, Mxe, My, Mw = self.metrics
        Mt = self.runtime

        if xc == '':
            xc = Mxc
        if xe == '':
            xe = Mxe
        if y == '':
            y = My
        if w == '':
            w = Mw
        if am == '':
            am = Mam
        if aM == '':
            aM = MaM
        if bc == '':
            bc = Mbc
        if be == '':
            be = Mbe
        if g == '':
            g = Mg
        if l == '':
            l = Ml
        if s == '':
            s = Ms
        if d == '':
            d = Md
        if k == '':
            k = Mk
        if r == '':
            r = Mr
        if t == '':
            t = Mt

        self.parameters = [am, aM, bc, be, g, l, s, d, k, r]
        self.metrics = [xc, xe, y, w]
        self.runtime = t

    def load_params(self, fname):
        """ Load model values from file"""

        data = {'t': 0}
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                for line in f:
                    pair = line.split()
                    data[pair[0]] = float(pair[1])
        else:
            print "File doesn't exist, ", fname, "exiting"
            exit(0)

        for k in data.keys():
            print k, data[k]

        xc = data['xc']  # initial commoner popultaion
        xe = data['xe']  # initial elite population
        y = data['y']  # inital amount of nature
        w = data['w']  # initial amount of wealth
        am = data['am']  # minimum death rate
        aM = data['aM']  # Maximal death rate
        bc = data['bc']  # commoner birth rate
        be = data['be']  # elite birth rate
        g = data['g']  # nature regeneration factor
        l = data['l']  # nature's capactiy
        s = data['s']  # subsistence salary (consumption)
        d = data['d']  # nature depletion factor
        k = data['k']  # difference in consumtion factor
        r = data['r']  # minimum required consumption

        self.runtime = int(data['t'])  # how long to run the simulation
        self.parameters = [am, aM, bc, be, g, l, s, d, k, r]
        self.metrics = [xc, xe, y, w]

    def update(self):
        """ Update loop for the HANDY model"""
        xc, xe, y, w = self.metrics
        am, aM, bc, be, g, l, s, d, k, r = self.parameters

        wth = (r * xc) + (k * r * xe)
        if not wth == 0:
            cc = min(1, w/wth) * s * xc
            ce = min(1, w/wth) * k * s * xe
        else:
            cc = s * xc
            ce = k * s * xe
        if not (s * xc) == 0:
            ac = am + (max(0, 1 - (cc / (s * xc))) * (aM - am))
        else:
            ac = am
        if not (s * xe) == 0:
            ae = am + (max(0, 1 - (ce / (s * xe))) * (aM - am))
        else:
            ae = am

        dxc = (bc * xc) - (ac * xc)
        dxe = (be * xe) - (ae * xe)
        dy = (g * y * (l - y)) - (d * xc * y)
        dw = (d * xc * y) - cc - ce

        xc = xc + dxc
        if xc < 0:
            xc = 0
        # if xc > 1e22:
            # xc = 1e22
        xe = xe + dxe
        if xe < 0:
            xe = 0
        # if xe > 1e22:
            # xe = 1e22
        y = y + dy
        if y < 0:
            y = 0
        # if y > 1e22:
            # y = 1e22
        w = dw + w
        if w < 0:
            w = 0
        # if w > 1e22:
            # w = 1e22
        self.metrics = [xc, xe, y, w]

        return [xc, xe, y, w]

    def run_auto(self, time=-1, norm=False):
        if time == -1:
            time = self.runtime
        if time == 0:
            time = 1000
        am, aM, bc, be, g, l, s, d, k, r = self.parameters

        XC = []
        XE = []
        N = []
        W = []
        for i in range(time):
            metrics = self.update()
            XC.append(metrics[0])
            XE.append(metrics[1])
            N.append(metrics[2])
            W.append(metrics[3])
        if norm:
            maxXC = max(XC)
            if not maxXC == 0:
                XC = map(lambda x: x/maxXC, XC)
            maxXE = max(XE)
            if not maxXE == 0:
                XE = map(lambda x: x/maxXC*k, XE)
            maxN = max(N)
            if not maxN == 0:
                N = map(lambda x: x/maxN, N)
            maxW = max(W)
            if not maxW == 0:
                W = map(lambda x: x/maxW, W)
            print "max xc", maxXC, "max xe", maxXE, "max n", maxN,
            print "max w", maxW
        print 'final xc', XC[-1], 'final xe', XE[-1], 'final n',
        print N[-1], 'final w', W[-1]

        return [XC, XE, N, W]

    def print_params(self):
        Mam, MaM, Mbc, Mbe, Mg, Ml, Ms, Md, Mk, Mr = self.parameters
        Mxc, Mxe, My, Mw = self.metrics
        Mt = self.runtime
        print Mxc, "xc  initial commoner popultaion"
        print Mxe, "xe  initial elite population"
        print My, "y   inital amount of nature"
        print Mw, "w   initial amount of wealth"
        print Mam, "am  minimum death rate"
        print MaM, "aM  Maximal death rate"
        print Mbc, "bc  commoner birth rate"
        print Mbe, "be  elite birth rate"
        print Mg, "g   nature regeneration factor"
        print Ml, "l   nature's capactiy"
        print Ms, "s   subsistence salary (consumption)"
        print Md, "d   nature depletion factor"
        print Mk, "k   difference in consumtion factor"
        print Mr, "r   minimum required consumption"
        print Mt, "t   how long to run the simulation"


if __name__ == '__main__':
    print """
    xc  initial commoner popultaion
    xe  initial elite population
    y   inital amount of nature
    w   initial amount of wealth
    am  minimum death rate
    aM  Maximal death rate
    bc  commoner birth rate
    be  elite birth rate
    g   nature regeneration factor
    l   nature's capactiy
    s   subsistence salary (consumption)
    d   nature depletion factor
    k   difference in consumtion factor
    r   minimum required consumption
    t   how long to run the simulation"""
