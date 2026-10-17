import os
import polib

def compile_po_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base_dir, 'locale')

    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith('.po'):
                po_path = os.path.join(root, file)
                mo_path = os.path.join(root, file[:-3] + '.mo')
                try:
                    po = polib.pofile(po_path)
                    po.save_as_mofile(mo_path)
                    print(f"Успешно скомпилирован: {mo_path}")
                except Exception as e:
                    print(f"Ошибка в файле {po_path}: {e}")

if __name__ == '__main__':
    compile_po_files()