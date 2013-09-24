# It plot load by time
library("ggplot2")

args <- commandArgs(TRUE)
file_in <- args[1]
file_out <- args[2]

# relat_stamp abs_stamp count
in_data <- read.table(file_in, header=T)
in_data$load_type = "dispatch"
in_data$sample = 0
in_data2 <- in_data

in_data$order = "Original Workload"
in_data$timing = "fullspeed"

in_data2$order = "Original Workload"
in_data2$timing = "timestamp"

#order timing relatitve_stamp abs_stamp count case={dispatch, running} sample order timing
out <- read.table(file_out, header=T)
levels(out$order)[levels(out$order)=="fs"] <- "FS"
levels(out$order)[levels(out$order)=="con"] <- "Conservative"

# ordering polices, faced by timing polices
out = subset(out, load_type == "dispatch")
out = subset(out, sample %in% c(0))
merged = merge(merge(in_data, out, all=TRUE), in_data2, all=TRUE)
merged$relative_stamp = merged$relative_stamp/1000000

p <- ggplot(merged, aes(relative_stamp, load)) + geom_point(aes(group=order, colour=order, shape=order)) + scale_shape_manual(values=c(0, 4, 6)) + scale_y_log10() 
p <- p + facet_grid(. ~ timing) + ylab("Request Load") + xlab("Time (seconds)")+ theme_bw() + theme(legend.position="top")
ggsave(p, file="merge_abelhinha.png")
