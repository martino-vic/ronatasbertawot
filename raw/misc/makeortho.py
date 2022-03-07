"""cd to folder `misc` and run `python makeortho.py` from terminal"""

from pathlib import Path
import re

import epitran
import pandas as pd
from ipatok import tokenise

# have 2 diff transcription files for Hungarian vs Pre-Hungarians
epi = epitran.Epitran("hun-Latn").transliterate
def segment(w): return ' '.join(tokenise(epi(w)))

def main():
    """creates othography.tsv with Graphemes 2 IPA mappings"""

    #create orthography.py
    in_path = Path.cwd().parent.parent / "cldf" / "forms.csv"
    out_path = Path.cwd().parent.parent / "etc" / "orthography.tsv"
    pd.read_csv(in_path, usecols=["Form", "Language_ID"])\
      .assign(IPA=lambda x: list(map(segment, x.Form)))\
      .rename(columns={"Form": "Grapheme"})\
      .drop_duplicates()\
      .to_csv(out_path, index=False, encoding="utf-8", sep="\t")

if __name__ == "__main__":
    main()
