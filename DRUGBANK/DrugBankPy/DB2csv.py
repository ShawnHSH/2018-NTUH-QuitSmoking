import io
import sys
import xml.etree.ElementTree as ET
import untangle
import pandas as pd

i = 0
filepath = "full_database.xml"
df_drugbank = pd.DataFrame(
    columns=["name","type","description"]
)
context = ET.iterparse(filepath,events=('start',))
for event,elem in context:
    #元素标签有点奇怪，但确实是{http://www.drugbank.ca}drug，需要仔细观察xml文档
    if ((elem.tag == "{http://www.drugbank.ca}drug" or elem.tag == "drug") and len(elem.attrib)):
        for key in elem.attrib.keys():
            if(key == "type"):
                attr = elem.attrib[key]
                #print(attr)
                df_drugbank.loc[i, "type"] =attr
                break
        for child in elem:
            if (child.tag == "{http://www.drugbank.ca}name" or child.tag == "name" ):
                text = child.text
                #不知道为什么抓不到Denileukin diftitox这个药
                if(text == "Denileukin diftitox"):
                    df_drugbank.loc[i, "name"] = child.text
                    print("got it!")
                    break
                df_drugbank.loc[i,"name"] = child.text
                #print(child.text)
                break

        #print(elem.attrib["type"])
        # for child in elem:
        i = i + 1
        elem.clear()
#会有点慢，毕竟700多M的xml，但是这个时间复杂度我也是不满意的...
df_drugbank.to_csv("drugbank.csv", encoding='utf-8', index=False)

