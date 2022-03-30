"""cd to folder `misc` and run `python makesc.py` from terminal"""

from pathlib import Path
from loanpy import qfysc

def main():
    """creates soundchanges.txt for horizontal or vertical transfers"""

    #define in and out paths
    in_path1 = Path.cwd().parent.parent / "cldf" / "forms.csv"
    in_path2 = Path.cwd().parent / "wot.tsv"
    out_path = Path.cwd().parent.parent / "etc" / "soundchanges"

    #run qfysc module from loanpy
    Etym = qfysc.Qfy(dfetymology=(in_path1, in_path2, "EAH", "H"),
                     left="Target_Form", right="Source_Form", vfb=None)
    Etym.dfetymology2dict(write=True, outname=out_path)

if __name__ == "__main__":
    main()
