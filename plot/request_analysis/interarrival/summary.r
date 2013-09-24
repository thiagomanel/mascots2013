library("ggplot2")
library("plyr")

Args <- commandArgs(TRUE)
fileName <- Args[1]

#arrival trace
input <- read.table(fileName, header = T)

data <- ddply(input, .(trace), transform, ecd = ecdf(arrival)(arrival))

for (t in levels(data$trace)) {
   sub <- subset(data, data$trace %in% c(t))
   print(t)
   print(length(sub$ecd))
   print(summary(sub))
#   print(sub)
}
