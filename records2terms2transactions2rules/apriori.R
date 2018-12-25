library(arules)
library(Matrix)
library(grid)
library(arulesViz)
library(data.table)
transactions <- read.transactions("transactions_Med_class4.csv",
                                  format="basket",sep = ",",skip=0)
summary(transactions)
mx1 <- as(transactions,"matrix")
dim(mx1)
head(mx1[,0:5])

basketSize <- size(transactions)
table(basketSize)
basketSize
itemFreq <- itemFrequency(transactions)
head(itemFreq[order(-itemFreq)])
#itemFrequencyPlot(transactions,support = quantile(itemFreq,0.9))
#过滤只有一种药/检验的病历
transactions_use <- transactions[basketSize>1]
dim(transactions_use)
dim(transactions)

myRules <- apriori(transactions,
                   parameter = list(support = 0.1,
                                    confidence = 0.4,
                                    minlen = 2,maxtime = 500))
summary(myRules)

inspect(myRules[1:10])

ordered_myRules <- sort(myRules,by = "lift")

inspect(ordered_myRules[1:10])

myRules@quality$lift2 <- floor(myRules@quality$lift*100)/100
ordered_myRules2 <- sort(myRules,by=c("lift2","support"))
inspect(ordered_myRules2[1:10])

top.vegie.rules <- sort(ordered_myRules2,
                        by = c("support","lift"))[1:30]
plot(top.vegie.rules,measure="support",
     method="graph",
     shading="lift",
     cex = 0.7,
     lwd = 2)
write(ordered_myRules2,fileEncoding = "UTF-8",sep=",",quote=TRUE,file = "./class4Rules_Med.csv",row.names=FALSE)
