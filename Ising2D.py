#!/usr/bin/env python

import random
import sys
import math
import util

from lattice import Lattice2D

#General model properties
LATTICE_SIZE = 10
MAGNETIC_FIELD = 0

#Measurement properties
EQUILIBRIATION_SWEEPS = 20
MEASUREMENT_SWEEPS = 20
SAMPLING_FREQUENCY = 10

#Temperature dependence measurements
STARTING_TEMPERATURE = 0.01
FINAL_TEMPERATURE = 3
TEMPERATURE_STEP = 0.1

class Ising2D:

    _lattice = None

    def old__init__(self):
        results = {}
        step = 0.1
        maxtemp = 3
        self._lattice = Lattice2D(LATTICE_SIZE, B=MAGNETIC_FIELD, T=STARTING_TEMPERATURE)
        self.equilibriate(20)
        while self._lattice.T < maxtemp:
            print("T: {temp}".format(temp=self._lattice.T))
            self.equilibriate(20)
            self.generate_samples()
            results[self._lattice.T] = self.calculate_properties()
            self._lattice.T += step
            self.measurement_data = {"M" : [],
                                     "E" : []}
        self.write_results(results, "results.csv")
        util.generate_report(
                "reports/{length}x{length}-B{B}-report.pdf".format(
                    length=self._lattice.length,
                    B=MAGNETIC_FIELD))

    def __init__(self):

        #Initialize a new lattice
        self._lattice = Lattice2D(length=LATTICE_SIZE,
                                 T=STARTING_TEMPERATURE,
                                 B=MAGNETIC_FIELD)
        results = {}
        #Equilibriate lattice before taking averages
        self.equilibriate(LATTICE_SIZE)
        #Start measuring averages at increasing temperatures
        while self._lattice.T < FINAL_TEMPERATURE:
            print("T: {temp}".format(temp=self._lattice.T))
            #Equilibriate lattice after temperature increase
            #Equilibriation can be smaller because starting point is no longer
            #at infinite temperature
            self.equilibriate(LATTICE_SIZE / 2)
            #Sample equilibrium properties
            data = self.sample()
            #Calculate averages and response functions
            results[self._lattice.T] = self.calculate_properties(data)
            #Write results data to disk
            util.write_results(results, "{0}x{0}-B{1}".format(self._lattice.length, MAGNETIC_FIELD))
            #Generate a PDF report
            #self.gen
            #Increase temperature for next measurement cycle
            self._lattice.set_temperature(self._lattice.T + TEMPERATURE_STEP)

    def equilibriate(self, cycles):
        """Equlilibriate the lattice before sampling."""

        #Step counter
        n = 0
        #Equilibriation log for tracking magnetization
        log = [("x", "y",)]
        for sweep in range(cycles):
            for i in range(self._lattice.length**2):
                #Perform MC step
                self._lattice.mc_move()
                n += 1
                #Log magnetization
                log.append((str(n), str(self._lattice.get_magnetization()),))
            #Take a snapshot of the lattice after each sweep
            #util.write_lattice(self._lattice, "data/lattice%i.csv" % (sweep + 1))
        #Write equilibriation log to disk
        util.write_log(log, "{0}x{0}-B{1}".format(self._lattice.length, MAGNETIC_FIELD), "equilibriation-T{0}.csv".format(self._lattice.T))

    def calculate_properties(self, data):
        E = 0.0
        E2 = 0.0
        M = 0.0
        M2 = 0.0
        for e in data["E"]:
            E += e
            E2 += e**2
        E = E / len(data["E"])
        E2 = E2 / len(data["E"])
        for m in data["M"]:
            M += m
            M2 += m**2
        M = M / len(data["M"])
        M2 = M2 / len(data["M"])
        return {"E" : E, "E2" : E2, "M" : M, "M2" : M2}

    def sample(self):
        """Sample equilibrium properties from current configuration."""

        data = {"E" : [], "M" : []}
        for n in range(MEASUREMENT_SWEEPS * self._lattice.length**2):
            self._lattice.mc_move()
            if n % SAMPLING_FREQUENCY == 0:
                magnetization = self._lattice.get_magnetization()
                energy = self._lattice.get_energy()
                data["M"].append(magnetization)
                data["E"].append(energy)
        return data

if __name__ == "__main__":
    Ising2D()
    if "+r" in sys.argv:
        util.generate_report("report.pdf")
