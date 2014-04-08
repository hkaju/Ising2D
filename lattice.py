import random
from copy import deepcopy

class Lattice2D:

    lattice = []

    #Model parameters

    #External magnetic field
    #Default: no field
    B = 0

    #Coupling between NN spins
    #-1 - ferromagnet, aligned spins lower in energy
    #+1 - antiferromagnet, antialigned spins lower in energy
    #Default: ferromagnet
    J = -1

    #Calculated lattice properties
    energy = None
    magnetization = None

    def __init__(self, length=None, lattice=None, B=None):
        #If length is specified, initialize a new lattice with the required length
        if length:
            self.initialize(length)
        #If an existing lattice is provided, use that to initialize
        if lattice:
            self.lattice = lattice
            self.length = len(lattice)
        if B:
            self.B = B

    def initialize(self, length):
        """Create a square lattice and populate it with random spins."""

        self.length = length
        print("Initializing {len}x{len} square lattice".format(len=length))
        for i in range(length):
            row = []
            for r in range(length):
                row.append(random.choice([-1, 1]))
            self.lattice.append(row)

    def visualize(self):
        """Print out the lattice."""

        for row in self.lattice:
            #TODO Pretty formatting
            print(row)

    def flip(self, x, y):
        """Flip spin at (x, y)."""

        #Copy lattice
        newlattice = deepcopy(self.lattice)
        #Flip the spin
        newlattice[y][x] = -newlattice[y][x]
        #Return a new Lattice2D object
        return Lattice2D(lattice=newlattice, B=self.B)

    def randflip(self, x, y):
        """Randomize spin at (x, y)."""

        #Copy lattice
        newlattice = deepcopy(self.lattice)
        #Generate new spin
        newlattice[y][x] = random.choice([-1, 1])
        #Return a new Lattice2D object
        return Lattice2D(lattice=newlattice, B=self.B)

    def get_magnetization(self):
        """Returns total magnetization of the current configuration."""

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
                    #NN interactions
                    #Negative coordinates used to get PBC for free thanks to Python's lists
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y + 1][-x] * self.J
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y - 1][-x] * self.J
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y][-x + 1] * self.J
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y][-x - 1] * self.J
                    #Interactions with the magnetic field
                    energy += self.lattice[-y][-x] * self.B
            #Store energy for future use
            self.energy = energy

        return self.energy

    def get_energy_at(self, x, y):
        """Returns the energy of spin at (x, y)."""

        energy = 0.0

        #NN interactions with PBC
        energy += 0.5 * self.lattice[y][x] * self.lattice[min(y + 1, y + 1 - self.length)][x] * self.J
        energy += 0.5 * self.lattice[y][x] * self.lattice[y - 1][x] * self.J
        energy += 0.5 * self.lattice[y][x] * self.lattice[y][min(x + 1, x + 1 - self.length)] * self.J
        energy += 0.5 * self.lattice[y][x] * self.lattice[y][x - 1] * self.J
        #Interactions with the magnetic field
        energy += self.lattice[y][x] * self.B

        return energy
