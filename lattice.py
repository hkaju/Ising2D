import random
import math

class Lattice2D:

    lattice = []

    #Model parameters

    #External magnetic field
    #Default: no field
    B = 0

    #Temperature
    #Default: 0.01
    T = 0.01

    #Coupling between NN spins
    #- - ferromagnet, aligned spins lower in energy
    #+ - antiferromagnet, antialigned spins lower in energy
    #Default: ferromagnet, multiplied by 0.5 to avoid double counting
    J = -1

    #Calculated lattice properties
    energy = None
    magnetization = None

    def __init__(self, length, B=None, T=None, J=None, prerun=False):
        if B:
            self.B = B
        if J:
            self.J = J
        if T:
            self.T = T
        if length:
            if prerun:
                self.initialize(length, random_spins=True)
            else:
                self.initialize(length)

    def initialize(self, length, random_spins=False):
        """Create a square lattice and populate it with random spins."""

        self.length = length
        #Initialize lattice with empty rows. Minor performance gain vs appending
        self.lattice = [None] * length
        for y in range(length):
            row = [None] * length
            for x in range(length):
                if random_spins:
                    #Set all spins to be random to start out at T = infinity
                    row[x] = random.choice([-1, 1])
                else:
                    #Set all spins to be pointing in one direction to start at T = 0
                    row[x] = 1
            self.lattice[y] = row
        print("Initialized {0}x{0} lattice with T={1}, B={2}, J={3}".format(
            self.length, self.T, self.B, self.J))
        print("M: {0}\nE: {1}".format(self.get_magnetization(),
            self.get_energy()))

    def set_temperature(self, temperature):
        """Set the temperature of the lattice."""

        self.T = temperature

    def visualize(self):
        """Print out the lattice."""

        for row in self.lattice:
            #TODO Pretty formatting
            print(row)

    def flip(self, x, y):
        """Flip spin at (x, y)."""

        old = self.get_energy_at(x, y)
        #Flip the spin
        self.lattice[y][x] = -self.lattice[y][x]
        new = self.get_energy_at(x, y)
        #Update energy and magnetization values
        if self.energy != None:
            self.energy += new - old
        if self.magnetization != None:
            self.magnetization += 2 * self.lattice[y][x]

    def mc_move(self):
        """Perform a single Monte Carlo move."""

        #Select a spin at random
        x = random.randrange(self.length)
        y = random.randrange(self.length)

        #Calculate energy of the old configuration
        old = self.get_energy()
        #Flip the spin
        self.flip(x, y)
        #Calculate the energy difference between the new
        #and the old configuration
        new = self.get_energy()
        dE = new - old
        #Calculate acceptance rate
        if self.T > 0:
            acc = min(1, math.exp(-dE/self.T))
        else:
            if dE <= 0:
                acc = 1
            else:
                acc = 0
        #If the step was rejected, flip the spin back to it's original state
        if random.uniform(0, 1) > acc:
            self.flip(x, y)

    def get_magnetization(self):
        """Returns total magnetization of the current configuration."""

        #If no magnetization is stored, recalculate
        if self.magnetization == None:
            magnetization = 0
            for row in self.lattice:
                for cell in row:
                    magnetization += cell
            #Store magnetization for future use
            self.magnetization = magnetization

        return self.magnetization

    def get_average_magnetization(self):
        return self.get_magnetization() / float(self.length**2)

    def get_energy(self):
        """Returns the total energy of the current configuration."""

        #If energy is not stored, recalculate
        if self.energy == None:
            energy = 0.0
            for x in range(self.length):
                for y in range(self.length):
                    #Nearest-neighbour interactions
                    #Negative coordinates used to get periodic boundary
                    #conditions for free thanks to Python's lists
                    energy += self.lattice[-y][-x]\
                                * self.lattice[-y + 1][-x] * self.J
                    energy += self.lattice[-y][-x]\
                                * self.lattice[-y - 1][-x] * self.J
                    energy += self.lattice[-y][-x]\
                                * self.lattice[-y][-x + 1] * self.J
                    energy += self.lattice[-y][-x]\
                                * self.lattice[-y][-x - 1] * self.J
                    #Interactions with the magnetic field
                    energy += self.lattice[-y][-x] * self.B
            #Store energy for future use
            self.energy = energy

        return self.energy

    def get_average_energy(self):
        return self.get_energy() / float(self.length**2)

    def get_energy_at(self, x, y):
        """Returns the energy of spin at (x, y)."""

        energy = 0.0

        #NN interactions with PBC
        energy += self.lattice[y][x]\
                    * self.lattice[min(y + 1, y + 1 - self.length)][x]\
                    * self.J
        energy += self.lattice[y][x]\
                    * self.lattice[y - 1][x]\
                    * self.J
        energy += self.lattice[y][x]\
                    * self.lattice[y][min(x + 1, x + 1 - self.length)]\
                    * self.J
        energy += self.lattice[y][x]\
                    * self.lattice[y][x - 1]\
                    * self.J

        #Interactions with the magnetic field
        energy += self.lattice[y][x] * self.B

        return energy
