import glob
import subprocess

def generate_report():
    '''Generate a PDF report containing magnetization data and lattice snapshots.'''

    n_lattices = len(glob.glob("data/lattice*.csv"))
    #R code template
    report_template = open("templates/report.template.r", 'r').read()
    #R code template for a lattice file
    latticeplot_template = """data{0} <- read.csv('data/lattice{0}.csv', header=T)
    levelplot(spin~x*y, data{0}, main='Sweeps: {0}', colorkey=FALSE, xlab='', ylab='', at=c(-1, 0, 1))\n"""
    #Generate R code for each lattice file
    lattice_plots = ""
    for n in range(n_lattices):
        lattice_plots += latticeplot_template.format(n)
    #Write R file to disk
    open('report.r', 'w').write(report_template % lattice_plots)
    #Run R and compile report
    subprocess.call(['R', '-f report.r'])
    print("Report generated!")

def write_lattice(lattice, filename):
    '''Write the lattice configuration to a CSV file.'''

    f = open(filename, 'w')
    f.write("x,y,spin\n")
    for x in range(lattice.length):
        for y in range(lattice.length):
            f.write("%i,%i,%i\n" % (x, y, lattice.lattice[y][x]))
    f.close()
