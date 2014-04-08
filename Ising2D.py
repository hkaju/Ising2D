#!/usr/bin/env python

import random
import sys
import math
import util

from lattice import Lattice2D

LATTICE_SIZE = 20
EQUILIBRIATION_CYCLES = 30
MEASUREMENT_CYCLES = 10
MAGNETIC_FIELD = 0.1

class Ising2D:

    lattice = None
    T = 0.5

    def __init__(self):
        self.lattice = Lattice2D(LATTICE_SIZE, B=MAGNETIC_FIELD)
        util.write_lattice(self.lattice, "data/lattice0.csv")
        self.equilibriate()

    def equilibriate(self):
        """Equlilibriate the lattice before sampling."""

        print("Equilibriating")
        #Step counter
        n = 0
        #Equilibriation log for tracking magnetization
        log = [("x", "y",)]
        for sweep in range(EQUILIBRIATION_CYCLES):
            for i in range(self.lattice.length**2):
                #Perform MC step
                self.MCStep()
                n += 1
                #Log magnetization
                log.append((str(n), str(self.lattice.get_magnetization()),))
            #Take a snapshot of the lattice after each sweep
            util.write_lattice(self.lattice, "data/lattice%i.csv" % (sweep + 1))
        #Write equilibriation log to disk
        logfile = open("data/equilibriation.csv", "w")
        for line in log:
            logfile.write("%s,%s\n" % line)

    def sample(self):
        pass

    def MCStep(self):
        """Perform a single Monte Carlo step."""

        #Select a spin at random
        x = random.randrange(self.lattice.length)
        y = random.randrange(self.lattice.length)
        #Flip the spin
        new_lattice = self.lattice.flip(x, y)
        #Calculate the energy difference between the new and the old configuration
        dE = new_lattice.get_energy_at(x, y) - self.lattice.get_energy_at(x, y)
        #Calculate acceptance rate
        acc = min(1, math.exp(-dE/self.T))
        #Determine if the step was accepted
        if random.uniform(0, 1) < acc:
            self.lattice = new_lattice

if __name__ == "__main__":
    Ising2D()
    if "+r" in sys.argv:
        util.generate_report()
