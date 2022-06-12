import pandas as pd
import re

dfin = "wot10.tsv"
dfout = "wot11.tsv"

df = pd.read_csv(dfin, sep="\t")
df["donor"] = [re.split("[/~,]| or ", i) if not isinstance(i, float) else i for i in df["donor"]]
df = df.explode("donor")
df["donor"] = [i.strip() for i in df["donor"]]
df.to_csv(dfout, sep="\t", encoding="utf-8", index=False)
