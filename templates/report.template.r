pdf("{filename}")

data <- read.csv("results.csv", header=T)

par(mfrow=c(2,2))
plot(data$T, data$M, xlab="Temperature", ylab="Magnetization")
plot(data$T, data$E, xlab="Temperature", ylab="Energy")
plot(data$T, data$Xb, xlab="Temperature", ylab="Magnetic susceptibility")
plot(data$T, data$Xt, xlab="Temperature", ylab="Heat capacity")

par(mfrow=c(2,3))
{equilibriation_graphs}

dev.off()
