import pymorphy3
import re

morph = pymorphy3.MorphAnalyzer()

def normalize_text(text: str):
    words = re.findall(r"\w+", text.lower())
    lemmas = []

    for word in words:
        parses = morph.parse(word)
        selected = None
        for p in parses:
            if 'ADJF' in p.tag or 'PRTF' in p.tag:
                selected = p
                break

        if selected:
            lemmas.append(selected.normal_form)
        else:
            lemmas.append(parses[0].normal_form)

    return lemmas