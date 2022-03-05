"""cd to folder `etc` and run `python makeconcepts.py` from terminal"""

from pathlib import Path
import re

import pandas as pd
from pysem.glosses import to_concepticon

in_path = Path.cwd().parent / "wot.tsv"
out_path = Path.cwd().parent.parent / "etc" / "concepts.tsv"


def gg(d):
    """dict vals to tuples (ID, Gloss) or ("", "")"""
    return {k: (d[k][0][0], d[k][0][1]) if d[k] else ("", "") for k in d}


def main():
    """"
    read wot.tsv,
    link data to concepticon,
    write concepts.tsv
    """
    # read file and clean column "sense"
    dfgot = pd.read_csv(in_path, sep="\t", usecols=["en"])

    # define list of dictionaries and plug into to_concepticon()
    glo = [{"gloss": e} for e in dfgot.en]
    G = gg(to_concepticon(glo, language="en", max_matches=1))

    # map dictionary to new columns
    newcols = ["Concepticon_ID", "Concepticon_Gloss"]
    dfgot[newcols] = dfgot['en'].map(G).tolist()
    dfgot.to_csv(out_path, index=False, encoding="utf-8", sep="\t")


if __name__ == "__main__":
    main()
