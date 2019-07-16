 # Author: Shihao Hong(Harold), undergraduate student of computer science
 #         at Hefei University of Technology
 # Target: to group patients according to medication and smoking cessation effects
library(xlsx)
library(ggplot2)
library(data.table)
workbook <- "C:\\Users\\Harold\\Desktop\\ntuh\\NTUH_big5.xlsx"
mydataframe <- read.xlsx(workbook,sheetIndex = 1,encoding = 'UTF-8')
mydataframe <-mydataframe[, apply(mydataframe,2,function(x)!all(is.na(x)))]

 # Function Name: GetLastnum
 # To get the latest valid value. In this program, 
 # these six input values are data on the number of
 # recent smoking in the patient's six questionnaires.
 # The purpose of this function is to get the patient's last smoking.
GetLastnum <- function(num1,num2,num3,num4,num5,num6){
  if(!is.na(num6))
  {
    return (num6)
  } else if(!is.na(num5))
  {
    return(num5)
  } else if(!is.na(num4))
  {
    return(num4)
  } else if(!is.na(num3))
  {
    return(num3)
  } else if(!is.na(num2))
  {
    return(num2)
  } else if(!is.na(num1))
  {
    return(num1)
  } else{
    return(-1)
  }
}

 # Function Name: GetAssessment
 # input: "firstgrade" is the Cigarette addiction index for the first survey
 #        "lastnum" is the patient's last smoking.
 # output:"assess" is a quantitative assessment of the effectiveness of
 #        smoking cessation for patients
GetAssessment <- function(firstgrade,lastnum){
  assess <- lastnum / log(exp(1)+firstgrade)
  return (assess)
}

 # Function Name: GetFrequency
 # Usage: Convert numbers into words
GetFrequency <- function(times){
  if(times>=5){
    return("five")
  }
  if(times == 4){
    return("four")
  }
  if(times == 3){
    return("three")
  }
  if(times == 2){
    return("twice")
  }
  if(times == 1){
    return("once")
  }
}
 # Function Name: GetClass
 # Usage: Divide the quantitative evaluation range into four intervals
 #        and mark them with A, B, C, and D levels.
GetClass <- function(assessment){
  if(assessment == 0){
    return("A")
  }else if(assessment < 5){
    return("B")
  }else if(assessment < 10){
    return("C")
  }else{
    return("D")
  }
}

mydataframe$lastnum <- mapply(GetLastnum, mydataframe$Current_Average_Smoking1,mydataframe$Current_Average_Smoking2,
            mydataframe$Current_Average_Smoking3,mydataframe$Current_Average_Smoking4,
            mydataframe$Current_Average_Smoking5,mydataframe$Current_Average_Smoking6)
mydataframe$assessment <- mapply(GetAssessment,mydataframe$times,mydataframe$lastnum)
mydataframe$class <- mapply(GetClass,mydataframe$assessment)
mydataframe$frequency <- mapply(GetFrequency,mydataframe$times)
View(mydataframe)

 # effectivedata: gets rid of patients who have only visited the clinic once
 # selectdata observe patients whose assessment is greater than 0
 # Medicine?data analyse each kind of medicine separately
effectivedata <- mydataframe[mydataframe$times>1,]
selectdata <- effectivedata[effectivedata$assessment>0,]

 # to draw a patient's assessment score distribution map
theme_set(theme_classic())
g <- ggplot(selectdata,aes(assessment)) + 
geom_histogram(bins = 5,col = "black",size = .1) 
plot(g)

#ggplot(selectdata,aes(x =assessment , y =times )) + geom_point(size = 3)
#ggplot(selectdata,aes(x = assessment))+geom_histogram(binwidth=.5)
 
#ggplot(selectdata,aes(x = times))+geom_histogram(binwidth=.5)

 # Pick out patients who take chewing gum drugs(drug1)
Medicine1data <- effectivedata[effectivedata$prescription1_1 == "Nicorette Freshmint medicated Chewing Gum 2mg",]
Medicine2_1data <- effectivedata[effectivedata$prescription1_1 == "Nicotinell TTS 30" | effectivedata$prescription1_1 == "Nicotinell TTS 20",]
 # Pick out patients taking oral medications(drug2)
Medicine2data <- Medicine2_1data[is.na(Medicine2_1data$prescription1_2),]
 # Pick out patients who take patch-type drugs(drug3)
Medicine3data <- effectivedata[effectivedata$prescription1_1 == "Champix film coated tablet 1.0mg",]
 # Pick out patients who take chewing gum and oral medications(drug2_1)
Medicine2_1data <- Medicine2_1data[!is.na(Medicine2_1data$prescription1_2),]

View(Medicine1data)
View(Medicine2data)
View(Medicine2_1data)
View(Medicine3data)
length(effectivedata$serial..Number)

g <- ggplot(effectivedata,aes(assessment)) + 
  geom_histogram(aes(fill = c(prescription1_1,prescription1_2)),bins = 6,
                 col = "black", size = .1) +labs(title="Medicine type and assessment")

 # To draw a pie chart of the assessment class distribution of patients
 # taking the drug1(Nicorette Freshmint medicated Chewing Gum 2mg)
theme_set(theme_classic())
pie <- ggplot(Medicine1data, aes(x = "", fill = factor(class))) + 
  geom_bar(width = 1) +
  theme(axis.line = element_blank(), 
        plot.title = element_text(hjust=0.5)) + 
  labs(fill="class", 
       x=NULL, 
       y=NULL, 
       title="Pie Chart of class", 
       caption="Source: Medicine1data")+coord_polar(theta = "y", start=0)
plot(pie)

var <- Medicine3data$class
nrows <- 10
df <- expand.grid(y = 1:nrows, x = 1:nrows)
categ_table <- round(table(var) * ((nrows*nrows)/(length(var))))
categ_table

df$class <- factor(rep(names(categ_table), categ_table))  

ggplot(df, aes(x = x ,y = y, fill = class)) + 
  geom_tile(color = "black", size = 0.5) + 
  scale_x_continuous(expand = c(0,0)) +
  scale_y_continuous(expand = c(0,0)) +
  scale_fill_brewer(palette = "Set3") +
  labs(title ="Champix film coated tablet 1.0mg",caption = "Source: Medicine1data" )

df1_1 <- Medicine1data[Medicine1data$assessment == 0,]
df1_1 <- subset(df1_1, select = c(serial..Number,assessment))

df1_2 <- Medicine1data[Medicine1data$assessment >0 &Medicine1data$assessment<5,]
df1_2 <- subset(df1_2, select = c(serial..Number,assessment))

df1_3 <- Medicine1data[Medicine1data$assessment >5 &Medicine1data$assessment<10,]
df1_3 <- subset(df1_3, select = c(serial..Number,assessment))

df1_4 <- Medicine1data[Medicine1data$assessment >10,]
df1_4 <- subset(df1_4, select = c(serial..Number,assessment))

df2_1 <- Medicine2data[Medicine2data$assessment == 0,]
df2_1 <- subset(df2_1, select = c(serial..Number,assessment))

df2_2 <- Medicine2data[Medicine2data$assessment >0 &Medicine2data$assessment<5,]
df2_2 <- subset(df2_2, select = c(serial..Number,assessment))

df2_3 <- Medicine2data[Medicine2data$assessment >5 &Medicine2data$assessment<10,]
df2_3 <- subset(df2_3, select = c(serial..Number,assessment))

df2_4 <- Medicine2data[Medicine2data$assessment >10,]
df2_4 <- subset(df2_4, select = c(serial..Number,assessment))

df3_1 <- Medicine3data[Medicine3data$assessment == 0,]
df3_1 <- subset(df3_1, select = c(serial..Number,assessment))

df3_2 <- Medicine3data[Medicine3data$assessment >0 &Medicine3data$assessment<5,]
df3_2 <- subset(df3_2, select = c(serial..Number,assessment))

df3_3 <- Medicine3data[Medicine3data$assessment >5 &Medicine3data$assessment<10,]
df3_3 <- subset(df3_3, select = c(serial..Number,assessment))

df3_4 <- Medicine3data[Medicine3data$assessment >10,]
df3_4 <- subset(df3_4, select = c(serial..Number,assessment))

df2_1_1 <- Medicine2_1data[Medicine2_1data$assessment == 0,]
df2_1_1 <- subset(df2_1_1, select = c(serial..Number,assessment))

df2_1_2 <- Medicine2_1data[Medicine2_1data$assessment >0 &Medicine2_1data$assessment<5,]
df2_1_2 <- subset(df2_1_2, select = c(serial..Number,assessment))

df2_1_3 <- Medicine2_1data[Medicine2_1data$assessment >5 &Medicine2_1data$assessment<10,]
df2_1_3 <- subset(df2_1_3, select = c(serial..Number,assessment))

df2_1_4 <- Medicine2_1data[Medicine2_1data$assessment >10,]
df2_1_4 <- subset(df2_1_4, select = c(serial..Number,assessment))

 fwrite(df1_1,"C:\\Users\\Harold\\Desktop\\ntuh\\df1_1.csv")
 fwrite(df1_2,"C:\\Users\\Harold\\Desktop\\ntuh\\df1_2.csv")
 fwrite(df1_3,"C:\\Users\\Harold\\Desktop\\ntuh\\df1_3.csv")
 fwrite(df1_4,"C:\\Users\\Harold\\Desktop\\ntuh\\df1_4.csv")
 
 
 fwrite(df2_1,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_1.csv")
 fwrite(df2_2,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_2.csv")
 fwrite(df2_3,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_3.csv")
 fwrite(df2_4,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_4.csv")
 
 
 fwrite(df3_1,"C:\\Users\\Harold\\Desktop\\ntuh\\df3_1.csv")
 fwrite(df3_2,"C:\\Users\\Harold\\Desktop\\ntuh\\df3_2.csv")
 fwrite(df3_3,"C:\\Users\\Harold\\Desktop\\ntuh\\df3_3.csv")
 fwrite(df3_4,"C:\\Users\\Harold\\Desktop\\ntuh\\df3_4.csv")
 
 fwrite(df2_1_1,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_1_1.csv")
 fwrite(df2_1_2,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_1_2.csv")
 fwrite(df2_1_3,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_1_3.csv")
 fwrite(df2_1_4,"C:\\Users\\Harold\\Desktop\\ntuh\\df2_1_4.csv")
 

View(df1_1)
View(df1_2)
View(df1_3)
View(df1_4)
View(df2_1)
View(df2_2)
View(df2_3)
View(df2_4)
View(df2_1_1)
View(df2_1_2)
View(df2_1_3)
View(df2_1_4)
View(df3_1)
View(df3_2)
View(df3_3)
View(df3_4)

length(df1_1$serial..Number)
length(df1_2$serial..Number)
length(df1_3$serial..Number)
length(df1_4$serial..Number)

length(Medicine3data$serial..Number)
length(selectdata$serial..Number)



