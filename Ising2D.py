#!/usr/bin/env python

import random
import sys
import math
import util

from lattice import Lattice2D

LATTICE_SIZE = 10
EQUILIBRIATION_SWEEPS = 30
MEASUREMENT_SWEEPS = 50
MEASUREMENT_FREQUENCY = 10
MAGNETIC_FIELD = 0.1

class Ising2D:

    lattice = None
    T = 0.01
    measurement_data = {"M" : [],
                        "E" : []}

    def __init__(self):
        results = {}
        step = 0.1
        maxtemp = 5
        self.lattice = Lattice2D(LATTICE_SIZE, B=MAGNETIC_FIELD)
        while self.T < maxtemp:
            util.write_lattice(self.lattice, "data/lattice0.csv")
            self.equilibriate()
            self.generate_samples()
            results[self.T] = self.calculate_properties()
            util.generate_report(
                "reports/report-T{0:g}-B{1:g}.pdf".format(self.T, MAGNETIC_FIELD)
                )
            self.T += step
        self.write_results(results)

    def equilibriate(self):
        """Equlilibriate the lattice before sampling."""

        print("Equilibriating...")
        #Step counter
        n = 0
        #Equilibriation log for tracking magnetization
        log = [("x", "y",)]
        for sweep in range(EQUILIBRIATION_SWEEPS):
            for i in range(self.lattice.length**2):
                #Perform MC step
                self.MCStep()
                n += 1
                #Log magnetization
                log.append((str(n), str(self.lattice.get_magnetization()),))
            #Take a snapshot of the lattice after each sweep
            #util.write_lattice(self.lattice, "data/lattice%i.csv" % (sweep + 1))
        #Write equilibriation log to disk
        logfile = open("data/equilibriation.csv", "w")
        for line in log:
            logfile.write("%s,%s\n" % line)

    def generate_samples(self):

        print("Calculating ensemble averages...")
        for n in range(MEASUREMENT_SWEEPS * self.lattice.length**2):
            self.MCStep()
            if n % MEASUREMENT_FREQUENCY == 0:
                self.sample()

    def write_results(self, data):
        results_file = open("results.csv", "w")
        results_file.write("T,E,M,Xt,Xb\n")
        for temperature in data:
            Xt = (data[temperature]["E2"] - data[temperature]["E"]**2) / float(temperature)**2
            Xb = (data[temperature]["M2"] - data[temperature]["M"]**2) / float(temperature)
            line = "{T},{E},{M},{Xt},{Xb}\n".format(T=temperature,
                                                    E=data[temperature]["E"],
                                                    M=data[temperature]["M"],
                                                    Xt=Xt,
                                                    Xb=Xb)
            results_file.write(line)
        results_file.close()

    def calculate_properties(self):
        E = 0.0
        E2 = 0.0
        M = 0.0
        M2 = 0.0
        for e in self.measurement_data["E"]:
            E += e
            E2 += e**2
        E = E / len(self.measurement_data["E"])
        E2 = E2 / len(self.measurement_data["E"])
        for m in self.measurement_data["M"]:
            M += m
            M2 += m**2
        M = M / len(self.measurement_data["M"])
        M2 = M2 / len(self.measurement_data["M"])
        return {"E" : E, "E2" : E2, "M" : M, "M2" : M2}

    def sample(self):
        """Sample equilibrium properties from current configuration."""

        magnetization = self.lattice.get_magnetization()
        energy = self.lattice.get_energy()
        self.measurement_data["M"].append(magnetization)
        self.measurement_data["E"].append(energy)

    def MCStep(self):
        """Perform a single Monte Carlo step."""

        #Select a spin at random
        x = random.randrange(self.lattice.length)
        y = random.randrange(self.lattice.length)
        #Flip the spin
        new_lattice = self.lattice.flip(x, y)
        #Calculate the energy difference between the new
        #and the old configuration
        dE = new_lattice.get_energy_at(x, y) - self.lattice.get_energy_at(x, y)
        #Calculate acceptance rate
        if self.T > 0:
            acc = min(1, math.exp(-dE/self.T))
        else:
            if dE <= 0:
                acc = 1
            else:
                acc = 0
        #Determine if the step was accepted
        if random.uniform(0, 1) < acc:
            self.lattice = new_lattice

if __name__ == "__main__":
    Ising2D()
    if "+r" in sys.argv:
        util.generate_report("report.pdf")
