#!/usr/bin/env python

import random
from lattice import *
import glob
import subprocess
import sys
import math

LATTICE_SIZE = 40
EQUILIBRIATION_SWEEPS = 30

def generate_report():
    nlat = len(glob.glob("data/lattice*.csv"))
    rtemplate = open("templates/report.template.r", 'r').read()
    lattemplate = """data{0} <- read.csv('data/lattice{0}.csv', header=T)
    levelplot(z~x*y, data{0}, main='Sweeps: {0}', colorkey=FALSE, xlab='', ylab='')\n"""
    latprocessing = ""
    for i in range(nlat):
        latprocessing = latprocessing + lattemplate.format(i)
    open('report.r', 'w').write(rtemplate % latprocessing)
    subprocess.call(['R', '-f report.r'])
    print("Report generated!")

def write_lattice(lat, filename):
    f = open(filename, 'w')
    f.write("x,y,z\n")
    for x in range(lat.length):
        for y in range(lat.length):
            f.write("%i,%i,%i\n" % (x, y, lat.lattice[y][x]))
    f.close()

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
        write_lattice(lattice, "data/lattice%i.csv" % (sweep + 1))
    #Write equilibriation log to disk
    l = open('data/equilibriation.csv', 'w')
    for line in log:
        l.write("%s,%s\n" % line)
    #Return new lattice
    return lattice


if __name__ == "__main__":
    if '-r' in sys.argv:
        generate_report()
        sys.exit(0)
    lat = Lattice2D(LATTICE_SIZE, B=0.1)
    write_lattice(lat, "data/lattice0.csv")
    lat = equilibriate(lat, EQUILIBRIATION_SWEEPS)
    if '+r' in sys.argv:
        generate_report()
