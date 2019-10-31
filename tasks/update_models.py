import os

import luigi
import poiolib.wikipedia

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def corpus_path(iso_639_3):
    return os.path.join(SCRIPT_DIR, "..", "build", "corpus", "wikipedia", iso_639_3)


class WikipediaCorpusTask(luigi.Task):
    iso_639_3 = luigi.Parameter()

    def run(self):
        self.output().makedirs()
        poiolib.wikipedia.extract_to_txt(self.iso_639_3, self.output().fn)

    def output(self):
        return luigi.LocalTarget(
            os.path.join(corpus_path(self.iso_639_3), "{}.txt".format(self.iso_639_3))
        )
