require(lattice)
lattice.options(default.theme = standard.theme(color = FALSE))

pdf("report.pdf")

equi <- read.csv("data/equilibriation.csv", header=T)
plot(equi$x, equi$y, xlab="Monte Carlo moves", ylab="Magnetization", type="n")
lines(equi$x, equi$y)

%s

dev.off()
