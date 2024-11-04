import fitz  # Импортируем PyMuPDF
import os
from datetime import datetime


def parse_pdf_for_unique_words(file_path, tags):
    """Парсит PDF-файл и возвращает уникальные слова с тегами и номера страниц."""
    pdf_document = fitz.open(file_path)
    words_with_tags = {}  # Словарь для хранения уникальных слов с тегами и номеров страниц

    # Проходим по каждой странице PDF-документа
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        page_text = page.get_text("text")  # Получаем текст страницы

        # Проверяем наличие тегов на странице и сохраняем слова, содержащие теги
        for tag in tags:
            if tag in page_text:
                # Разбиваем текст на слова и проверяем наличие тега в каждом слове
                words = page_text.split()
                for word in words:
                    if tag in word:
                        if word not in words_with_tags:
                            words_with_tags[word] = set()  # Используем множество для номеров страниц
                        words_with_tags[word].add(page_num + 1)  # Добавляем номер страницы

    pdf_document.close()  # Закрываем PDF-документ
    return words_with_tags


def highlight_words_in_pdf(file_path, words_with_tags, output_path):
    """Выделяет слова с тегами на страницах PDF-файла и сохраняет его под новым именем."""
    pdf_document = fitz.open(file_path)

    # Проходим по каждой странице и выделяем уникальные теги
    for word, pages in words_with_tags.items():
        for page_num in pages:
            page = pdf_document[page_num - 1]  # Индексация страниц начинается с 0
            text_instances = page.search_for(word)  # Ищем все вхождения слова на странице

            # Добавляем выделение для каждого вхождения
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 0, 0))  # Устанавливаем красный цвет выделения
                highlight.update()

    # Сохраняем новый файл с выделениями
    pdf_document.save(output_path, garbage=4, deflate=True)
    pdf_document.close()


def compare_pdfs_and_highlight(file_path1, file_path2, tags, output_dir):
    """Сравнивает два PDF по тегам, сохраняет уникальные слова с тегами и номера страниц в PDF и TXT."""
    # Создаем папку с уникальным именем для текущего запуска
    timestamp = datetime.now().strftime("%Y%m%d_H%H_M%M_S%S")
    result_folder = os.path.join(output_dir, f"output_{timestamp}")
    os.makedirs(result_folder, exist_ok=True)

    # Парсим каждый PDF и получаем уникальные слова с тегами и номера страниц
    words_with_tags_pdf1 = parse_pdf_for_unique_words(file_path1, tags)
    words_with_tags_pdf2 = parse_pdf_for_unique_words(file_path2, tags)

    # Определяем общие слова с тегами, присутствующие в обоих документах
    common_words = set(words_with_tags_pdf1.keys()) & set(words_with_tags_pdf2.keys())

    # Определяем уникальные слова, исключая общие
    unique_words_pdf1 = {word: pages for word, pages in words_with_tags_pdf1.items() if word not in common_words}
    unique_words_pdf2 = {word: pages for word, pages in words_with_tags_pdf2.items() if word not in common_words}

    # Создаем файлы с уникальными названиями
    output_file_pdf1 = os.path.join(result_folder, f"highlighted_unique_pdf1_{timestamp}.pdf")
    output_file_pdf2 = os.path.join(result_folder, f"highlighted_unique_pdf2_{timestamp}.pdf")
    output_file_txt = os.path.join(result_folder, f"comparison_result_{timestamp}.txt")

    # Сохраняем файлы с выделенными уникальными тегами
    highlight_words_in_pdf(file_path1, unique_words_pdf1, output_file_pdf1)
    highlight_words_in_pdf(file_path2, unique_words_pdf2, output_file_pdf2)

    # Записываем результаты в текстовый файл
    with open(output_file_txt, "w", encoding="utf-8") as file:
        file.write("Уникальные теги в первом PDF:\n")
        for word, pages in sorted(unique_words_pdf1.items()):
            file.write(f"{word} (Страницы: {', '.join(map(str, sorted(pages)))})\n")

        file.write("\n" + "=" * 40 + "\n\n")

        file.write("Уникальные теги во втором PDF:\n")
        for word, pages in sorted(unique_words_pdf2.items()):
            file.write(f"{word} (Страницы: {', '.join(map(str, sorted(pages)))})\n")

    print(f"Сравнение тегов завершено. Результаты сохранены в директории:\n{result_folder}")


# Пример использования
file_path1 = r"e:\Объекты\Михайловский перевал\РД\01-23-Р-ССОИ\PDF\01-23-Р-ССОИ_без_СО.pdf"
file_path2 = r"e:\Объекты\Михайловский перевал\РД\01-23-Р-ССОИ\PDF\01-23-Р-ССОИ.pdf"
tags = ["UPS", "ШОП", "SW"]  # Замените на нужные вам теги
output_dir = r"e:\Объекты\Результаты"  # Укажите директорию для сохранения файла

# Сравниваем PDF по тегам, выделяем уникальные теги и сохраняем в PDF и TXT
compare_pdfs_and_highlight(file_path1, file_path2, tags, output_dir)
