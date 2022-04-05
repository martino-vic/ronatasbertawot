"""cd to folder `misc` and run `python makescH_EAH.py` from terminal"""

from pathlib import Path
from loanpy import qfysc

def main():
    """creates soundchanges.txt for horizontal or vertical transfers"""

    #define in and out paths
    in_path = Path.cwd().parent.parent / "cldf" / "forms.csv"
    out_path = Path.cwd().parent.parent / "etc" / "soundchangesH_EAH"

    #run qfysc module from loanpy
    Etym = qfysc.Qfy(dfetymology=(in_path, "EAH", "H"),
                     left="Target_Form", right="Source_Form", vfb=None)
    Etym.dfetymology2dict(write=True, outname=out_path)

if __name__ == "__main__":
    main()
