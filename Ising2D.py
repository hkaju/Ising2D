#!/usr/bin/env python

import random
from lattice import *
import glob

def generate_report():
    nlat = len(glob.glob("data/lattice*.csv"))
    rtemplate = open("templates/report.template.r", 'r').read()
    lattemplate = """data{0} <- read.csv('data/lattice{0}.csv', header=T)
    levelplot(z~x*y, data{0}, main='Sweeps: {0}')\n"""
    latprocessing = ""
    for i in range(nlat):
        latprocessing = latprocessing + lattemplate.format(i)
    open('report.r', 'w').write(rtemplate % latprocessing)
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
                if newlat.getEnergy() <= lattice.getEnergy():
                    lattice = newlat
                n += 1
                log.append((str(n), str(lattice.getEnergy()),))
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
    lat = Lattice2D(10, temp=0.00001)
    write_lattice(lat, "data/lattice0.csv")
    lat = equilibriate(lat, 20)
    generate_report()
