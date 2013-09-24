library("plyr")
library("ggplot2")

#It sums up all operations latency. So we exclude idle intervals.
Args <- commandArgs(TRUE)
file <- Args[1]

#process count trace
data <- read.table(file, header = T)
summary(data)

p <- ggplot(data, aes(factor(type))) + geom_bar(position='dodge')
p <- p + theme_bw() + xlab(NULL) + ylab(NULL) + opts(axis.text.x  = theme_text(angle=45, hjust = 1, vjust = 1))
ggsave(p, filename=paste(file, "bar_optype.png", sep="_"))
