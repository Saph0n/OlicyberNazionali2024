import random
from PIL import Image
import matplotlib.pyplot as plt
import io
import os

# Funzione per rimuovere il rumore usando il seme specificato
def remove_noise_with_seed(image, seed):
    random.seed(seed)
    clean_image = image.copy()
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x, y))
            p = tuple([(c - random.randint(0, 255)) % 256 for c in p])
            clean_image.putpixel((x, y), p)
    return clean_image

# Funzione ottimizzata per trovare il seme corretto
def find_seed_optimized(image, output_folder, batch_size=16):
    width, height = image.size
    
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for batch_start in range(0, 256, batch_size):
        for seed in range(batch_start, batch_start + batch_size):
            cleaned_image_candidate = remove_noise_with_seed(image, seed)
            
            # Salva l'immagine pulita per ispezione visiva
            cleaned_image_path = os.path.join(output_folder, f'cleaned_image_seed_{seed}.png')
            cleaned_image_candidate.save(cleaned_image_path)
            print(f"Saved image with seed {seed} as {cleaned_image_path}")

    print(f"All images saved in the folder: {output_folder}")
    return None

# Carica l'immagine rumorosa dal file binario
output_bin_path = r"C:\Users\berto\Downloads\output.bin"  # Usa una stringa raw per il percorso del file
with open(output_bin_path, 'rb') as file:
    output_bin_content = file.read()
noisy_image = Image.open(io.BytesIO(output_bin_content))

# Esegui la funzione ottimizzata per trovare il seme corretto
output_folder = r"C:\Users\berto\Downloads\cleaned_images"  # Specifica la cartella di output
find_seed_optimized(noisy_image, output_folder)
