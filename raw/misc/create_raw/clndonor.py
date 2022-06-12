import pandas as pd
import re

dfin = "wot9.tsv"
dfout = "wot10.tsv"

def cln(w):
    w = w.strip()
    for i in "-*?()":
        w = w.replace(i,"")
        w = re.sub("\{[^\}]*?}", "", w)
        w = re.sub("\‘[^\’]*?’", "", w)
        w = re.sub("etc.", "", w)
        w = re.split("[><←→]", w)[0]

    return w.strip()

df = pd.read_csv(dfin, sep="\t")
df["donor"] = [cln(i) for i in df["donor"]]
df.to_csv(dfout, sep="\t", encoding="utf-8", index=False)
