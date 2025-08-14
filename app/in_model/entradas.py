import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import json
import random


USER_AGENTS = [
    # Windows - Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/124.0.0.0 Safari/537.36",
    # MacOS - Chrome / Safari / Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) Gecko/20100101 Firefox/124.0",
    # Linux - Chrome / Firefox
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/124.0",
    # Android - Chrome / Samsung / Opera
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; CPH2273) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; V2027) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    # iPhone / iPad - Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    # Opera Desktop
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/109.0.0.0",
]


class Gsmarena:
    def __init__(self):
        self.phones = []
        self.features = ["Brand", "Model Name", "Model Image"]
        self.url = "https://www.gsmarena.com/"
        self.new_folder_name = "GSMArenaDataset"
        self.absolute_path = os.path.join(os.getcwd(), self.new_folder_name)

    def crawl_html_page(self, sub_url):
        url = self.url + sub_url
        header = {"User-Agent": random.choice(USER_AGENTS)}

        # Pausa para no saturar el servidor
        time.sleep(random.uniform(3, 8))

        try:
            # Intentar hasta 3 veces si falla
            for attempt in range(3):
                try:
                    page = requests.get(url, timeout=None, headers=header)
                    page.raise_for_status()
                    soup = BeautifulSoup(page.text, "html.parser")

                    # Verificar que no sea una página vacía o bloqueada
                    if not soup.find("html") or "Access Denied" in soup.text:
                        print(f"[WARN] Página vacía o bloqueada: {url}")
                        return None

                    return soup

                except requests.exceptions.ReadTimeout:
                    print(f"[TIMEOUT] Intento {attempt + 1}/3 en {url}")
                    time.sleep(5)

            print(f"[ERROR] No se pudo obtener {url} después de 3 intentos.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Fallo al acceder {url}: {e}")
            return None

    def crawl_phone_brands(self):
        phones_brands = []
        soup = self.crawl_html_page("makers.php3")

        # Verificar si se obtuvo algo
        if soup is None:
            print("[ERROR] No se pudo cargar la página de marcas.")
            return []

        # Verificar si hay tablas
        tables = soup.find_all("table")
        if not tables:
            print(f"[WARN] No se encontró ninguna tabla en {self.url + 'makers.php3'}")
            return []

        table = tables[0]
        table_a = table.find_all("a")
        for a in table_a:
            try:
                temp = [
                    a["href"].split("-")[0],
                    a.find("span").text.split(" ")[0],
                    a["href"],
                ]
                phones_brands.append(temp)
            except Exception as e:
                print(f"[WARN] Error procesando marca: {a} → {e}")

        return phones_brands

    def crawl_phones_models(self, phone_brand_link):
        links = []
        nav_link = []
        soup = self.crawl_html_page(phone_brand_link)
        nav_data = soup.find(class_="nav-pages")

        if not nav_data:
            nav_link.append(phone_brand_link)
        else:
            nav_link = nav_data.find_all("a")
            nav_link = [link["href"] for link in nav_link]
            nav_link.append(phone_brand_link)
            nav_link.insert(0, nav_link.pop())

        for link in nav_link:
            soup = self.crawl_html_page(link)
            data = soup.find(class_="section-body")
            if not data:
                continue
            for line1 in data.find_all("a"):
                links.append(line1["href"])

        return links

    def crawl_phones_models_specification(self, link, phone_brand):
        phone_data = {}
        soup = self.crawl_html_page(link)
        model_name = soup.find(class_="specs-phone-name-title").text.strip()
        model_img_html = soup.find(class_="specs-photo-main")
        model_img = model_img_html.find("img")["src"]

        img_folder = os.path.join(self.absolute_path, "images")
        os.makedirs(img_folder, exist_ok=True)

        img_filename = (
            f"{phone_brand}_{model_name.replace('/', '_').replace(' ', '_')}.jpg"
        )
        img_path = os.path.join(img_folder, img_filename)

        try:
            img_data = requests.get(model_img, timeout=10).content
            with open(img_path, "wb") as handler:
                handler.write(img_data)
        except Exception as e:
            print(f"Error descargando imagen {model_name}: {e}")
            img_path = model_img

        phone_data.update({"Brand": phone_brand})
        phone_data.update({"Model Name": model_name})
        phone_data.update({"Model Image": img_path})

        return phone_data

    def create_folder(self):
        if not os.path.exists(self.new_folder_name):
            os.makedirs(self.new_folder_name)
            print(f"Carpeta {self.new_folder_name} creada.")
        else:
            print(f"{self.new_folder_name} directory already exists")

    def check_file_exists(self):
        return os.listdir(self.absolute_path)

    def save_specification_to_file(self):
        phone_brand = self.crawl_phone_brands()
        self.create_folder()
        files_list = self.check_file_exists()
        for brand in phone_brand:
            phones_data = []
            if (brand[0].title() + ".csv") not in files_list:
                link = self.crawl_phones_models(brand[2])
                model_value = 1
                print("Working on", brand[0].title(), "brand.")
                for value in link:
                    datum = self.crawl_phones_models_specification(value, brand[0])
                    phones_data.append(datum)
                    print("Completed ", model_value, "/", len(link))
                    model_value += 1
                with open(
                    os.path.join(self.absolute_path, brand[0].title() + ".csv"),
                    "w",
                    newline="",
                ) as file:
                    dict_writer = csv.DictWriter(file, fieldnames=self.features)
                    dict_writer.writeheader()
                    dict_writer.writerows(phones_data)
                print("Data loaded in the file")
            else:
                print(brand[0].title() + ".csv file already in your directory.")


if __name__ == "__main__":
    try:
        obj = Gsmarena()
        obj.save_specification_to_file()
    except KeyboardInterrupt:
        print("File has been stopped due to KeyBoard Interruption.")
