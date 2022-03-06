import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language
from pylexibank import FormSpec

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "ronatasbertawot"
    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements= [(" ", "")])

    def cmd_makecldf(self, args):
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

        for i in range(2, len(data), 2):
            words = dict(zip(header, data[i]))
            cognates = dict(zip(header, data[i+1]))
            concept = data[i][5]
            for language in languages:
                entry = words.get(language).strip()
                cog = cognates.get(language).strip()
                if concept not in cognates:
                    cognates[concept] = cogidx
                    cogidx += 1
                cogid = cognates[concept]
                for lex in args.writer.add_forms_from_value(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=entry,
                        Source="wot",
                        Loan=True,
                        Cognacy=cogid
                        ):
                    args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=cogid,
                            Source="wot"
                            )
