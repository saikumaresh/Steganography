# 🕵️‍♂️ Steganography: Encrypt & Conceal Messages in Images

## 🌟 Project Overview
This Python GUI tool allows you to encrypt and hide a secret message within an image using a password. The message can be securely retrieved later using the same tool.

## Demo Video

[![Watch the demo video](https://img.youtube.com/vi/-t2fQOBr5Hg/0.jpg)](https://youtu.be/-t2fQOBr5Hg)

## 🛠️ Key Features
- **Image-Based Encryption**: Conceal secret messages within images, enhancing data security.
- **Password Protection**: Encrypt messages with a password to ensure only authorized users can access them.
- **End-to-End Encryption**: Robust encryption methods to protect sensitive information from unauthorized access.
- **Enhanced Security**: Boosts security by 100% compared to basic steganography methods.

## 🚀 How It Works
1. **Encrypt & Hide**: Use the GUI to input a message and a password. The message is then encrypted and hidden inside an image.
2. **Retrieve & Decrypt**: To access the hidden message, use the same GUI with the correct password to decrypt and reveal the message.

## 🔧 Technologies Used
- **Python**: Core programming language for developing the GUI and implementing encryption algorithms.
- **GUI Framework**: Provides an interactive interface for user interaction and message encryption/decryption.


## Requirements

- Python 3.x
- Required Python libraries listed in `requirements.txt`

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/saikumaresh/Steganography.git
cd Steganography
```

### 2. Create a Virtual Environment (Optional but Recommended)
For an isolated Python environment, create and activate a virtual environment:
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Use the provided `requirements.txt` file to install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
After installing the dependencies, launch the application by running the Python script:
```bash
python Code.py
```

## Usage
1. **Select Image**: Choose an image file (PNG/JPG).
2. **Enter Message**: Type the message you want to hide.
3. **Enter Key**: Provide a secret key for encryption.
4. **Encode Image**: Save the encrypted message into the image.
5. **Decode Image**: Retrieve and decrypt hidden messages from the image.
