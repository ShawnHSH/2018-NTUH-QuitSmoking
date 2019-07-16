# Author: Shihao Hong(Harold), undergraduate student of computer science
#         at Hefei University of Technology
# Target: to draw association rules graph using the transactions we produced.
library(arules)
library(Matrix)
library(grid)
library(arulesViz)
library(data.table)
transactions <- read.transactions("transactions_Check_class4.csv",
                                  format="basket",sep = ",",skip=0,encoding = 'UTF-8')
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
 # Filter out medical records that contain only one drug/test
transactions_use <- transactions[basketSize>1]
dim(transactions_use)
dim(transactions)

myRules <- apriori(transactions_use,
                   parameter = list(support = 0.25,
                                    confidence = 0.8,
                                    minlen = 2,maxlen = 20))
summary(myRules)
inspect(myRules[1:5])

ordered_myRules <- sort(myRules,by = "lift")
inspect(ordered_myRules[1:10])
myRules@quality$lift2 <- floor(myRules@quality$lift*100)/100
ordered_myRules2 <- sort(myRules,by=c("lift","support"))
inspect(ordered_myRules2[1:10])
top.vegie.rules <- sort(ordered_myRules2,
                        by = c("support","lift"))[1:30]

summary(top.vegie.rules)
plot(top.vegie.rules,measure="support",
     method="graph",
     shading="lift",
     cex = 0.7,
     lwd = 2)
write(ordered_myRules2,fileEncoding = "UTF-8",sep=",",quote=TRUE,file = "./class4Rules_Check.csv",row.names=FALSE)

