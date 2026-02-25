import pdfplumber
import unicodedata
import re

INPUT_FILE = "orfoepicheskij_slovar.pdf"
OUTPUT_FILE = "orfoepicheskij_slovar.txt"

# В данном словаре словарная часть начинается после разделов с описанием и алфавитом.
# Проверьте PDF, с какой страницы начинаются слова на букву "А".
START_PAGE = 11


def remove_stress(text):
    text = unicodedata.normalize("NFD", text)
    # удаляем знак ударения (U+0301)
    text = text.replace("\u0301", "")
    return unicodedata.normalize("NFC", text)


def is_valid_headword(word):
    # Только русские заглавные буквы и дефис
    # В данном словаре заголовки пишутся ВСЕМИ ЗАГЛАВНЫМИ
    if not re.fullmatch(r"[А-ЯЁ\-]+", word):
        return False
    if len(word) < 2:
        return False
    return True


words = []

with pdfplumber.open(INPUT_FILE) as pdf:
    # Проверка на случай, если страниц меньше, чем START_PAGE
    actual_start = min(START_PAGE, len(pdf.pages))

    for page in pdf.pages[actual_start:]:
        word_objects = page.extract_words(
            use_text_flow=True,
            keep_blank_chars=False
        )

        for w in word_objects:
            raw_text = w["text"]

            # Очищаем от ударений для проверки
            clean_text = remove_stress(raw_text)

            # Ключевой момент: в этом словаре заголовочные слова - ЗАГЛАВНЫЕ
            # Если слово не полностью заглавное, пропускаем его (это формы слова или пояснения)
            if not clean_text.isupper():
                continue

            # Удаляем цифры в конце слов (индексы омонимов: АДРЕС1 -> АДРЕС)
            clean_text = re.sub(r"\d+$", "", clean_text)

            # Удаляем возможные "мусорные" символы (на случай, если isupper пропустил что-то странное)
            clean_text = re.sub(r"[^А-ЯЁ\-]", "", clean_text)

            if is_valid_headword(clean_text):
                words.append(clean_text)

unique_words = sorted(set(words))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for w in unique_words:
        f.write(w + "\n")

print("Найдено слов:", len(unique_words))