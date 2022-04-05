"""cd to folder `misc` and run `python3 -m makescEAH_WOT` from terminal"""

from pathlib import Path
from loanpy import qfysc

def main():
    """creates soundchanges.txt for horizontal or vertical transfers"""

    #define in and out paths
    in_path = Path.cwd().parent.parent / "cldf" / "forms.csv"
    out_path1 = Path.cwd().parent.parent / "etc" / "soundsubstiEAH_WOT"
    out_path2 = Path.cwd().parent.parent / "etc" / "phonotctsubstiEAH_WOT"

    #read in words from forms.csv
    Etym = qfysc.Qfy(dfetymology=(in_path, "WOT", "EAH"), mode="adapt",
                     left="Target_Form", right="Source_Form", vfb=None,
                     ptct_thresh=1)
    #create dict of heuristic sound substitutions based on feature vectors
    Etym.getscdictbase(write=False)
    #extract sound substitutions
    Etym.dfetymology2dict(write=True, outname=out_path1)
    #extract phonotactic changes
    Etym.dfetymology2dict_struc(write=True, outname=out_path2)

if __name__ == "__main__":
    main()
