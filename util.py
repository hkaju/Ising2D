import glob
import subprocess
import os

def deepcopy(lattice):
    l = len(lattice)
    newlattice = [[None] * l] * l
    for x in range(l):
        for y in range(l):
            newlattice[y][x] = 1 * lattice[y][x]
    return newlattice

def generate_report(filename):
    report_template = open("templates/report.template.r", 'r').read()
    equilibriation_template = """{run} <- read.csv("{filename}", header=T)
plot({run}$x, {run}$y, xlab="MC moves", ylab="Magnetization", type="n", main="{run}", ylim=c(-1, 1))
lines({run}$x, {run}$y)\n"""
    equilibriation_graphs = ""
    for datafile in glob.glob("data/equilibriation*.csv"):
        run = datafile[20:-4]
        equilibriation_graphs += equilibriation_template.format(filename=datafile, run=run)
    #Write R file to disk
    open('report.r', 'w').write(report_template.format(equilibriation_graphs=equilibriation_graphs, filename=filename))
    #Run R and compile report
    subprocess.call(['R', '-f report.r'])
    print("Report generated!")

def generate_equilibriation_report(filename):
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
    open('report.r', 'w').write(report_template.format(lattices=lattice_plots, filename=filename))
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

def write_results(data, folder):
    path = "data" + os.sep + folder
    if not os.path.exists(path):
        os.mkdir(path)
    results_file = open(path + os.sep + "results.csv", "w")
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

def write_log(log, folder, filename):
    path = "data" + os.sep + folder
    if not os.path.exists(path):
        os.mkdir(path)
    logfile = open(path + os.sep + filename, "w")
    for line in log:
        logfile.write("%s,%s\n" % line)
    logfile.close()
