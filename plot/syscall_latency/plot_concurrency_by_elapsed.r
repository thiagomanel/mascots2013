library("plyr")
library("ggplot2")

Args <- commandArgs(TRUE)
fileName <- Args[1]
#operation_type  latency actual_rvalue   tid     stamp   order   timing  sample  concurrency     cgroup
data <- read.table(fileName, header = T)

replay <- subset(data, data$operation_type %in% c("read"))
summary(replay)

#histogram filled by concurrency
p <- ggplot(replay, aes(x=latency, fill=factor(concurrency))) + scale_fill_grey(name="Concurrency\nLevel") + geom_histogram(binwidth = 1) + scale_x_continuous(limits=c(0, 20))
p <- p + ylab(NULL) + xlab("Response Time (microseconds)")
p <- p + facet_grid(order ~ .) + theme_bw()
ggsave(p, filename=paste(fileName, "hist_limit_20_read_by_order_concurrencyfill.png", sep="_"))
