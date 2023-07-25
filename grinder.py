from PIL import Image, ImageDraw, ImageFont
import os
import time
import tkinter as tk
from tkinter import scrolledtext

def create_ascii_window():
    root = tk.Tk()
    root.title("ASCII Animation")
    root.geometry("1000x900")

    frame_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 9), fg='#FFF', bg='#000')
    frame_text.pack(expand=True, fill="both")

    return root, frame_text

def update_ascii_frame(frame_text, ascii_frame):
    frame_text.delete(1.0, tk.END)
    frame_text.insert(tk.END, ascii_frame)

def extract_gif_frames(gif, fillEmpty=False):
    frames=[]
    try:
        while True:
            gif.seek(gif.tell()+1)
            new_frame = Image.new('RGBA',gif.size)
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            
            #check if we are painting over a canvas
            if fillEmpty:
                canvas=Image.new('RGBA', new_frame.size, (255,255,255,255))
                canvas.paste(new_frame, mask=new_frame)
                new_frame=canvas
            frames.append(new_frame)
    except EOFError:
        pass # end of sequence
    return frames

def save_frames_list(frames):        
    i=0
    for frame in frames:
        i+=1
        frame.save('test%d.png'%i,**frame.info)

def convert_image_to_ascii(image):
    font = ImageFont.load_default() # load default bitmap monospaced font
    (chrx, chry) = font.getsize(chr(32))
    # calculate weights of ASCII chars
    weights = []
    for i in range(32, 127):
        chrImage = font.getmask(chr(i))
        ctr = 0
        for y in range(chry):
            for x in range(chrx):
                if chrImage.getpixel((x, y)) > 0:
                    ctr += 1
        weights.append(float(ctr) / (chrx * chry))
    
    output = ""
    (imgx, imgy) = image.size
    imgx = int(imgx / chrx)
    imgy = int(imgy / chry)
    # NEAREST/BILINEAR/BICUBIC/ANTIALIAS
    image = image.resize((imgx, imgy), Image.BICUBIC)
    image = image.convert("L") # convert to grayscale
    pixels = image.load()
    for y in range(imgy):
        for x in range(imgx):
            w = float(pixels[x, y]) / 255 / intensity_multiplier
            # find closest weight match
            wf = -1.0; k = -1
            for i in range(len(weights)):
                if abs(weights[i] - w) <= abs(wf - w):
                    wf = weights[i]; k = i
            output+=chr(k + 32)
        output+="\n"
    return output

def convert_frames_to_ascii(frames):
    ascii_frames = []
    for frame in frames:
        new_frame = convert_image_to_ascii(frame)
        ascii_frames.append(new_frame)
    return ascii_frames

def animate_ascii(ascii_frames, num_iterations):
    root, frame_text = create_ascii_window()
    for i in range(num_iterations):
        for frame in ascii_frames:
            update_ascii_frame(frame_text, frame)
            time.sleep(0.05)
            root.update()  # Update the GUI window to display the new ASCII frame
    root.destroy()

im = Image.open("grinderr.gif")
frames = extract_gif_frames(im, fillEmpty=True)

intensity_multiplier = 3
ascii_frames = convert_frames_to_ascii(frames)
animate_ascii(ascii_frames, num_iterations=3)