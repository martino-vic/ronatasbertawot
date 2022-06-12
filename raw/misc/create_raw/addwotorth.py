import pandas as pd
import pandas as pd
import re
import epitran

dfin = "wot14.tsv"
dfout = "wot15.tsv"

epi = epitran.Epitran("wot-hunorth")

df = pd.read_csv(dfin, sep="\t")
df = df.rename(columns={"H": "H_orth"})
for i in df.H_orth:
    print(i, ":")
    print(epi.transliterate(i))
df.insert(1, "H", [epi.transliterate(i) for i in df["H_orth"]])
df.to_csv(dfout, sep="\t", encoding="utf-8", index=False)
