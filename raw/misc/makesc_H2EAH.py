"""cd to folder `misc` and run `python3.9 -m makescH2EAH` from terminal"""

from pathlib import Path
from loanpy import qfysc

def main():
    """creates soundchanges.txt for horizontal or vertical transfers"""

    #define in and out paths
    in_path = Path.cwd().parent.parent / "cldf" / "forms.csv"
    out_path = Path.cwd().parent.parent / "etc" / "sc_H2EAH.txt"

    #read in words from forms.csv
    Etym = qfysc.Etym(
            forms_csv=in_path,
            source_language="H",
            target_language="EAH",
            adapting=False
            )

    #extract sound substitutions
    Etym.get_sound_corresp(write_to=out_path)

if __name__ == "__main__":
    main()
