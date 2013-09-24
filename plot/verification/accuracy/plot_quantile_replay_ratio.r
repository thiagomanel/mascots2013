library("plyr")
library("ggplot2")

Args <- commandArgs(TRUE)
file <- Args[1]

replay <- read.table(file, header = T)

replay <- subset(replay, replay$order %in% c("fs", "con"))
replay <- subset(replay, replay$timing %in% c("timestamp"))
summary(replay)
replay <- subset(replay, replay$delay > 0)
replay <- subset(replay, replay$replay_ratio > 0)
levels(replay$order)[levels(replay$order)=="fs"] <- "FS"
levels(replay$order)[levels(replay$order)=="con"] <- "Conservative"
summary(replay)

cdata <- ddply(replay, .(order, timing), transform, ecd = ecdf(replay_ratio)(replay_ratio))

p <- ggplot(cdata, aes(y=ecd, x=replay_ratio)) + geom_point(aes(group=order, colour = order, shape=order)) + scale_shape_manual(values=c(0, 4)) + ylab("Cumulative Probability") + xlab("Compute Time Error Ratio") + theme_bw()
ggsave(p, file="compute_time_ratio_quantile.png")

p <- ggplot(cdata, aes(y=ecd, x=replay_ratio)) + geom_point(aes(group=order, colour = order, shape=order)) + scale_x_log10() + scale_shape_manual(values=c(0, 4)) + ylab("Cumulative Probability") + xlab("Compute Time Error Ratio") + theme_bw()
ggsave(p, file="compute_time_ratio_log_quantile.png")
