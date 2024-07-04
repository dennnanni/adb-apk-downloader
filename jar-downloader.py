import os
import requests

def download_jars(urls, download_folder):
    # Crea la cartella di download se non esiste
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Scarica i file jar
    for url in urls:
        file_name = url.split('/')[-1]
        file_path = os.path.join(download_folder, file_name)
        print(f"Downloading {file_name}...")
        try:
            response = requests.get(url)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"{file_name} downloaded successfully!")
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")

# Lista di URL dei file jar da scaricare
urls = []

for i in range(1, 2, 1):
    for j in range(6, 7, 1):
        urls.append("https://repo1.maven.org/maven2/io/ktor/ktor-client-core-jvm/" + str(i) + "." + str(j) + ".0/ktor-client-core-jvm-" + str(i) + "." + str(j) + ".0.jar")
        
#https://repo1.maven.org/maven2/io/ktor/ktor-client-core-jvm/2." + str(i) + ".0/ktor-client-core-jvm-2." + str(i) + ".0.jar

# Cartella di download
download_folder = "C:\\Users\\denno\\Downloads\\libsjar"

# Chiamata alla funzione per scaricare i file jar
download_jars(urls, download_folder)
