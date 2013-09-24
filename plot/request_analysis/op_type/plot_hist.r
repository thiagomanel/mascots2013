library("plyr")
library("ggplot2")

#It sums up all operations latency. So we exclude idle intervals.
Args <- commandArgs(TRUE)
file <- Args[1]

#process count trace
data <- read.table(file, header = T)
summary(data)


df.new <- ddply(data,.(trace), summarise, prop=prop.table(table(type)), Type=names(table(type)))
summary(df.new)
p <- ggplot(df.new, aes(Type, prop)) + geom_bar(stat="identity", position='dodge') + facet_wrap(~trace)
p <- p + theme_bw() + xlab(NULL) + opts(axis.text.x  = theme_text(angle=45, hjust = 1, vjust = 1))
ggsave(p, filename=paste(file, "bar_optype.png", sep="_"))
