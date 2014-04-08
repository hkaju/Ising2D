#!/usr/bin/env python

import random
from lattice import Lattice2D
import sys
import math
import util

LATTICE_SIZE = 10
EQUILIBRIATION_SWEEPS = 50

def equilibriate(lattice, sweeps):
    '''Minimise energy before calculating equilibrium properties.'''

    print("Minimising energy")
    #Flip counter
    n = 0
    #Log file for tracking energy
    log = [('x', 'y',)]
    for sweep in range(sweeps):
        for row in range(lattice.length):
            for cell in range(lattice.length):
                #Generate new lattice with a flipped spin
                #print("Flipped %i %i" % (row, cell))
                newlat = lattice.flip(row, cell)
                #If the new lattice is lower in energy, accept the spin flip and continue
                if newlat.getEnergyOf(row, cell) <= lattice.getEnergyOf(row, cell) or random.uniform(0, 1) < math.exp((-newlat.getEnergyOf(row, cell) + lattice.getEnergyOf(row, cell))):
                    lattice = newlat
                n += 1
                log.append((str(n), str(lattice.getMagnetization()),))
        #Print new energy value
        print(lattice.getEnergy())
        util.write_lattice(lattice, "data/lattice%i.csv" % (sweep + 1))
    #Write equilibriation log to disk
    l = open('data/equilibriation.csv', 'w')
    for line in log:
        l.write("%s,%s\n" % line)
    #Return new lattice
    return lattice


if __name__ == "__main__":
    if '-r' in sys.argv:
        util.generate_report()
        sys.exit(0)
    lat = Lattice2D(LATTICE_SIZE, B=0.1)
    util.write_lattice(lat, "data/lattice0.csv")
    lat = equilibriate(lat, EQUILIBRIATION_SWEEPS)
    if '+r' in sys.argv:
        util.generate_report()
