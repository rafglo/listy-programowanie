import zipfile, os, datetime, time
from pathlib import Path

def copy_mod(folders, out_path, extension, mod_time = 3, mod_format = "d"):
    """
    Function - copy_mod
    Funkcja tworząca kopię bezpieczeństwa plików o danych rozszerzeniach, z danych folderów, modyfikowanych w danym przez użytkownika czasie
    (funkcja zapisuje plik zip w katalogu Backup, który zostanie utworzony automatycznie jeśli nie istnieje).

    Input:
    folders(list) - lista folderów, w których znajdują się pliki do kopii
    out_path(str) - ścieżka do katalogu Backup
    extension(str) - rozszerzenie plików, których kopię chcemy zrobić
    mod_time(int) - liczba (sekund/godzin/dni/tygodni/lat) określająca przedział czasu, w którym pliki, których kopię chcemy zrobić zostały zmodyfikowane
    mod_format(str) - jednostka czasu dla mod_time: "s" - sekundy, "m" - minuty, "h" - godziny, "d" - dni, "w" - tygodnie, "y" - lata

    """
    mod_formats = ["s", "m", "h", "d", "w", "y"]
    mod_index = mod_formats.index(mod_format)
    mod_div = [1, 60, 3600, 3600*24, 3600*24*7, 3600*24*365]
    date = str(datetime.date.today())
    zip_name = "copy - " + date + ".zip"
    if_exists = os.path.exists(out_path + "\\Backup")
    if if_exists:
        names = []
        for root, dirs, files in os.walk(out_path + "\\Backup"):
            for file in files:
                names.append(os.path.basename(os.path.join(root, file))[1:])
        how_much = names.count(zip_name)
        if how_much > 0:
            zip_name = str(how_much + 1) + "copy - " + date + ".zip"
        else:
            zip_name = "1" + "copy - " + date + ".zip"
        zip_path = out_path + "\\Backup\\" + zip_name
    else:
        backup_path = out_path + "\\Backup\\"
        os.mkdir(backup_path)
        zip_path = backup_path + "\\" + zip_name

    with zipfile.ZipFile(zip_path, "w") as zf:
        for folder in folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    mod = os.path.getmtime(os.path.join(root, file))
                    delta = (time.time() - mod) / mod_div[mod_index]
                    if Path(file).suffix == extension and delta < mod_time:
                        zf.write(os.path.join(root, file))
    zf.close()


copy_mod([r"C:\Users\Rafal\OneDrive\Pulpit\goegrafia", r"C:\Users\Rafal\OneDrive\Pulpit\informatyka"], r"C:\Users\Rafal\OneDrive\Pulpit", ".txt", 3, "w")
