pdf("reports/{run}-preruns.pdf")

prerun1 = read.csv("data/{run}-prerun1/equilibriation-T1.0.csv", header=T)
prerun2 = read.csv("data/{run}-prerun2/equilibriation-T1.0.csv", header=T)
prerun3 = read.csv("data/{run}-prerun3/equilibriation-T1.0.csv", header=T)

plot(prerun1$x, prerun1$y, xlab="Lattice sweeps", ylab="Magnetization", type="n", main="Preruns for {run}")
lines(prerun1$x, prerun1$y, col="red")
lines(prerun2$x, prerun2$y, col="green")
lines(prerun3$x, prerun3$y, col="blue")

dev.off()
