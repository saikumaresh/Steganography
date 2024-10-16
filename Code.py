from tkinter import *
from tkinter import filedialog, messagebox
from Cryptodome.Cipher import AES, Blowfish
from PIL import Image
import base64
import os

# Padding for encryption
def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

# AES Encryption
def encrypt_aes(key, message):
    cipher = AES.new(pad(key).encode('utf-8'), AES.MODE_ECB)
    encrypted_text = base64.b64encode(cipher.encrypt(pad(message).encode('utf-8')))
    return encrypted_text

# Blowfish Encryption
def encrypt_blowfish(key, message):
    cipher = Blowfish.new(pad(key).encode('utf-8'), Blowfish.MODE_ECB)
    encrypted_text = base64.b64encode(cipher.encrypt(pad(message).encode('utf-8')))
    return encrypted_text

# LSB Encoding
def lsb_encode(image, data):
    encoded_image = image.copy()
    width, height = image.size
    pixels = encoded_image.load()
    data += '=====' # End of message indicator
    data_bits = ''.join([format(ord(char), '08b') for char in data])
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Modify each RGB channel's LSB
                if data_index < len(data_bits):
                    pixel[i] = pixel[i] & ~1 | int(data_bits[data_index])
                    data_index += 1
            pixels[x, y] = tuple(pixel)
            if data_index >= len(data_bits):
                return encoded_image
    return encoded_image

# LSB Decoding Optimization
def lsb_decode(image):
    width, height = image.size
    pixels = image.load()
    data_bits = ''
    
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Read each RGB channel's LSB
                data_bits += str(pixel[i] & 1)
                if len(data_bits) >= 40 and data_bits[-40:] == '0011110100111101001111010011110100111101':  # '=====' in binary
                    all_bytes = [data_bits[i:i+8] for i in range(0, len(data_bits), 8)]
                    decoded_data = ''.join([chr(int(byte, 2)) for byte in all_bytes])
                    return decoded_data.split('=====')[0]
    
    all_bytes = [data_bits[i:i+8] for i in range(0, len(data_bits), 8)]
    decoded_data = ''.join([chr(int(byte, 2)) for byte in all_bytes])
    
    return decoded_data.split('=====')[0]

# Steganography Application
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography with AES and Blowfish")
        
        self.label = Label(root, text="Choose Encryption Method:")
        self.label.pack()
        
        self.var = StringVar(value="AES")
        self.aes_radio = Radiobutton(root, text="AES", variable=self.var, value="AES")
        self.aes_radio.pack()
        self.blowfish_radio = Radiobutton(root, text="Blowfish", variable=self.var, value="Blowfish")
        self.blowfish_radio.pack()
        
        self.message_label = Label(root, text="Enter the Message:")
        self.message_label.pack()
        self.message_entry = Entry(root, width=50)
        self.message_entry.pack()
        
        self.key_label = Label(root, text="Enter the Key:")
        self.key_label.pack()
        self.key_entry = Entry(root, width=50)
        self.key_entry.pack()
        
        self.image_button = Button(root, text="Select Image", command=self.select_image)
        self.image_button.pack()
        
        self.image_label = Label(root, text="No file selected")
        self.image_label.pack()
        
        self.encode_button = Button(root, text="Encode and Save Image", command=self.encode_image)
        self.encode_button.pack()
        
        self.decode_button = Button(root, text="Decode Message from Image", command=self.decode_image)
        self.decode_button.pack()

    def select_image(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.filepath:
            self.image = Image.open(self.filepath)
            self.image_label.config(text=f"File selected: {os.path.basename(self.filepath)}")
        else:
            self.image_label.config(text="No file selected")

    def encode_image(self):
        message = self.message_entry.get()
        key = self.key_entry.get()
        encryption_method = self.var.get()
        
        if encryption_method == "AES":
            encrypted_message = encrypt_aes(key, message)
        else:
            encrypted_message = encrypt_blowfish(key, message)
        
        encrypted_message = encrypted_message.decode('utf-8')
        encoded_image = lsb_encode(self.image, encrypted_message)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        encoded_image.save(save_path)
        messagebox.showinfo("Success", "Image saved successfully!")

    def decode_image(self):
        encrypted_message = lsb_decode(self.image)
        key = self.key_entry.get()
        encryption_method = self.var.get()
        
        try:
            # Pad the encrypted message to make its length a multiple of 16
            if len(encrypted_message) % 16 != 0:
                encrypted_message += '=' * (16 - len(encrypted_message) % 16)
            
            if encryption_method == "AES":
                decrypted_message = base64.b64decode(encrypted_message)
                cipher = AES.new(pad(key).encode('utf-8'), AES.MODE_ECB)
            else:
                decrypted_message = base64.b64decode(encrypted_message)
                cipher = Blowfish.new(pad(key).encode('utf-8'), Blowfish.MODE_ECB)
            
            decrypted_message = cipher.decrypt(decrypted_message).decode('utf-8').strip()
            messagebox.showinfo("Decrypted Message", decrypted_message)
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = SteganographyApp(root)
    root.mainloop()
