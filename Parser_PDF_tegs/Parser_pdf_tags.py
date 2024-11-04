import fitz  # Импортируем PyMuPDF
import os
from datetime import datetime  # Для создания временной отметки


def parse_pdf_for_unique_words(file_path, tags):
    """Парсит PDF-файл и возвращает уникальные слова с тегами."""
    pdf_document = fitz.open(file_path)
    words_with_tags = set()  # Множество для хранения уникальных слов с тегами

    # Проходим по каждой странице PDF-документа
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        page_text = page.get_text()  # Получаем текст страницы

        # Проверяем наличие тегов на странице и сохраняем слова, содержащие теги
        for tag in tags:
            if tag in page_text:
                # Разбиваем текст на слова и проверяем наличие тега в каждом слове
                words = page_text.split()
                for word in words:
                    if tag in word:
                        words_with_tags.add(word)  # Добавляем слово с тегом в множество

    pdf_document.close()  # Закрываем PDF-документ
    return words_with_tags


def compare_pdfs_by_tags(file_path1, file_path2, tags, output_dir):
    """Сравнивает два PDF по тегам и сохраняет уникальные слова с тегами."""
    # Парсим каждый PDF и получаем уникальные слова с тегами
    words_with_tags_pdf1 = parse_pdf_for_unique_words(file_path1, tags)
    words_with_tags_pdf2 = parse_pdf_for_unique_words(file_path2, tags)

    # Определяем общие слова с тегами, присутствующие в обоих документах
    common_words = words_with_tags_pdf1 & words_with_tags_pdf2

    # Определяем уникальные слова, исключая общие
    unique_words_pdf1 = words_with_tags_pdf1 - common_words
    unique_words_pdf2 = words_with_tags_pdf2 - common_words

    # Создаем временную отметку для имени файла
    timestamp = datetime.now().strftime("%Y%m%d_H%H_M%M_S%S")
    output_file = os.path.join(output_dir, f"comparison_result_{timestamp}.txt")

    # Убедимся, что директория для сохранения файла существует
    os.makedirs(output_dir, exist_ok=True)

    # Сохраняем результат в файл
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Уникальные теги в первом PDF:\n")
        for word in sorted(unique_words_pdf1):
            file.write(f"{word}\n")

        file.write("\n" + "=" * 40 + "\n\n")

        file.write("Уникальные теги во втором PDF:\n")
        for word in sorted(unique_words_pdf2):
            file.write(f"{word}\n")

    print(f"Сравнение тегов завершено. Результаты сохранены в файл: {output_file}")


# Пример использования
file_path1 = r"e:\Объекты\Михайловский перевал\РД\01-23-Р-ССОИ\PDF\01-23-Р-ССОИ_без_СО.pdf"
file_path2 = r"e:\Объекты\Михайловский перевал\РД\01-23-Р-ССОИ\PDF\01-23-Р-ССОИ.pdf"
tags = ["UPS", "ШОП", "SW"]  # Замените на нужные вам теги
output_dir = r"e:\Объекты\Результаты"  # Укажите директорию для сохранения файла

# Сравниваем PDF по тегам
compare_pdfs_by_tags(file_path1, file_path2, tags, output_dir)
