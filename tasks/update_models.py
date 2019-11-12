import os
import json
import shutil

import luigi
import poiolib.wikipedia
import pressagio

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRIPT_DIR, "..", "config.json"), "r", encoding="utf-8") as f:
    CONFIG = json.load(f)


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


class CopyCorpusFiles(luigi.Task):
    iso_639_3 = luigi.Parameter()

    def create_corpus_map(self):
        result = {}
        if "files" in CONFIG["languages"][self.iso_639_3]["corpus"]:
            for source_file in CONFIG["languages"][self.iso_639_3]["corpus"]["files"]:
                file_name = os.path.basename(source_file)
                result[source_file] = os.path.join(
                    build_path(self.iso_639_3, "corpus"), file_name
                )
        return result

    def run(self):
        for source_file, target_file in self.create_corpus_map().items():
            target_path = os.path.basename(target_file)
            os.makedirs(target_path)
            shutil.copyfile(source_file, target_file)

    def output(self):
        return [luigi.LocalTarget(fn) for fn in self.create_corpus_map().values()]


class Ngrams(luigi.Task):
    iso_639_3 = luigi.Parameter()
    ngram_size = luigi.IntParameter()

    def requires(self):
        result = CopyCorpusFiles(self.iso_639_3)
        if CONFIG["languages"][self.iso_639_3]["corpus"]["use_wikipedia"] == True:
            result.append(WikipediaCorpus(self.iso_639_3))
        return result

    def corpus_size(self):
        size = 0
        for target in self.input():
            size += os.path.getsize(target.fn)
        return size

    def run(self):
        cutoff = 0
        corpus_size = self.corpus_size()
        if self.ngram_size == 3:
            if corpus_size > 20000:
                cutoff = 1
            elif corpus_size > 2000000:
                cutoff = 2
        if self.ngram_size == 2:
            if corpus_size > 100000:
                cutoff = 1
            elif corpus_size > 10000000:
                cutoff = 2

        files = [target.fn for target in self.input()]
        ngram_map = pressagio.tokenizer.forward_tokenize_files(
            files, self.ngram_size, lowercase=True, cutoff=cutoff
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

        self.output().makedirs()
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
        return [AllNgrams(iso_639_3) for iso_639_3, _ in CONFIG["languages"].items()]

    def output(self):
        return self.input()
