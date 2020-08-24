from tkinter import * 
from tkinter.ttk import * 
import tkinter as tk
from tkinter import ttk
from youtubesearchpython import SearchVideos
import time
import pafy
import vlc
import os
import threading


if not os.path.exists('downloads'):
        os.makedirs('downloads')  
folder = 'downloads' 
directory = os.getcwd() 
SAVE_PATH = os.path.join(directory, folder)
win = root = tk.Tk()
win.geometry("600x500") 
win.title("YouTUBE") 
win.resizable(False, False) 
name = {}
link = {} 
Instance = vlc.Instance() 
player = Instance.media_player_new()
title = StringVar()
category = StringVar()
author = StringVar()
duration = StringVar()

def search(event):
    listbox.delete(0,END)
    # accepting the keywords entered in the gui
    key = inputtxt.get()
    
    # making the name and links be altered and available at different functions
    global name
    global links
    
    # searching youtube
    search = SearchVideos(key, offset = 1, mode = "json", max_results = 20)   
    # making the name and links dict 
    i = 1
    while i != 21 :
        for n in search.titles:
            temp_name = {n: i}
            name.update(temp_name)
            # adding each name to the list box
            listbox.insert(END, n)
            i+=1
    f =  0
    while f != 20 :
        for l in search.links:
            temp_link = {f: l}
            # making the corresponding link dictionary 
            link.update(temp_link)
            f += 1
    print(name)
    print(link)
 
    
# finding the selected option from listbox
def pass_CurSelet(event):
    cs = threading.Thread(target=lambda : CurSelet(event))
    cs.start()
    
def CurSelet(evt):
    # getting the name of the selected video
    temp_no = listbox.curselection()
    for no in temp_no:
        number = no 
    # finding the link using the index of the name dict
    global link_to_video
    link_to_video = (link[number])
    print(link_to_video)
    
    
def details():
    # displaying all the details of the video
    url = link_to_video
    video = pafy.new(url)
    # displaying the duration of the video
    value = video.length
    ty_res = time.gmtime(value) 
    res = time.strftime("%H:%M:%S",ty_res)
    lbl = Label(text = res)
    lbl.place(relx = 0.65, rely = 0.64)
    # displaying the title of the video
    title = video.title + "                       "
    lbl = Label(text = title)
    lbl.place(relx = 0.65, rely = 0.49)
    # displaying the author of the video
    author = video.author+ "                       "
    lbl = Label(text = author)
    lbl.place(relx = 0.65, rely = 0.54)
    # displaying the category of the video
    category = video.category+ "                       "
    lbl = Label(text = category)
    lbl.place(relx = 0.65, rely = 0.59)

    
# streaming audio from youtute link    
def stream_audio():
    print(link_to_video)
    url = link_to_video 
    audio = pafy.new(url)
    best = audio.getbestaudio()
    playurl = best.url 
    Media = Instance.media_new(playurl) 
    Media.get_mrl() 
    player.set_media(Media)         
    player.play()
    
  
# streaming video from youtube link
def stream_video():
    print(link_to_video)
    url = link_to_video
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url 
    Media = Instance.media_new(playurl)
    Media.get_mrl() 
    player.set_media(Media) 
    player.play()
    
# player controls
def play():
    player.play()
def pause():  
    player.pause()
    player.set_rate(1)
def stop():
    player.stop()  
def pass_fforward():
    ff = threading.Thread(target=lambda : fforward())
    ff.start()
def fforward():
    player.set_position(player.get_position()+160/6000.0)
def pass_fbackward():
    fb = threading.Thread(target=lambda : fbackward())
    fb.start()
def fbackward():
    player.set_position(player.get_position()-160/6000.0)
i = 0
def speedforward():
    global i
    i += 1
    player.set_rate(i)
j = 1
def slowdown():
    global j 
    j = j / 2 
    player.set_rate(j)
    print(j)
def normal_speed():
    player.set_rate(1)

# opening downloads folder
def open_folder():
    os.startfile("downloads")

def pass_load_downloads():
    ld = threading.Thread(target=lambda : load_downloads())
    ld.start()
    
    
# downloading options
def load_downloads():
    video = pafy.new(link_to_video)
    global video_formats
    video_formats = video.streams + video.videostreams +  video.audiostreams
    
    btn_v = Button(text = "show options", command = pass_top_window)
    btn_v.place(relx = 0.25, rely = 0.67)
    
    
def pass_top_window():
    topThread = threading.Thread(target=lambda : top_window())
    topThread.start()
    
    
def pass_download_confirm():
    dc = threading.Thread(target=lambda : download_confirm())
    dc.start()
    
    
# making seperate window for downlaod    
def top_window():
    global top
    top = Toplevel()
    top.geometry("275x325")
    top.title("download")
    top.resizable(False, False)
    lbl = Label(top, text = "select a format")
    lbl.place(relx = 0.01 , rely = 0.01 )
    global listboxtop
    listboxtop = Listbox(top, height = 15,  width = 40,  bg = "white", activestyle = 'dotbox', fg = "black") 
    listboxtop.place(relx = 0.054 , rely = 0.06)
    selected = listboxtop.bind('<<ListboxSelect>>',pass_download)
    for vf in video_formats:
        listboxtop.insert(END, vf)
def pass_download(event):
    pd = threading.Thread(target=lambda : download(event))
    pd.start()
# for downloading video
def download(event):
    number = (listboxtop.curselection())
    for no in number:
        number_new = no
    print(number_new)
    to_download = number_new  
    size = str(round(((video_formats[to_download].get_filesize())/1024000))) + " MB        "
    print(to_download)
    print(size)
    lbl = Label(top, text = size)
    lbl.place(relx = 0.1, rely = 0.89)
    btn = Button(top, text = "download", command = pass_download_confirm) 
    btn.place(relx = 0.65, rely = 0.89)
    
def pass_mycb(total, recvd, ratio, rate, eta):
    downloadThread = threading.Thread(target=lambda : mycb(total, recvd, ratio, rate, eta))
    downloadThread.start()
    
    
def mycb(total, recvd, ratio, rate, eta):
    percent = 0
    percent = round(ratio*100)
    print(percent)
    mpb = Progressbar(top,orient ="horizontal",length = 250, mode ="determinate") 
    mpb.place(relx = 0.01,rely = 0.82) 
    mpb["maximum"] = 100 
    mpb["value"] = percent
    top.update_idletasks()
    
    
def download_confirm():
    print(listboxtop.index(ACTIVE))
    to_download = listboxtop.index(ACTIVE)
    video_formats[to_download].download(SAVE_PATH, quiet = True,  callback = pass_mycb) 
    os.startfile("downloads")
def pass_help():
    h = threading.Thread(target=lambda : phelp())
    h.start()
    
def phelp():
    global top_2
    top_2 = Toplevel()
    top_2.geometry("600x150")
    top_2.title("help")
    top_2.resizable(False, False)
    lbl = Label(top_2,text = "normal means it contains both the audio as well as the video")
    lbl2 = Label(top_2,text = "video means it contains only the video")
    lbl3 = Label(top_2,text = "audio means it contains only the audio")
    lbl.pack()
    lbl2.pack()
    lbl3.pack()
    lbl4 = Label(top_2, text = "this is due to the YouTUBE DASH format")
    lbl4.pack()
    lbl = Label(top_2,text = "while selecting a downlaod option")
    lbl.pack()
    
    
lbl = Label(win, text = "  ")
lbl.grid(column = 0, row= 0 , padx = 7, sticky = 'e')

	
l = Label(win, text = "YouTube Search")
l.grid(column = 0, row= 1 , padx = 7, pady = 3, sticky = 'e')
 
inputtxt =  Entry(win, width=75)
inputtxt.place(relx = 0.18 , rely = 0.04)
inputtxt.bind("<Return>", search)


lbl = Label(text="enter in the box above and click enter, search results will be displayed here")
lbl.place(relx = 0.05, rely = 0.115)

listbox = Listbox(win, height = 7,  width = 88,  bg = "white", activestyle = 'dotbox', fg = "black") 
listbox.place(relx = 0.05 , rely = 0.15)
selected = listbox.bind('<ButtonPress-1>',pass_CurSelet)

btn = Button(win , text = "play audio", command = stream_audio)
btn.place(relx = 0.05, rely = 0.39)

btn = Button(win, text = "play video", command =stream_video)
btn.place(relx = 0.18, rely = 0.39)

btn = Button(win, text = "details", command = details)
btn.place(relx = 0.811, rely = 0.39)

lbl = Label(text = "Title :")
lbl.place(relx = 0.52, rely = 0.49)

lbl = Label(text = "Author :")
lbl.place(relx = 0.52, rely = 0.54)

lbl = Label(text = "Category :")
lbl.place(relx = 0.52, rely = 0.59)

lbl = Label(text = "Duration :")
lbl.place(relx = 0.52, rely = 0.64)

btn = Button(win, text = "veiw details about downloading ", command = pass_help)
btn.place(relx = 0.68, rely = 0.915)

lbl = Label(win, text = "Download :")
lbl.place(relx = 0.01, rely = 0.55)

btn = Button(win , text = "load download options", command = pass_load_downloads)
btn.place(relx = 0.116, rely = 0.545)

btn = Button(win, text = "open folder", command = open_folder)
btn.place(relx = 0.36, rely = 0.545)

lbl = Label(win , text = "available video formats : ")
lbl.place(relx = 0.01, rely = 0.67)


lbl = Label(text = "controls :")
lbl.place(relx = 0.05, rely = 0.78)

play = Button(win, text = "|| \ >", command = pause)
play.place(relx = 0.18, rely = 0.85)

fforward = Button(win, text = ">>5secs", command = fforward)
fforward.place(relx = 0.308, rely = 0.85)

fastforward = Button(win, text = ">>2x", command = speedforward)
fastforward.place(relx = 0.308, rely = 0.899)

slow = Button(win, text = "<<1/2x", command = slowdown)
slow.place(relx = 0.052, rely = 0.899)

fbackward = Button(win, text = "5secs<<", command = fbackward)
fbackward.place(relx = 0.052, rely = 0.85)

stop = Button(win, text = "x", command = stop)
stop.place(relx = 0.18, rely = 0.798)

ns = Button(win, text = "1x", command = normal_speed)
ns.place(relx = 0.18, rely = 0.899)


lbl = Label(text = "coded by akhil_raj_s / py_57")
lbl.place(relx = 0.008, rely = 0.956)
mainloop() 
