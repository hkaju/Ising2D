require(lattice)

pdf("report.pdf")

equi <- read.csv("plots/equilibriation.csv", header=T)
plot(equi$x, equi$y, xlab="Spin flips", ylab="Energy", type="n")
lines(equi$x, equi$y)

%s

dev.off()
