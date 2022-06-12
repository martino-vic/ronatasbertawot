import pandas as pd
import re

recip = []
donor = []
en = []

lgs = "WOT|Cum|South Sl[^←]*← WOT|\? WOT|\? Cum|WOT or Cum|\(WOT"
#NOT: ← WOT *tir, ← WOT *sön-, ← WOT *tatraŋ
lgs = "|".join(["← ?" + i for i in lgs.split("|")])
#print(lgs)
wot = re.split(lgs, open("wot.txt").read().replace("\n", ""))
dfout = pd.DataFrame()


# grab recipient words:
for w in wot[:-1]:
    try: recip.append(w.rsplit("|", 1)[1])
    except IndexError: recip.append(None)

# grab donor words:
for w in wot[1:]:
    try: donor.append(w.split("|", 1)[0])
    except IndexError: donor.append(None)

# grab English translations
for r, w in zip(recip, wot[:-1]):
    try:
        # grab headword from previos search and clean it
        t = re.split("[ ,]", r.strip().replace("-", ""), 1)[0]
        # search for the same headword in the beginning of the article
        t = str(re.search(fr"\[{t}\][^‘]*?\‘.*\’", w).group())
        # grab text between ’’ (= English translation)
        t = t.split("‘")[1].replace("’", "").strip()
        en.append(t)
    except AttributeError:
        en.append(None)

dfout["recip"], dfout["donor"], dfout["en"] = recip, donor, en

# split col recip into different proto lg stages
#print(min([len(i.split("<")) for i in recip]))

dfout.to_csv("wot.tsv", sep="\t", encoding="utf-8", index=False)
