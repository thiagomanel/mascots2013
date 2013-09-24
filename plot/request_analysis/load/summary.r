library("plyr")

args <- commandArgs(TRUE)
file_in <- args[1]
# relat_stamp abs_stamp count trace
data <- read.table(file_in, header=T)

co.var <- function(x,na.rm=TRUE) 100*(sd(x,na.rm=na.rm)/mean(x,na.rm=na.rm))

for (t in levels(data$trace)) {
    sub = subset(data, data$trace %in% c(t))
    print(t)
    print(summary(sub$load))
    print(co.var(sub$load))
}

#cdata <- ddply(data, .(trace), transform, cov = co.var(count)(count))
#summary(cdata)
