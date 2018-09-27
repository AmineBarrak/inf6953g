# Your data
hadoop <- c(4.16,4.188,4.244,4.173,4.146,4.071,4.093,4.267,4.423)
ubuntu<- c(0.803,0.857,	0.745	,0.731	,0.864	,0.986,	0.832,	0.829,	0.855)
spark <- c(6.541	,6.672,	6.435,	6.399	,6.511	,6.429	,6.416	,6.517	,6.456)

#Graph cars using a y axis that ranges from 0 to 12
plot(hadoop, type="o", col=plot_colors[1], ylim=c(0,12),lwd=2.5,  cex=2, ann=FALSE)

#lines(d3, type='o', col='black', lwd=2.5, pch=15, cex=2.5)
# Graph trucks with red dashed line and square points
lines(ubuntu, type="o", pch=22,  lwd=2.5, cex=2,col=plot_colors[2])

lines(spark, type="o", pch=23, lwd=2.5, cex=2,col=plot_colors[3])
# Create a title with a red, bold/italic font
#title(main="Comparaison de performance hadoop, spark et ubuntu", cex.main=1.7,col.main="red", font.main=4)

# Label the x and y axes with dark green text
title(xlab= "Iteration", cex.lab=1.5,col.lab=rgb(0,0.5,0))
title(ylab= "Temps (s)",cex.lab=1.3, col.lab=rgb(0,0.5,0), line = 3)


legend(1, 12, legend=c("hadoop", "ubuntu","spark"),
       col=c(plot_colors[1], plot_colors[2],plot_colors[3]), lty=1,lwd=2.5,cex=1.3,text.font=4, bg='lightblue')