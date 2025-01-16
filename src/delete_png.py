import os
import glob

# Caminho do diretório alvo
directory_path = r"C:\Users\João Faelis\Desktop\IBGE_MORTALIDADE"

# Usamos glob para encontrar todos os arquivos .png no diretório
png_files = glob.glob(os.path.join(directory_path, "*.png"))

# Iteramos sobre cada arquivo encontrado e excluímos
for file_path in png_files:
    try:
        os.remove(file_path)
        print(f"Removido: {file_path}")
    except OSError as e:
        print(f"Erro ao excluir {file_path}: {e}")
