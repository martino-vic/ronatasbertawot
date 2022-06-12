import pandas as pd
import re

dfin = "wot11.tsv"
dfout = "wot12.tsv"

def cln(w):
    w = w.strip()
    w = re.split("\|", w)[0]
    w = re.sub("\[[^\]]*?]", "", w)
    return w.strip()

df = pd.read_csv(dfin, sep="\t")
df["en"] = [cln(i) if not isinstance(i, float) else i for i in df["en"]]
df.to_csv(dfout, sep="\t", encoding="utf-8", index=False)
