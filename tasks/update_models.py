import os
import json
import shutil

import luigi
import poiolib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRIPT_DIR, "..", "config.json"), "r", encoding="utf-8") as f:
    CONFIG = json.load(f)


def build_path(iso_639_3, build_type):
    return os.path.join(SCRIPT_DIR, "..", "build", build_type, iso_639_3)


def flatten_corpus_files(luigi_input):
    filenames = []
    for target in luigi_input:
        if isinstance(target, list):
            for target_file in target:
                filenames.append(target_file.fn)
        else:
            filenames.append(target.fn)
    return filenames


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
    task_complete = False
    corpus_map = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corpus_map = self.create_corpus_map()

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
        for source_file, target_file in self.corpus_map.items():
            target_path = os.path.basename(target_file)
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            shutil.copyfile(source_file, target_file)
        if len(self.corpus_map) == 0:
            self.task_complete = True

    def complete(self, *args, **kwargs):
        if len(self.corpus_map) == 0:
            return self.task_complete
        else:
            return super().complete(*args, **kwargs)

    def output(self):
        return [luigi.LocalTarget(fn) for fn in self.create_corpus_map().values()]


class SentenceStartsCapitalMap(luigi.Task):
    iso_639_3 = luigi.Parameter()

    def requires(self):
        result = [CopyCorpusFiles(self.iso_639_3)]
        if CONFIG["languages"][self.iso_639_3]["corpus"]["use_wikipedia"] == True:
            result.append(WikipediaCorpus(self.iso_639_3))
        return result

    def run(self):
        corpus_files = flatten_corpus_files(self.input())
        capitals_map = poiolib.capitals.sentence_starts_capital_map(corpus_files)
        self.output().makedirs()
        with open(self.output().fn, "w", encoding="utf-8") as f:
            json.dump(capitals_map, f, indent=2)

    def output(self):
        return luigi.LocalTarget(
            os.path.join(build_path(self.iso_639_3, "data"), "capitals_map.json")
        )


class Ngrams(luigi.Task):
    iso_639_3 = luigi.Parameter()
    ngram_size = luigi.IntParameter()

    def requires(self):
        result = [
            SentenceStartsCapitalMap(self.iso_639_3),
            CopyCorpusFiles(self.iso_639_3),
        ]
        if CONFIG["languages"][self.iso_639_3]["corpus"]["use_wikipedia"] == True:
            result.append(WikipediaCorpus(self.iso_639_3))
        return result

    def corpus_files(self):
        return flatten_corpus_files(self.input()[1:])

    def corpus_size(self):
        size = 0
        for target in self.corpus_files():
            size += os.path.getsize(target)
        return size

    def run(self):
        cutoff = 0
        corpus_size = self.corpus_size()
        cutoff_map = CONFIG["cutoff_map"][str(self.ngram_size)]
        for entry in cutoff_map:
            if corpus_size > entry[0]:
                cutoff = entry[1]
                break

        ngram_map = poiolib.ngrams.corpus_ngrams(
            self.corpus_files(), self.ngram_size, lowercase=True, cutoff=cutoff
        )
        poiolib.ngrams.ngrams_to_postgres(
            ngram_map, self.ngram_size, self.iso_639_3,
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
