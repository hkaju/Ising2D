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
    J = -1 * 0.5

    #Calculated lattice properties
    energy = None
    magnetization = None

    def __init__(self, length, B=None, T=None, J=None):
        if B:
            self.B = B
        if J:
            self.J = J
        if T:
            self.T = T
        if length:
            self.initialize(length)

    def initialize(self, length):
        """Create a square lattice and populate it with random spins."""

        self.length = length
        #Initialize lattice with empty rows. Minor performance gain vs appending
        self.lattice = [None] * length
        for y in range(length):
            row = [None] * length
            for x in range(length):
                row[x] = random.choice([-1, 1])
            self.lattice[y] = row
        print("Initialized {0}x{0} lattice with T={1}, B={2}, J={3}".format(self.length, self.T, self.B, self.J))

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

        #Flip the spin
        self.lattice[y][x] = -self.lattice[y][x]

        #Reset properties so that they will be recalculated
        #self.energy = None
        #self.magnetization = None

    def mc_move(self):
        """Perform a single Monte Carlo move."""

        #Select a spin at random
        x = random.randrange(self.length)
        y = random.randrange(self.length)
        #Calculate energy of the old configuration
        energy = self.get_energy_at(x, y)
        #Flip the spin
        self.flip(x, y)
        #Calculate the energy difference between the new
        #and the old configuration
        dE = self.get_energy_at(x, y) - energy
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
        """Returns magnetization per site of the current configuration."""

        #If no magnetization is stored, recalculate
        if not self.magnetization:
            magnetization = 0.0
            for row in self.lattice:
                for cell in row:
                    magnetization += cell
            #Store magnetization for future use
            self.magnetization = magnetization / self.length**2

        return self.magnetization

    def get_energy(self):
        """Returns the total energy of the current configuration."""

        #If energy is not stored, recalculate
        if not self.energy:
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
