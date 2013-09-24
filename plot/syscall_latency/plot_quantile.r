library("plyr")
library("ggplot2")

#http://www.cookbook-r.com/Graphs/Legends_%28ggplot2%29/
#http://www.cookbook-r.com/Graphs/Shapes_and_line_types/

Args <- commandArgs(TRUE)
fileName <- Args[1]

replay <- read.table(fileName, header = T)

replay <- subset(replay, replay$operation_type %in% c("read", "write"))
replay_limit200 <- subset(replay, replay$latency <= 200)
#levels(replay$order)[levels(replay$order)=="fs"] <- "FS"
#levels(replay$order)[levels(replay$order)=="con"] <- "Conservative"

cdata <- ddply(replay, .(operation_type, order, timing), transform, ecd = ecdf(latency)(latency))

p <- ggplot(cdata, aes(x=latency, y=ecd)) + geom_point(aes(group=order, colour=order, shape=order)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_x_log10()
p <- p + facet_grid(operation_type ~ timing, scales ="free") + ylab("Cumulative Probability") + xlab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_latency_quantiles.png", sep="."))
p <- ggplot(cdata, aes(x=latency, y=ecd)) + geom_point(aes(group=timing, colour=timing, shape=timing)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_x_log10()
p <- p + facet_grid(operation_type ~ order, scales ="free") + ylab("Cumulative Probability") + xlab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_latency_quantiles_grouped_by_timing.png", sep="."))

p <- ggplot(cdata, aes(y=latency, x=ecd)) + geom_point(aes(group=order, colour=order, shape=order)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_y_log10()
p <- p + facet_grid(operation_type ~ timing, scales = "free") + xlab("Cumulative Probability") + ylab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_latency_quantiles_inverted.png", sep="."))
p <- ggplot(cdata, aes(y=latency, x=ecd)) + geom_point(aes(group=timing, colour=timing, shape=timing)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_y_log10()
p <- p + facet_grid(operation_type ~ order, scales = "free") + xlab("Cumulative Probability") + ylab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_latency_quantiles_inverted_grouped_by_timing.png", sep="."))

p <- ggplot(cdata, aes(x=latency, y=ecd)) + geom_point(aes(group=order, colour=order, shape=order)) + scale_x_continuous(limits=c(0, 200)) + scale_shape_manual(values=c(0, 4, 6,8))
p <- p + facet_grid(operation_type ~ timing, scales ="free") + ylab("Cumulative Probability") + xlab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_latency_quantiles_limit200.png", sep="."))


cdata <- subset(cdata, cdata$ecd <= 0.99)
p <- ggplot(cdata, aes(x=latency, y=ecd)) + geom_point(aes(group=order, colour=order, shape=order)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_x_log10()
p <- p + facet_grid(operation_type ~ timing, scales = "free") + ylab("Cumulative Probability") + xlab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_99latency_quantiles.png", sep="."))
p <- ggplot(cdata, aes(x=latency, y=ecd)) + geom_point(aes(group=timing, colour=timing, shape=timing)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_x_log10()
p <- p + facet_grid(operation_type ~ order, scales = "free") + ylab("Cumulative Probability") + xlab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_99latency_quantiles_grouped_by_timing.png", sep="."))

p <- ggplot(cdata, aes(y=latency, x=ecd)) + geom_point(aes(group=order, colour=order, shape=order)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_y_log10()
p <- p + facet_grid(operation_type ~ timing, scales = "free") + xlab("Cumulative Probability") + ylab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_99latency_quantiles_inverted.png", sep="."))
p <- ggplot(cdata, aes(y=latency, x=ecd)) + geom_point(aes(group=timing, colour=timing, shape=timing)) + scale_shape_manual(values=c(0, 4, 6,8)) + scale_y_log10()
p <- p + facet_grid(operation_type ~ order, scales = "free") + xlab("Cumulative Probability") + ylab("Response Time (microseconds)") + theme_bw()
ggsave(p, file=paste(fileName, "scaled_99latency_quantiles_inverted_grouped_by_timing.png", sep="."))
