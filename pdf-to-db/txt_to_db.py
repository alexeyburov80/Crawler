import sqlite3
import os
import glob

# --- НАСТРОЙКИ ---
DB_NAME = "../dictionary-check/app/data/database.db"  # Имя файла базы данных
TXT_FOLDER = "."  # Папка с txt файлами ("." - текущая папка)
TABLE_NAME = "dictionary" # Имя таблицы


# -----------------

def init_db(conn):
    """Создаем таблицу и индекс"""
    cursor = conn.cursor()

    # Создаем таблицу.
    # UNIQUE автоматически создает индекс для быстрого поиска
    # и гарантирует отсутствие дублей.
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE
        )
    ''')

    # Дополнительный индекс для ускорения поиска по шаблону (например, LIKE 'Абб%')
    # Если нужно искать просто точное совпадение, UNIQUE выше уже справляется.
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_word ON {TABLE_NAME}(word)")

    conn.commit()
    print(f"База данных '{DB_NAME}' инициализирована.")


def import_files(conn, folder_path):
    cursor = conn.cursor()

    # Ищем все txt файлы в папке
    files = glob.glob(os.path.join(folder_path, "*.txt"))

    if not files:
        print("Не найдено .txt файлов в указанной папке.")
        return

    total_added = 0

    for file_path in files:
        print(f"Обработка файла: {os.path.basename(file_path)} ...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Читаем файл построчно
                for line in f:
                    word = line.strip()  # Удаляем пробелы и переносы строк

                    if word:  # Если строка не пустая
                        try:
                            # INSERT OR IGNORE попытается добавить слово.
                            # Если оно уже есть (нарушение UNIQUE), оно просто пропустится без ошибки.
                            cursor.execute(f"INSERT OR IGNORE INTO {TABLE_NAME} (word) VALUES (?)", (word,))

                            if cursor.rowcount > 0:
                                total_added += 1

                        except sqlite3.Error as e:
                            print(f"Ошибка при вставке слова '{word}': {e}")

            conn.commit()  # Фиксируем изменения после каждого файла

        except UnicodeDecodeError:
            print(f"Ошибка кодировки в файле {file_path}. Попробуйте открыть как 'cp1251'")
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")

    print(f"\nГотово! Добавлено новых слов: {total_added}")

def main():
    # Подключение к БД
    conn = sqlite3.connect(DB_NAME)

    try:
        init_db(conn)
        import_files(conn, TXT_FOLDER)
       # search_test(conn)
    finally:
        conn.close()
        print("\nСоединение с БД закрыто.")


if __name__ == "__main__":
    main()