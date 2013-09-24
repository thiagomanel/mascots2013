library("plyr")
library("ggplot2")
library(scales)

#It sums up all operations latency. So we exclude idle intervals.
Args <- commandArgs(TRUE)
file <- Args[1]

replay <- read.table(file, header = T)

replay <- subset(replay, replay$order %in% c("fs", "con"))
replay <- subset(replay, replay$timing %in% c("timestamp"))
levels(replay$order)[levels(replay$order)=="fs"] <- "FS"
levels(replay$order)[levels(replay$order)=="con"] <- "Conservative"

replay <- subset(replay, replay$delay > 0)
replay$issue_error <- abs(replay$issue_error)

#ALL
cdata <- ddply(replay, .(order, timing), transform, ecd = ecdf(issue_error)(issue_error))
p <- ggplot(cdata, aes(y=ecd, x=issue_error)) + geom_point(aes(group=order, colour = order, shape=order)) + scale_shape_manual(values=c(0, 4)) + ylab("Cumulative Probability") + xlab("Issue Error (microseconds)") + theme_bw()
ggsave(p, file="issue_error_quantile.png")
p <- ggplot(cdata, aes(y=ecd, x=issue_error)) + geom_point(aes(group=order, colour = order, shape=order)) + scale_shape_manual(values=c(0, 4))  + scale_x_log10() + ylab("Cumulative Probability") + xlab("Issue Error (microseconds)") + theme_bw()
ggsave(p, file="issue_error_quantile_zoomed.png")

#FS
replay_fs <- subset(replay, replay$order %in% c("FS"))
cdata <- ddply(replay_fs, .(order, timing), transform, ecd = ecdf(issue_error)(issue_error))
p <- ggplot(cdata, aes(y=ecd, x=issue_error)) + geom_point(aes(group=order, colour = order, shape=order)) + scale_shape_manual(values=c(0, 4))  + scale_x_log10() + ylab("Cumulative Probability") + xlab("Issue Error (microseconds)") + theme_bw()
ggsave(p, file="issue_error_quantile_fs.png")

#CON
replay_con <- subset(replay, replay$order %in% c("Conservative"))
cdata <- ddply(replay_con, .(order, timing), transform, ecd = ecdf(issue_error)(issue_error))
p <- ggplot(cdata, aes(y=ecd, x=issue_error)) + geom_point(aes(group=order, colour = order, shape=order)) + scale_shape_manual(values=c(0, 4))  + scale_x_log10() + ylab("Cumulative Probability") + xlab("Issue Error (microseconds)") + theme_bw()
ggsave(p, file="issue_error_quantile_con.png")
