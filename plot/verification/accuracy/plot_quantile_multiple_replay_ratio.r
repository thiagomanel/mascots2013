library("plyr")
library("ggplot2")

Args <- commandArgs(TRUE)
file <- Args[1]

replay <- read.table(file, header = T)

replay <- subset(replay, replay$order %in% c("fs", "con"))
replay <- subset(replay, replay$timing %in% c("timestamp"))
replay <- subset(replay, replay$delay > 0)
replay <- subset(replay, replay$replay_ratio > 0)
levels(replay$order)[levels(replay$order)=="fs"] <- "FS"
levels(replay$order)[levels(replay$order)=="con"] <- "Conservative"
names(replay)[names(replay)=="id"]  <- "Delay"

cdata <- ddply(replay, .(order, timing, Delay), transform, ecd = ecdf(replay_ratio)(replay_ratio))
p <- ggplot(cdata, aes(y=ecd, x=replay_ratio)) + geom_point(aes(group=factor(Delay), colour=factor(Delay), shape=factor(Delay))) + scale_colour_hue(name="Delay") + scale_shape_manual(name="Delay", values=c(0, 4, 6)) + ylab("Cumulative Probability") + xlab("Compute Time Error Ratio") + theme_bw()
p <- p + facet_grid(order ~ .)
ggsave(p, file="compute_time_ratio_multiple_quantile.png")


replay_limit <- subset(replay, replay$replay_ratio <= 1)
cdata <- ddply(replay_limit, .(order, timing, Delay), transform, ecd = ecdf(replay_ratio)(replay_ratio))
p <- ggplot(cdata, aes(y=ecd, x=replay_ratio)) + geom_point(aes(group=factor(Delay), colour=factor(Delay), shape=factor(Delay))) + scale_x_log10() + scale_colour_hue(name="Delay") + scale_shape_manual(name="Delay", values=c(0, 4, 6)) + ylab("Cumulative Probability") + xlab("Compute Time Error Ratio") + theme_bw()
p <- p + facet_grid(order ~ .)
ggsave(p, file="compute_time_ratio_multiple_log_quantile.png")
