"""cd to folder `misc` and run `python makesc.py` from terminal"""

from pathlib import Path
from loanpy import qfysc

def main():
    """creates othography.tsv with Graphemes 2 IPA mappings"""

    #create orthography.py
    in_path1 = Path.cwd().parent.parent / "cldf" / "forms.csv"
    in_path2 = Path.cwd().parent / "wot.tsv"
    out_path = Path.cwd().parent.parent / "etc" / "sc_vertical.tsv"

    Test = qfysc.Qfy(dfetymology=(in_path1, in_path2, "EAH", "H"), left="Target_Form", right="Source_Form")
    Test.dfetymology2dict(write=True)

if __name__ == "__main__":
    main()
