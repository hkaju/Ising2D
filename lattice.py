import random
from copy import *

class Lattice2D:

    lattice = []

    #Default model parameters
    B = 0 #External magnetic field
    J = -1 #Coupling between NN spins

    #Calculated lattice properties
    energy = None
    magnetization = None

    def __init__(self, length=None, lattice=None, temperature=None):
        #If length is specified, initialise a new lattice with the required length
        if length:
            self.initialize(length)
        #If temperature is specified, set it here
        if temperature:
            self.J = self.J * temp
        #If an existing lattice is provided, use that to initialize
        if lattice:
            self.lattice = lattice
            self.length = len(lattice)

    def initialize(self, length):
        '''Create a square lattice and populate it with random spins.'''

        self.length = length
        print("Initializing {len}x{len} square lattice".format(len=length))
        for i in range(length):
            row = []
            for r in range(length):
                row.append(random.choice([-1, 1]))
            self.lattice.append(row)

    def visualize(self):
        '''Print out the lattice.'''

        for row in self.lattice:
            #TODO Pretty formatting
            print(row)

    def flip(self, x, y):
        '''Flip spin at (x, y).'''

        #Copy lattice
        newlattice = deepcopy(self.lattice)
        #Flip the spin
        newlattice[y][x] = -newlattice[y][x]
        #Return a new Lattice2D object
        return Lattice2D(lattice=newlattice)

    def randflip(self, x, y):
        '''Randomise spin at (x, y).'''

        #Copy lattice
        newlattice = deepcopy(self.lattice)
        #Generate new spin
        newlattice[y][x] = random.choice([-1, 1])
        #Return a new Lattice2D object
        return Lattice2D(lattice=newlattice)

    def getMagnetization(self):
        '''Returns total magnetization of the current configuration.'''

        #If no magnetization is stored, recalculate
        if not self.magnetization:
            sum = 0
            for row in self.lattice:
                for cell in row:
                    sum += cell
            #Store magnetization for future use
            self.magnetization = sum

        return self.magnetization

    def getEnergy(self):
        '''Returns the total energy of the current configuration.'''

        #If energy is not stored, recalculate
        if not self.energy:
            energy = 0.0
            for x in range(self.length):
                for y in range(self.length):
                    #NN interactions with PBC
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y + 1][-x] * self.J
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y - 1][-x] * self.J
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y][-x + 1] * self.J
                    energy += 0.5 * self.lattice[-y][-x] * self.lattice[-y][-x - 1] * self.J
                    #Interactions with the magnetic field
                    energy += self.lattice[-y][-x] * self.B
            #Store energy for future use
            self.energy = energy

        return self.energy

    def getEnergyOf(self, x, y):
        '''Returns the energy of spin at (x, y).'''

        energy = 0.0

        #NN interactions with PBC
        energy += 0.5 * self.lattice[y][x] * self.lattice[min(y + 1, y + 1 - self.length)][x] * self.J
        energy += 0.5 * self.lattice[y][x] * self.lattice[y - 1][x] * self.J
        energy += 0.5 * self.lattice[y][x] * self.lattice[y][min(x + 1, x + 1 - self.length)] * self.J
        energy += 0.5 * self.lattice[y][x] * self.lattice[y][x - 1] * self.J
        #Interactions with the magnetic field
        energy += self.lattice[y][x] * self.B

        return energy
