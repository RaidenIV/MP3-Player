from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

#Set up GUI
root = Tk()
root.title('MUSIC PLAYER')
root.iconbitmap('C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/#PORTFOLIO#/Icons/musical-note_461146.ico')
root.geometry("500x400")

#Initialize PyGame mixer
pygame.mixer.init()

#Grab song length time info
def play_time():
    #Check for double timing
    if stopped:
        return
    #Grab current song elaspsed time
    current_time = pygame.mixer.music.get_pos() / 1000

    #Convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    #Grab song title from playlist
    song = song_box.get(ACTIVE)
    #Add directory structure and wav to song title
    song = f'C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX/{song}.mp3'

    #Load song with Mutagen
    song_mut = MP3(song)
    #Get song length
    global song_length
    song_length = song_mut.info.length

    #Convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    #Increase current time by 1 second
    current_time +=1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} of {converted_song_length}  ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        #Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else: 
        #Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        #Convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        #Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

        #Move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    #Update time
    status_bar.after(1000, play_time)

#Add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX', title="Choose A Song", filetypes=(("wav files", "*.mp3"), ))
    song = song.replace('C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX/', "")
    song = song.replace('.mp3', "")

    #Add song to listbox
    song_box.insert(END, song)

#Add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX', title="Choose A Song", filetypes=(("wav files", "*.mp3"), ))

    # Loop through song list and replace directory with info and wav
    for song in songs:
        song = song.replace('C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX/', "")
        song = song.replace('.mp3', "")

        #Insert into playlist
        song_box.insert(END, song)

#Play selected song
def play():
    #Set stopped variable to "False"
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Call play_time function to get song length
    play_time()

#Stop playing current song
global stopped
stopped = False
def stop():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    #Stop song from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #Clear the status bar
    status_bar.config(text='')

    #Set stop variable to True
    global stopped
    stopped = True

#Play the next song in the playlist
def next_song():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    #Get the current song tuple number
    next_one = song_box.curselection()
    #Add one to the current song number
    next_one = next_one[0]+1
    #Grab song title from playlist
    song = song_box.get(next_one)
    #Add directory structure and wav to song title
    song = f'C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX/{song}.mp3'
    #Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    #Activate new song bar
    song_box.activate(next_one)

    #Set active bar to next song
    song_box.selection_set(next_one, last=None)

#Play previous song in playlist
def previous_song():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    #Get the current song tuple number
    next_one = song_box.curselection()
    #Subtract one to the current song number
    next_one = next_one[0]-1
    #Grab song title from playlist
    song = song_box.get(next_one)
    #Add directory structure and wav to song title
    song = f'C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX/{song}.mp3'
    #Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    #Activate new song bar
    song_box.activate(next_one)

    #Set active bar to next song
    song_box.selection_set(next_one, last=None)

#Delete a song
def delete_song():
    stop()
    #Delete currently selected song
    song_box.delete(ANCHOR)
    #Stop music if it's playing
    pygame.mixer.music.stop()

#Delete all songs from playlist
def delete_all_songs():
    stop()
    #Delete all songs
    song_box.delete(0, END)
    #Stop music if it's playing
    pygame.mixer.music.stop()

#Create global pause variable
global paused
paused = False

#Pause and unpause current song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #Pause
        pygame.mixer.music.pause()
        paused = True

#Create slider function
def slide(x):
    song = song_box.get(ACTIVE)
    song = f'C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/Python Assets/Test Audio SFX/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#Create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

#Create playlist box
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="white")
song_box.grid(row=0, column=0)

#Define player control button Images
back_btn_img = PhotoImage(file='C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/#PORTFOLIO#/Icons/icons8-rewind-48.png')
forward_btn_img = PhotoImage(file='C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/#PORTFOLIO#/Icons/icons8-fast-forward-48.png')
play_btn_img = PhotoImage(file='C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/#PORTFOLIO#/Icons/icons8-play-48.png')
pause_btn_img = PhotoImage(file='C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/#PORTFOLIO#/Icons/icons8-pause-48.png')
stop_btn_img = PhotoImage(file='C:/Users/RAIDEN LABS/Documents/PYTHON PROJECTS/#PORTFOLIO#/Icons/icons8-stop-48.png')

#Create player control frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

#Create volume label frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

#Create player control buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=4, padx=10)
play_button.grid(row=0, column=1, padx=10)
pause_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=3, padx=10)

#Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

#Add many songs to the playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

#Create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Song From Playlist", command=delete_all_songs)

#Create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Create music position slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

#Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

root.mainloop()