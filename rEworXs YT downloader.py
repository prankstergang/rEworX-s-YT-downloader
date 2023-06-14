from tkinter import *
from tkinter import filedialog
import pytube
import requests
from PIL import ImageTk, Image
import io
import os

def download_video():
    global entry_url
    video_url = entry_url.get()
    save_path = filedialog.askdirectory()
    
    try:
        youtube = pytube.YouTube(video_url)
        video = youtube.streams.get_highest_resolution()
        video.download(save_path)
        lbl_status.config(text="Video downloaded successfully!", fg="green")
        
        if var_format.get() == 1:
            mp3_filename = video.title + ".mp3"
            video_filename = video.title + "." + video.subtype
            video_filepath = save_path + "/" + video_filename
            mp3_filepath = save_path + "/" + mp3_filename
            audio = youtube.streams.get_audio_only()
            audio.download(output_path=save_path, filename=video_filename)
            os.rename(video_filepath, mp3_filepath)
            lbl_status.config(text="MP3 downloaded successfully!", fg="green")
            
    except Exception as e:
        lbl_status.config(text=str(e), fg="red")

def create_window():
    global window, entry_url, lbl_status, var_format
    
    window = Tk()
    window.title("YouTube Video Downloader")
    window.geometry("500x300")
    
    icon_url = "https://drive.google.com/uc?export=download&id=1b1skeK0db7X34-tBBLQ3o-MTzGmrMTUm"
    response = requests.get(icon_url)
    icon_data = response.content
    icon_image = Image.open(io.BytesIO(icon_data))
    window.iconphoto(True, ImageTk.PhotoImage(icon_image))
    
    lbl_title = Label(window, text="YouTube Video Downloader", font=("Arial", 16))
    lbl_title.pack(pady=10)
    
    lbl_url = Label(window, text="Video URL:")
    lbl_url.pack()
    
    entry_url = Entry(window, width=50)
    entry_url.pack(pady=5)
    
    lbl_format = Label(window, text="Download Format:")
    lbl_format.pack()
    
    var_format = IntVar()
    rb_mp4 = Radiobutton(window, text="MP4", variable=var_format, value=0)
    rb_mp4.pack()
    rb_mp3 = Radiobutton(window, text="MP3", variable=var_format, value=1)
    rb_mp3.pack()
    
    btn_download = Button(window, text="Download", command=download_video)
    btn_download.pack(pady=10)
    
    lbl_save_location = Label(window, text="Select the save location using the 'Download' button.", wraplength=300)
    lbl_save_location.pack(pady=5)
    
    lbl_status = Label(window, text="", fg="black")
    lbl_status.pack()
    
    window.mainloop()

create_window()