import pdfplumber
import unicodedata
import re

INPUT_FILE = "slovar_inostr_slov.pdf"
OUTPUT_FILE = "slovar_inostr_slov.txt"

def remove_stress(text):
    decomposed = unicodedata.normalize("NFD", text)

    result = []
    for ch in decomposed:
        # удаляем ТОЛЬКО знак ударения (acute accent)
        if ch == "\u0301":
            continue
        result.append(ch)

    return unicodedata.normalize("NFC", "".join(result))


def is_valid_word(word):
    return bool(re.fullmatch(r"[А-ЯЁ\-]+", word)) and len(word) >= 2


words = []

with pdfplumber.open(INPUT_FILE) as pdf:
    for page in pdf.pages:
        # получаем все объекты слов
        word_objects = page.extract_words(use_text_flow=True, keep_blank_chars=False)

        # фильтруем только левый край (например, x0 < 240)
        left_words = [w for w in word_objects if w["x0"] < 240]

        # группируем по линии (по координате top, с допуском ±2)
        lines = {}
        for w in left_words:
            line_key = round(w["top"] / 2)  # делим на 2 чтобы уменьшить шум
            lines.setdefault(line_key, []).append(w)

        for line_words in lines.values():
            # сортируем слова слева направо
            line_words.sort(key=lambda x: x["x0"])
            # склеиваем в одно слово
            full_text = "".join(w["text"] for w in line_words)
            # убираем ударения
            full_text = remove_stress(full_text)
            # убираем цифры в конце
            full_text = re.sub(r"\d+", "", full_text)
            # оставляем только кириллицу и дефис
            full_text = re.sub(r"[^А-ЯЁ\-]", "", full_text)
            if is_valid_word(full_text):
                words.append(full_text)

unique_words = sorted(set(words))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for w in unique_words:
        f.write(w + "\n")

print("Найдено слов:", len(unique_words))