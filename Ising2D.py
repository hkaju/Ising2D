#!/usr/bin/env python

import sys
import re

import util
from lattice import Lattice2D

#Measurement properties
EQUILIBRIATION_SWEEPS = 100
MEASUREMENT_SWEEPS = 50
SAMPLING_FREQUENCY = 100

#Temperature dependence measurements
STARTING_TEMPERATURE = 0.01
FINAL_TEMPERATURE = 3
TEMPERATURE_STEP = 0.1

class Ising2D:

    _lattice = None

    def __init__(self, lattice_size, magnetic_field):
        """Set up the model and calculate temperature dependencies of
        equilibrium properties."""

        #Runs are are identified by lattice size and magnetic field
        #E.g. 10x10-B0.5
        self._run_id = "{0}x{0}-B{1}".format(lattice_size, magnetic_field)

        #Initialize new lattice
        self._lattice = Lattice2D(lattice_size,
                                 T=STARTING_TEMPERATURE,
                                 B=magnetic_field)

        #Equilibriate lattice before taking averages
        self.equilibriate(EQUILIBRIATION_SWEEPS)

        #Start measuring averages at increasing temperatures
        results = {}
        while self._lattice.T < FINAL_TEMPERATURE:
            print("T: {0}".format(self._lattice.T))

            #Equilibriate lattice after each temperature increase
            self.equilibriate(EQUILIBRIATION_SWEEPS)

            #Sample equilibrium properties
            data = self.sample()

            #Calculate averages and response functions
            results[self._lattice.T] = self.calculate_properties(data)

            #Increase temperature for next measurement cycle
            self._lattice.set_temperature(self._lattice.T + TEMPERATURE_STEP)

        #Write results to disk
        util.write_results(results, self._run_id)

    def equilibriate(self, cycles):
        """Equlilibriate the lattice before sampling."""

        #Step counter
        n = 0

        #Equilibriation log
        log = [("x", "y",)]

        for sweep in range(cycles):
            for i in range(self._lattice.length**2):
                #Perform MC step
                self._lattice.mc_move()
                n += 1
                #Log magnetization to track equilibriation progress
                log.append((str(n), str(self._lattice.get_magnetization()),))

        #Take a snapshot of the lattice after equilibriation
        #util.write_lattice(self._lattice,
        #    "data/{0}/lattice-T{1}.csv".format(self._run_id, self._lattice.T))

        #Write equilibriation log to disk
        util.write_log(log,
            self._run_id,
            "equilibriation-T{0}.csv".format(self._lattice.T))

    def calculate_properties(self, data):
        """Calculate properties from sampled data."""

        #Calculate averages of the energy and it's square
        E = 0.0
        E2 = 0.0
        for e in data["E"]:
            E += e
            E2 += e**2
        E = E / len(data["E"])
        E2 = E2 / len(data["E"])

        #Calculate averages of the magnetization and it's square
        M = 0.0
        M2 = 0.0
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
    for arg in sys.argv:
        match = re.search('(\d+)x(\d+)-B(.+)', arg)
        if match:
            lattice_size = int(match.group(1))
            magnetic_field = float(match.group(3))
    if not "+r" in sys.argv:
        Ising2D(lattice_size, magnetic_field)
    if not "-r" in sys.argv:
        #Generate a PDF report of the results
        util.generate_report("{0}x{0}-B{1}".format(lattice_size,
            magnetic_field))
