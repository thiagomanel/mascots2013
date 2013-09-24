# It plot load by time
library("ggplot2")

args <- commandArgs(TRUE)
file_in <- args[1]
# relat_stamp abs_stamp count trace
data <- read.table(file_in, header=T)

p <- ggplot(data, aes(relative_stamp/1000000, load)) + geom_point() + scale_y_log10()
p <- p + facet_grid(trace ~.) + ylab("Request Load") + xlab("Time (seconds)") + theme_bw()
ggsave(p, filename=paste(file_in, "load_in_multiple.png", sep = "_"))
