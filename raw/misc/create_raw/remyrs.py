import pandas as pd
import re

dfin = "wot12.tsv"
dfout = "wot13.tsv"

def cln(w):
    return re.sub(" ?\(c?\d\d\d\d\)", "", w)

df = pd.read_csv(dfin, sep="\t")
df["en"] = [cln(i) if not isinstance(i, float) else i for i in df["en"]]
df.to_csv(dfout, sep="\t", encoding="utf-8", index=False)
