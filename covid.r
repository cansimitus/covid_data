df <- read.table("covid_tr.txt", header = TRUE)
df$date <- as.Date(df$date, format="%d.%m.%Y")

par(mar = c(5,5,2,5))
with(df, plot(date, conf_total, xlab="", ylab="", type = "b", xaxt="n", yaxt="n"))
axis.Date(1, at=seq(min(df$date), max(df$date), by="days"), format="%d-%m-%Y", las = 2, cex.axis = 0.5, font = 2, family = 'mono')
par(new = T)
with(df, plot(date, deaths_total, xlab="", ylab="", type = "b", xaxt="n", yaxt="n", col="red3"))
par(new = T)
with(df, plot(date, rec_total, xlab="", ylab="", type = "b", xaxt="n", yaxt="n", col="green"))
par(new = T)
with(df, plot(date, intube_total, xlab="", ylab="", type = "b", xaxt="n", yaxt="n", col="cyan"))
par(new = T)
with(df, plot(date, severe_total, xlab="", ylab="", type = "b", xaxt="n", yaxt="n", col="blue"))
par(new = T)
with(df, plot(date, tests_total, xlab="", ylab="", type = "b", xaxt="n", yaxt="n", col="yellow"))

legend("topleft",
       legend=c("Deaths#","Cases#", "Recovered#","Intube#","Severe#","Test#"),
       lty=c(0,0,0,0,0,0), pch=c(1,1,1,1,1,1), col=c("red3", "black", "green","cyan","blue","yellow"))
