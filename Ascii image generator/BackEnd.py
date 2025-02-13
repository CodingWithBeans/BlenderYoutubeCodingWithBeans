import os
from PIL import Image
import cv2
import numpy as np



ascii_characters_by_density = [
    " ", ".", ",", ":", ";", "i", "!", "|", "1", "t", "f", "L", "I", "(", ")", "[", "]", "{", "}", "r", "c",
    "*", "+", "=", "7", "?", "v", "x", "J", "3", "n", "o", "s", "z", "5", "2", "S", "F", "C", "Z", "U", "O",
    "0", "Q", "8", "9", "V", "Y", "X", "G", "q", "m", "w", "p", "d", "A", "D", "H", "#", "M", "B", "&", "W",
    "E", "%", "6", "k", "R", "P", "N", "T", "4", "K", "E", "U", "h", "y", "b", "g", "j", "@", "^", "a", "u",
    "e", "l", "I", "T", "q", "H", "D", "W", "M", "B", "Q", "G", "N", "O", "Z", "S", "C", "V", "X", "Y", "K",
    "A", "0", "9", "8", "Q", "O", "Z", "C", "V", "S", "X", "Y", "N", "K", "M", "G", "B", "W", "H", "D", "Q",
    "E", "U", "T", "l", "y", "u", "a", "^", "@", "j", "g", "b", "y", "h", ".", "K", "4", "T", "N", "P", "R",
    "k", "6", "%", "E", "W", "B", "M", "#"
]

def get_ascii_art(Image_path, block_size, line_detection):
    try:
        if line_detection:
            image = cv2.imread(Image_path)
            img = edge_detection(image)
            img = Image.fromarray(img)
        else:
            img = Image.open(Image_path)

        img = img.convert("L")

        width, height = img.size
        new_width = width // block_size
        new_height = height // block_size

        img = img.resize((new_width, new_height))

        ascii_art = ""
        pixels = img.load()
        for y in range(new_height):
            for x in range(new_width):
                brightness = pixels[x,y]
                char_index = int((brightness / 255) * (len(ascii_characters_by_density) - 1))
                ascii_art += ascii_characters_by_density[char_index]
            ascii_art += "\n"

        return ascii_art
    except Exception as e:
        raise RuntimeError(f"Failed to process the image : {e}")
    
def save_ascii_art(ascii_art, file_path):
    try:
        with open(file_path, "W") as file:
            file.write(ascii_art)
    except Exception as e:
        raise RuntimeError(f"Failed to save art: {e}")
    

def edge_detection(frame, save_path="output"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)


    if len(frame.shape) == 2:
        gray_frame = frame
    elif len(frame.shape) == 3:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("Invalid frame format")
    

    blurred_frame = cv2.GaussianBlur(gray_frame, (5,5), 0)

    sobel_x = cv2.Sobel(blurred_frame, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(blurred_frame, cv2.CV_64F, 0, 1, ksize=3)

    edges = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    edges *= 225.0 / edges.max()
    edges = np.uint8(edges)

    cv2.imwrite(os.path.join(save_path, "edges_frame,jpg"), edges)
    return edges