# In[1]:

import untangle
import pandas as pd
from xml.etree import ElementTree as ET
import numpy as np
import os

# In[3]:
# Building dataframe of chemical descriptors
# Data Frame of DrugBank Small Molecule Type Drugs
df_drugbank_sm = pd.DataFrame(
    columns=["drugbank_id", "name", "cas"])
df_drugbank_sm

filename = "full_database.xml"
parser = ET.iterparse(filename)

obj = untangle.parse(filename)



# In[4]:

i = -1
# iterate over drug entries to extract information
for drug in obj.drugbank.drug:
    drug_type = str(drug["type"])

    i = i + 1
    # Get drugbank_id
    for id in drug.drugbank_id:
         if str(id["primary"]) == "true":
             df_drugbank_sm.loc[i, "drugbank_id"] = id.cdata
     # Drug name
    df_drugbank_sm.loc[i, "name"] = drug.name.cdata

    # Drug Description
    # Drug CAS
    df_drugbank_sm.loc[i, "cas"] = drug.cas_number.cdata

# In[5]:
df_drugbank_sm.head(10)

# In[6]:

print(df_drugbank_sm.shape)

# In[7]:
# write to csv
df_drugbank_sm.to_csv("drugbank.csv", encoding='utf-8', index=False)
