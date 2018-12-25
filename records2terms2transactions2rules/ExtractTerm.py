#it is a test program
import os
import codecs
import chardet
str1 = "商品名 劑量 頻率 途徑 天數 總量 記帳 連續 日期 狀態 開立者"
str2 = "1 Champix FC 1 mg/tab 1 tab BID PO 7 14 tab 健保  2016/02/26 已確認 已批 王維典 重複原因:病人因素(補給天數並延後回診)"
str3 = "Naposin 250 mg/tab 1 tab BIDPC PO 28 56 tab 健保  2015/11/06 已確認 已批 林峰盛  "
str4 = "Rinderon Inj 4 mg/1 mL /amp 8 mg STAT IV 1 2 amp 健保  2015/06/30 已確認 已批 林峰盛  "
str_list = str3.split(" ")
i = 0
if(str_list[0].isalpha()):
    str = str_list[i]
    while(str_list[i+1].isalpha()):
        str = " ".join((str,str_list[i+1]))
        i = i+1
        break
else:
     i = i+1
     str = str_list[i]
     while (str_list[i + 1].isalpha()):
         str = " ".join((str,str_list[i+1]))
         i = i + 1
         break

for line in open("patients/big5/48.txt",'r',encoding='BIG5'):
    print(line)

