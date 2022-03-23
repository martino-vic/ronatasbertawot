import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language
from pylexibank import FormSpec

stack = [""]

@attr.s
class CustomLanguage(Language):
    H_orth = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "ronatasbertawot"
    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements= [(" ", "")])

    def cmd_makecldf(self, args):

        #add borrowing table
        args.writer.cldf.add_component(
            "BorrowingTable"
            #{"name": "lol", "datatype": "string"},
        )
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for i, concept in enumerate(self.concepts):
            idx = str(i)+"_"+slug(concept["en"])
            concepts[concept["en"]] = idx
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["en"],
                    Concepticon_ID=concept["Concepticon_ID"],
                    Concepticon_Gloss=concept["Concepticon_Gloss"],
                    )
        args.log.info("added concepts")
        #print(concepts)
        # add language
        languages = args.writer.add_languages()
        args.log.info("added languages")

        # read in data
        data = self.raw_dir.read_csv(
            "wot.tsv", delimiter="\t",
        )
        header = data[0]
        cognates = {}
        cogidx = 1

        for i in range(2, len(data)):
            cognates = dict(zip(header, data[i]))
            concept = data[i][6]
            for language in languages:
                cog = cognates.get(language, "").strip()
                if concept not in cognates:
                    cognates[concept] = cogidx
                    cogidx += 1
                cogid = cognates[concept]
                for lex in args.writer.add_forms_from_value(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=cog,
                        Source="wot",
                        Loan=True,
                        Cognacy=cogid
                        ):
                    args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=cogid,
                            Source="wot"
                            )

                    if lex["Language_ID"] == "EAH":
                        tgtid = lex["ID"]

                    if lex["Language_ID"] == "WOT":
                        if stack[-1] == tgtid:
                            continue
                        stack.pop()
                        stack.append(tgtid)
                        args.writer.objects["BorrowingTable"].append({
                            "ID": lex["Parameter_ID"],
                            "Target_Form_ID": tgtid,
                            "Source_Form_ID": lex["ID"],
                            "Source": lex["Source"]
                            })

        #with self.cldf_writer(args) as writer:


            ##for fidx in ["a", "b", "c"]:
