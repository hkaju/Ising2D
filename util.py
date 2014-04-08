import glob
import subprocess

def generate_report():
    nlat = len(glob.glob("data/lattice*.csv"))
    rtemplate = open("templates/report.template.r", 'r').read()
    lattemplate = """data{0} <- read.csv('data/lattice{0}.csv', header=T)
    levelplot(spin~x*y, data{0}, main='Sweeps: {0}', colorkey=FALSE, xlab='', ylab='', at=c(-1, 0, 1))\n"""
    latprocessing = ""
    for i in range(nlat):
        latprocessing = latprocessing + lattemplate.format(i)
    open('report.r', 'w').write(rtemplate % latprocessing)
    subprocess.call(['R', '-f report.r'])
    print("Report generated!")

def write_lattice(lat, filename):
    f = open(filename, 'w')
    f.write("x,y,spin\n")
    for x in range(lat.length):
        for y in range(lat.length):
            f.write("%i,%i,%i\n" % (x, y, lat.lattice[y][x]))
    f.close()
