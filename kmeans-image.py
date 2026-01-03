import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.cluster import KMeans

def get_palette(image_path, clusters=5):
    # 1. Open and downsample for speed (essential for large datasets)
    img = Image.open(image_path)
    img = img.resize((150, 150))
    
    # 2. Convert to RGB and reshape to a list of pixels
    pixels = np.array(img).reshape(-1, 3)
    
    # 3. Apply K-Means clustering
    # n_init='auto' is more efficient for newer sklearn versions
    model = KMeans(n_clusters=clusters, n_init='auto')
    model.fit(pixels)
    
    # 4. Get the cluster centers (the dominant RGB colors)
    colors = model.cluster_centers_.astype(int)
    return colors

def plot_image_with_palette(image_path, palette):
    # Load original image for display
    original_img = Image.open(image_path)
    
    # Create the visualization figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), 
                                   gridspec_kw={'width_ratios': [3, 1]})
    
    # Show the original photo
    ax1.imshow(original_img)
    ax1.set_title("Original Image")
    ax1.axis('off')
    
    # Create a "palette block" - an array of the colors
    # We repeat the palette colors to create a vertical bar
    palette_block = np.zeros((100, 20, 3), dtype=int)
    chunk_size = 100 // len(palette)
    
    for i, color in enumerate(palette):
        palette_block[i*chunk_size : (i+1)*chunk_size, :, :] = color
        
    # Show the palette
    ax2.imshow(palette_block)
    ax2.set_title(f"{len(palette)} Dominant Colors")
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()

# --- Execution ---
# Replace with the path to one of your photos
image_file = r"W:\NELSON\photo-current\2025\2025_06\17-barrels-whitehall\barrels-whitehall-2025-06-17-0780.dng"

try:
    dominant_colors = get_palette(image_file, clusters=6)
    plot_image_with_palette(image_file, dominant_colors)
    
    # Print the hex codes for your design software
    print("Detected Palette (Hex):")
    for rgb in dominant_colors:
        print('#{:02x}{:02x}{:02x}'.format(*rgb))
        
except Exception as e:
    print(f"Error: {e}")