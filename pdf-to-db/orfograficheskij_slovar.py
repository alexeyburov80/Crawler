import pdfplumber
import unicodedata
import re

INPUT_FILE = "orfograficheskij_slovar.pdf"
OUTPUT_FILE = "orfograficheskij_slovar.txt"
START_PAGE = 8
def remove_stress(text):
    text = unicodedata.normalize("NFD", text)
    # удаляем только знак ударения (U+0301)
    text = text.replace("\u0301", "")
    return unicodedata.normalize("NFC", text)

def is_valid_word(word):
    # только русские буквы и дефис
    if not re.fullmatch(r"[А-Яа-яЁё\-]+", word):
        return False
    # исключаем служебные короткие формы
    if len(word) < 2:
        return False
    return True

words = []

with pdfplumber.open(INPUT_FILE) as pdf:
    for page in pdf.pages[START_PAGE:]:
        word_objects = page.extract_words(
            use_text_flow=True,
            keep_blank_chars=False
        )

        for w in word_objects:
            text = remove_stress(w["text"])

            # слово должно начинаться с буквы
            if not text or not text[0].isalpha():
                continue

            # важно: в словаре заголовочные слова стоят ближе к левому краю
            # подберите порог если нужно
            if w["x0"] < 240:   # <-- ключевой момент
                text = re.sub(r"[^А-Яа-яЁё\-]", "", text)

                if is_valid_word(text):
                    words.append(text)

unique_words = sorted(set(words))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for w in unique_words:
        f.write(w + "\n")

print("Найдено слов:", len(unique_words))