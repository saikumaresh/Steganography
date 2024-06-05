from tkinter import *
from tkinter import messagebox
from argparse import FileType
from tkinter.filedialog import *
from PIL import ImageTk, Image
from PIL import Image
from tkinter import font as tkFont
from subprocess import Popen
import chilkat
import datetime


###########################################################################################################################
# Functions for enc/dec and steg
###########################################################################################################################


def genData(data):

    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def encrypt_aes(keyHex, data):
    crypt = chilkat.CkCrypt2()
    crypt.put_CryptAlgorithm("aes")
    crypt.put_CipherMode("cbc")
    crypt.put_KeyLength(8)
    crypt.put_PaddingScheme(0)
    crypt.put_EncodingMode("hex")
    ivHex = "0001020304050607"
    crypt.SetEncodedIV(ivHex, "hex")
    crypt.SetEncodedKey(keyHex, "hex")
    encStr = crypt.encryptStringENC(data)
    return encStr


def decrypt_aes(keyHex, data):
    crypt = chilkat.CkCrypt2()
    crypt.put_CryptAlgorithm("aes")
    crypt.put_CipherMode("cbc")
    crypt.put_KeyLength(8)
    crypt.put_PaddingScheme(0)
    crypt.put_EncodingMode("hex")
    ivHex = "0001020304050607"
    crypt.SetEncodedIV(ivHex, "hex")
    crypt.SetEncodedKey(keyHex, "hex")
    decStr = crypt.decryptStringENC(data)
    return decStr


def encrypt_bf(keyHex, data):
    crypt = chilkat.CkCrypt2()
    crypt.put_CryptAlgorithm("blowfish2")
    crypt.put_CipherMode("cbc")
    crypt.put_KeyLength(8)
    crypt.put_PaddingScheme(0)
    crypt.put_EncodingMode("hex")
    ivHex = "0001020304050607"
    crypt.SetEncodedIV(ivHex, "hex")
    crypt.SetEncodedKey(keyHex, "hex")

    encStr = crypt.encryptStringENC(data)
    return encStr


def decrypt_bf(keyHex, data):
    crypt = chilkat.CkCrypt2()
    crypt.put_CryptAlgorithm("blowfish2")
    crypt.put_CipherMode("cbc")
    crypt.put_KeyLength(8)
    crypt.put_PaddingScheme(0)
    crypt.put_EncodingMode("hex")
    ivHex = "0001020304050607"
    crypt.SetEncodedIV(ivHex, "hex")
    crypt.SetEncodedKey(keyHex, "hex")
    decStr = crypt.decryptStringENC((data))
    return decStr
###########################################################################################################################
#  Encoding page
###########################################################################################################################


def encode_page():
    window.destroy()
    enc = Tk()
    enc.attributes("-fullscreen", True)
    enc.wm_attributes('-transparentcolor')
    img = ImageTk.PhotoImage(Image.open("bg2.jpg"))
    fontl = tkFont.Font(family='Algerian', size=32)
    label1 = Label(enc, image=img)
    label1.pack()

    LabelTitle = Label(text="ENCODE", bg="red", fg="white", width=20)
    LabelTitle['font'] = fontl
    LabelTitle.place(relx=0.6, rely=0.1)

    def openfile():
        global fileopen
        global imagee

        fileopen = StringVar()
        fileopen = askopenfilename(initialdir="/Desktop", title="Select file",
                                   filetypes=(("jpeg,png files", "*jpg *png"), ("all files", "*.*")))
        imagee = ImageTk.PhotoImage(Image.open(fileopen))

        Labelpath = Label(text=fileopen)
        Labelpath.place(relx=0.6, rely=0.25, height=21, width=450)

        Labelimg = Label(image=imagee)
        Labelimg.place(relx=0.7, rely=0.3, height=200, width=200)

    Button2 = Button(text="Select Image", command=openfile)
    Button2.place(relx=0.7, rely=0.2, height=31, width=94)

    enc_type = StringVar()
    radio1 = Radiobutton(text='AES', value='AES', variable=enc_type)
    radio1.place(relx=0.7, rely=0.57)

    radio2 = Radiobutton(text='Blowfish', value='Blowfish', variable=enc_type)
    radio2.place(relx=0.8, rely=0.57)

    opt_type = StringVar()
    radio3 = Radiobutton(text='JPG', value='jpg', variable=opt_type)
    radio3.place(relx=0.7, rely=0.62)

    radio4 = Radiobutton(text='PNG', value='png', variable=opt_type)
    radio4.place(relx=0.8, rely=0.62)

    radio6 = Radiobutton(text='BMP', value='bmp', variable=opt_type)
    radio6.place(relx=0.9, rely=0.62)

    Label1 = Label(text="Enter message: ")
    Label1.place(relx=0.6, rely=0.67, height=21, width=104)
    messgae_entry = Entry()
    messgae_entry.place(relx=0.7, rely=0.67, relheight=0.04, relwidth=0.200)

    Label2 = Label(text="Secret Key: ")
    Label2.place(relx=0.6, rely=0.75, height=21, width=104)
    key_entry = Entry()
    key_entry.place(relx=0.7, rely=0.75, relheight=0.04, relwidth=0.200)

    Label3 = Label(text="Output file name: ")
    Label3.place(relx=0.6, rely=0.82, height=21, width=124)
    output_name = Entry()
    output_name.place(relx=0.7, rely=0.82, relheight=0.04, relwidth=0.200)

    def steg_enc(data):
        img = str(fileopen)
        image = Image.open(img, 'r')
        newimg = image.copy()
        encode_enc(newimg, data)
        new_img_name = output_name.get()+"."+opt_type.get()
        #newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        newimg.save(new_img_name)
        messagebox.showinfo("popup", "Successful !")

    def encode():
        data= messgae_entry.get()
        if enc_type.get() == 'AES':
            data = encrypt_aes(key_entry.get(),data)
            steg_enc(data)
        if enc_type.get() == 'Blowfish':
            data = encrypt_bf(key_entry.get(), data)
            steg_enc(data)
        Label4 = Label(text="Encrypted text:  "+data)
        Label4.place(relx=0.6, rely=0.88, height=21, width=400)
        current_time = datetime.datetime.now()
        f = open(output_name.get()+".txt", "a")
        f.write("Time : " + str(current_time) + "\nFilename: "+output_name.get()+"."+opt_type.get() +
                "\nEncryption Method: "+enc_type.get()+"\nSecret key: "+key_entry.get()+"\nEncrypted text: "+data)
        f.close()
    	

    Button2 = Button(text="ENCODE", command=encode)
    Button2.place(relx=0.7, rely=0.92, height=31, width=94)

    def back():
        enc.destroy()
        Popen('python GUI.py')
    Buttonback = Button(text="Back", command=back)
    Buttonback.place(relx=0.8, rely=0.92, height=31, width=94)

    enc.mainloop()
###########################################################################################################################
#  Decoding page
###########################################################################################################################


def decode_page():
    window.destroy()
    dec = Tk()
    dec.attributes("-fullscreen", True)
    dec.wm_attributes('-transparentcolor')
    img = ImageTk.PhotoImage(Image.open("bg2.jpg"))
    fontl = tkFont.Font(family='Algerian', size=32)
    label1 = Label(dec, image=img)
    label1.pack()

    LabelTitle = Label(text="DECODE", bg="blue", fg="white", width=20)
    LabelTitle['font'] = fontl
    LabelTitle.place(relx=0.6, rely=0.1)

    enc_type = StringVar()
    radio1 = Radiobutton(text='AES', value='a', variable=enc_type)
    radio1.place(relx=0.7, rely=0.57)

    radio2 = Radiobutton(text='Blowfish', value='b', variable=enc_type)
    radio2.place(relx=0.8, rely=0.57)

    Label1 = Label(text="Secret Key: ")
    Label1.place(relx=0.6, rely=0.70, height=21, width=104)
    key_entry = Entry()
    key_entry.place(relx=0.7, rely=0.70, relheight=0.05, relwidth=0.200)

    def openfile():
        global fileopen
        global imagee
        fileopen = StringVar()
        fileopen = askopenfilename(initialdir="/Desktop", title="Select file", filetypes=(
            ("jpeg files, png file", "*jpg *png"), ("all files", "*.*")))

        imagee = ImageTk.PhotoImage(Image.open(fileopen))
        Labelpath = Label(text=fileopen)
        Labelpath.place(relx=0.6, rely=0.25, height=21, width=450)

        Labelimg = Label(image=imagee)
        Labelimg.place(relx=0.7, rely=0.3, height=200, width=200)
        if fileopen[-3:]!='png':
            im1 = Image.open(fileopen)
            im1.save(fileopen[:-4]+'_dec.png')
            sk=fileopen[:-4]+'_dec.png'
            fileopen=sk

    def steg_dec():
        image = Image.open(fileopen, 'r')
        data = ''
        imgdata = iter(image.getdata())
        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'
            data += chr(int(binstr, 2))
            if (pixels[-1] % 2 != 0):
                return data

    def deimg():
        if enc_type.get() == 'a':
            data = steg_dec()
            decoded_message = decrypt_aes(key_entry.get(), data)
            Label2 = Label(text="Secret message: "+str(decoded_message))
            Label2.place(relx=0.7, rely=0.9, height=21, width=304)
        if enc_type.get() == 'b':
            data = steg_dec()
            decoded_message = decrypt_bf(key_entry.get(), data)
            Label2 = Label(text="Secret message: "+str(decoded_message))
            #Label2 = Label(text="Secret message: "+str(data))
            Label2.place(relx=0.7, rely=0.9, height=21, width=304)

    Button2 = Button(text="Openfile", command=openfile)
    Button2.place(relx=0.7, rely=0.2, height=31, width=94)

    Button2 = Button(text="DECODE", command=deimg)
    Button2.place(relx=0.7, rely=0.8, height=31, width=94)

    def back():
        dec.destroy()
        Popen('python GUI.py')

    Buttonback = Button(text="Back", command=back)
    Buttonback.place(relx=0.7, rely=0.85, height=31, width=94)
    dec.mainloop()


###########################################################################################################################
#  Main page
###########################################################################################################################
window = Tk()
window.attributes("-fullscreen", True)
window.title('Enc & Dec Panel ')
fontl = tkFont.Font(family='Algerian', size=32)
global image1
image1 = ImageTk.PhotoImage(Image.open("bg1.jpg"))
label = Label(window, text="lalal", image=image1)
label.pack()
encbutton = Button(text='Encode', fg="white", bg="black",
                   width=20, command=encode_page)
encbutton['font'] = fontl
encbutton.place(relx=0.6, rely=0.3)


decbutton = Button(text='Decode', fg="white", bg="black",
                   width=20, command=decode_page)
decbutton['font'] = fontl
decbutton.place(relx=0.6, rely=0.5)


def exit():
    window.destroy()


closebutton = Button(text='EXIT', fg="white", bg="red", width=20, command=exit)
closebutton['font'] = fontl
closebutton.place(relx=0.6, rely=0.7)
window.mainloop()
###########################################################################################################################
