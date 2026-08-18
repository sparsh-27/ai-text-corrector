import importlib.resources
from symspellpy import SymSpell
from textblob import TextBlob

class ClassicalCorrector:
    def __init__(self):
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        try:
            import pkg_resources
            dictionary_path = pkg_resources.resource_filename(
                "symspellpy", "frequency_dictionary_en_82_765.txt"
            )
        except Exception:
            import symspellpy
            dictionary_path = str(importlib.resources.files(symspellpy).joinpath("frequency_dictionary_en_82_765.txt"))
            
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        
    def correct(self, text: str) -> str:
        # First use SymSpell for fast spelling correction of the whole phrase
        suggestions = self.sym_spell.lookup_compound(text, max_edit_distance=2)
        if suggestions:
            spell_corrected = suggestions[0].term
        else:
            spell_corrected = text
            
        try:
            blob = TextBlob(spell_corrected)
            grammar_corrected = str(blob.correct())
            return grammar_corrected
        except Exception:
            return spell_corrected

if __name__ == "__main__":
    corrector = ClassicalCorrector()
    print(corrector.correct("I am writting a leter to you"))
