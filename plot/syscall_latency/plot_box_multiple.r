library("plyr")
library("ggplot2")

Args <- commandArgs(TRUE)
file <- Args[1]

replay <- read.table(file, header = T)

replay <- subset(replay, replay$operation_type %in% c("read", "write"))
replay <- subset(replay, replay$order %in% c("fs", "con"))
replay <- subset(replay, replay$timing %in% c("fullspeed", "timestamp"))

levels(replay$order)[levels(replay$order)=="fs"] <- "FS"
levels(replay$order)[levels(replay$order)=="con"] <- "Conservative"

levels(replay$id)[levels(replay$id)=="10usec"] <- "10"
levels(replay$id)[levels(replay$id)=="100usec"] <- "100"
levels(replay$id)[levels(replay$id)=="1000usec"] <- "1000"

png("cat_latency_box.png")
p <- ggplot(replay, aes(factor(id), latency)) + geom_boxplot() + coord_flip() + scale_y_log10() + theme_bw()
p + facet_grid(order ~ .) + ylab("Response Time (microseconds)") + xlab("Additional delay (microseconds)")
dev.off()
