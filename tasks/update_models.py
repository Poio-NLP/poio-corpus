import os
import json

import luigi
import poiolib.wikipedia
import pressagio

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def build_path(iso_639_3, build_type):
    return os.path.join(SCRIPT_DIR, "..", "build", build_type, iso_639_3)


class WikipediaCorpus(luigi.Task):
    iso_639_3 = luigi.Parameter()

    def run(self):
        self.output().makedirs()
        poiolib.wikipedia.extract_to_txt(self.iso_639_3, self.output().fn)

    def output(self):
        return luigi.LocalTarget(
            os.path.join(build_path(self.iso_639_3, "corpus"), "wikipedia.txt")
        )


class Ngrams(luigi.Task):
    iso_639_3 = luigi.Parameter()
    ngram_size = luigi.IntParameter()

    def requires(self):
        return WikipediaCorpus(self.iso_639_3)

    def run(self):
        text_file = self.input().fn
        cutoff = 0
        file_size = os.path.getsize(text_file)
        if self.ngram_size == 3:
            if file_size > 20000:
                cutoff = 1
            elif file_size > 2000000:
                cutoff = 2
        if self.ngram_size == 2:
            if file_size > 100000:
                cutoff = 1
            elif file_size > 10000000:
                cutoff = 2

        self.output().makedirs()
        ngram_map = pressagio.tokenizer.forward_tokenize_file(
            text_file, self.ngram_size, lowercase=True, cutoff=cutoff
        )

        pressagio.dbconnector.insert_ngram_map_postgres(
            ngram_map,
            self.ngram_size,
            self.iso_639_3,
            append=False,
            create_index=True,
            lowercase=True,
            normalize=True,
        )

        try:
            with open(self.output().fn, "w", encoding="utf-8") as f:
                for ngram, count in ngram_map.items():
                    f.write("{}\t{}\n".format("\t".join(ngram), count))
        except Exception:
            os.remove(self.output().fn)

    def output(self):
        return luigi.LocalTarget(
            os.path.join(
                build_path(self.iso_639_3, "ngrams"),
                "{}gram.txt".format(self.ngram_size),
            )
        )


class AllNgrams(luigi.Task):
    iso_639_3 = luigi.Parameter()

    def requires(self):
        return [Ngrams(self.iso_639_3, ngram_size) for ngram_size in [1, 2, 3]]

    def output(self):
        return self.input()


class AllLanguages(luigi.Task):
    def requires(self):
        with open(
            os.path.join(SCRIPT_DIR, "..", "config.json"), "r", encoding="utf-8"
        ) as f:
            config = json.load(f)

        return [
            AllNgrams(iso_639_3)
            for iso_639_3, lang_config in config["languages"].items()
            if lang_config["corpus"]["use_wikipedia"] == True
        ]

    def output(self):
        return self.input()
