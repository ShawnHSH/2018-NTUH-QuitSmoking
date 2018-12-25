import os
import csv
from collections import OrderedDict
import matplotlib.pyplot as plt
import codecs
import chardet
import re
from pylab import mpl
import pandas as pd
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

csv_file_Transactions = open("./transactions_class4.csv",'w',encoding='UTF-8',newline="")
csv_file_Transactions_Med = open("./transactions_Med_class4.csv",'w',encoding='UTF-8',newline="")
csv_file_Transactions_Check = open("./transactions_Check_class4.csv",'w',encoding='UTF-8',newline="")
csv_file_Medicine = open("./Medicine_class4.csv",'w',encoding="UTF-8",newline="")
csv_file_Check = open("./check_class4.csv",'w',encoding="UTF-8",newline="")

csv_write_Transaction = csv.writer(csv_file_Transactions)
csv_write_Transaction_Med = csv.writer(csv_file_Transactions_Med)
csv_write_Transaction_Check = csv.writer(csv_file_Transactions_Check)
csv_write_Medicine = csv.writer(csv_file_Medicine)
csv_write_Check = csv.writer(csv_file_Check)

transaction = []
transaction_Med = []
transaction_Check = []

i = 0
#define the regular expression rule of percentage such as "56.3%"
value = re.compile(r'[0-9]+\.?[0-9]*\%?$')


classpath = "C:\\Users\\Harold\\Desktop\\WordExtract\\patients\\utf8"
class_assessment = ["\\class_2_4","\\class_2_1_4","\\class_3_4"]
check = {}
medicine = {}
for num in range(0,3):
    path = classpath+class_assessment[num]
    fs = os.listdir(path)

    for f in fs:
        submed = {}
        subcheck = {}
        for line in open(path+'\\'+f,'r',encoding='UTF-8'):
            if(line == "" and line == " "):
                continue
            else:
                str_list = line.split(" ")
                # if(flag == 'N' and str_list[0] == "商品名"):
                #     flag = 'M'
                #     continue
                if ("健保" in str_list):
                    i = 0
                    str = str_list[i]

                    while (not (value.match(str_list[i + 1]))):
                        str = " ".join((str, str_list[i + 1]))
                        i = i + 1
                    str = "_".join((str,"MEDICINE"))
                    #print("藥品: "+str)
                    if(str not in submed):
                        submed[str] = 1
                        transaction.append(str)
                        transaction_Med.append(str)
                        csv_write_Medicine.writerow([str])
                        if(str not in medicine):
                            medicine[str] = 1
                        else:
                            medicine[str] += 1

                    continue
                if( str_list[0] == "檢驗"):
                    #flag = "N"
                    i = 2
                    str = str_list[i]
                    while (not (value.match(str_list[i + 1]))):
                        str = " ".join((str, str_list[i + 1]))
                        i = i + 1
                    str = "_".join((str,"CHECK"))
                    #print("檢驗："+str)
                    if (str not in subcheck):
                        subcheck[str] = 1
                        transaction.append(str)
                        transaction_Check.append(str)
                        csv_write_Check.writerow([str])
                        if (str not in check):
                            check[str] = 1
                        else:
                            check[str] += 1
                    continue
        #remove the quit smoking drug
        if ("Nicorette Freshmint medicated chewing-gum_MEDICINE" in transaction):
            transaction.remove("Nicorette Freshmint medicated chewing-gum_MEDICINE")
            transaction_Med.remove("Nicorette Freshmint medicated chewing-gum_MEDICINE")
        if ("30 Nicotinell TTS_MEDICINE" in transaction):
            transaction.remove("30 Nicotinell TTS_MEDICINE")
            transaction_Med.remove("30 Nicotinell TTS_MEDICINE")
        if ("20 Nicotinell TTS_MEDICINE" in transaction):
            transaction.remove("20 Nicotinell TTS_MEDICINE")
            transaction_Med.remove("20 Nicotinell TTS_MEDICINE")
        if ("1 Champix FC_MEDICINE" in transaction):
            transaction.remove("1 Champix FC_MEDICINE")
            transaction_Med.remove("1 Champix FC_MEDICINE")
        if(num == 0):
            transaction.append("Nicotinell TTS_SMOKE")
            transaction_Med.append("Nicotinell TTS_SMOKE")
            transaction_Check.append("Nicotinell TTS_SMOKE")
        elif(num == 1):
            transaction.append("Nicotinell TTS&Chewing Gum_SMOKE")
            transaction_Med.append("Nicotinell TTS&Chewing Gum_SMOKE")
            transaction_Check.append("Nicotinell TTS&Chewing Gum_SMOKE")
            #transaction.append("Chewing Gum_SMOKE")
        elif(num ==2):
            transaction.append("Champix tablet_SMOKE")
            transaction_Med.append("Champix tablet_SMOKE")
            transaction_Check.append("Champix tablet_SMOKE")

        csv_write_Transaction.writerow(transaction)
        csv_write_Transaction_Med.writerow(transaction_Med)
        csv_write_Transaction_Check.writerow(transaction_Check)

        transaction = []
        transaction_Med = []
        transaction_Check = []

csv_file_Check.close()
csv_file_Medicine.close()
csv_file_Transactions.close()
csv_file_Transactions_Med.close()
csv_file_Transactions_Check.close()

print(medicine)
print(check)
sorted_medicine = OrderedDict(sorted(medicine.items(),key = lambda item: item[1],reverse = False))
#plot barsh diagram
plt.barh(list(sorted_medicine.keys()),list(sorted_medicine.values()))
plt.show()

sorted_medicine = OrderedDict(sorted(check.items(),key = lambda item: item[1],reverse = False))
#plot barsh diagram
plt.barh(list(sorted_medicine.keys()),list(sorted_medicine.values()))
plt.show()
