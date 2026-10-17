import os
import re
import polib

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LANGUAGES = ['uz', 'ru', 'en']


def extract_trans_strings():
    strings = set()
    pattern = re.compile(r'\{%\s*trans\s+["\'](.*?)["\']\s*%\}')

    for root, _, files in os.walk(PROJECT_DIR):
        if '.venv' in root or 'locale' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    for match in matches:
                        strings.add(match)
    return sorted(list(strings))


def update_po_files():
    found_strings = extract_trans_strings()
    print(f"Найдено уникальных фраз в HTML: {len(found_strings)}")

    for lang in LANGUAGES:
        po_folder = os.path.join(PROJECT_DIR, 'locale', lang, 'LC_MESSAGES')
        os.makedirs(po_folder, exist_ok=True)
        po_file_path = os.path.join(po_folder, 'django.po')

        if os.path.exists(po_file_path):
            po = polib.pofile(po_file_path)
        else:
            po = polib.POFile()
            po.metadata = {
                'Project-Id-Version': '1.0',
                'Report-Msgid-Bugs-To': '',
                'POT-Creation-Date': '2026-10-08 15:00+0000',
                'PO-Revision-Date': '2026-10-08 15:00+0000',
                'Last-Translator': 'FULL NAME <EMAIL@ADDRESS>',
                'Language-Team': f'{lang} <{lang}@li.org>',
                'Language': lang,
                'MIME-Version': '1.0',
                'Content-Type': 'text/plain; charset=UTF-8',
                'Content-Transfer-Encoding': '8bit',
            }

        existing_msgids = {entry.msgid for entry in po}
        added_count = 0

        for text in found_strings:
            if text not in existing_msgids:
                entry = polib.POEntry(
                    msgid=text,
                    msgstr=""
                )
                po.append(entry)
                added_count += 1

        po.save(po_file_path)
        print(f"[{lang.upper()}] Обновлён {po_file_path} (добавлено новых фраз: {added_count})")


if __name__ == '__main__':
    update_po_files()