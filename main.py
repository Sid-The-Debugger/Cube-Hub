from random import choice, sample, randint
import tkinter as tk
import tkinter.font as font
from tkinter.ttk import *
from tkinter import messagebox
from datetime import datetime

# test commit

time_data = []
counter = 66600
running = False
elapsed = 0

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 

def counter_label(label):  
    def count():  
        if running:  
            global counter  
            global elapsed
    
            # To manage the intial delay.  
            if counter==66600:              
                display="Starting..."
            else:
                tt = datetime.fromtimestamp(counter) 
                display = convert(elapsed)
                elapsed += 1  
    
            label['text'] = display   # Or label.config(text=display)  
    
            # label.after(arg1, arg2) delays by   
            # first argument given in milliseconds  
            # and then calls the function given as second argument.  
            # Generally like here we need to call the   
            # function in which it is present repeatedly.  
            # Delays by 1000ms=1 seconds and call count again.  
            label.after(1000, count)   
            counter += 1
    
    # Triggering the start of the counter.  
    count()       
    
def export_times():
  with open("rubik's_time_table.txt", 'w') as f:
    for item in time_data:
      f.write("%s\n" % item)
# start function of the stopwatch  
def Start(label):  
    global running  
    running=True
    counter_label(label)
    start['state']='disabled'
    stop['state']='normal'
    scrambler["text"] = "Scramble"
    
# Stop function of the stopwatch  
def Stop():  
    global running  
    global listbox
    global counter  
    global elapsed
    time_data.append(convert(elapsed))
    start['state']='normal'
    stop['state']='disabled'
    label["text"] = convert(elapsed)
    running = False
    listbox.pack_forget()
    listbox = tk.Listbox(root, selectmode = "multiple", bg = "#66cdaa", relief = tk.SUNKEN)
    for idx, val in enumerate(time_data):
      listbox.insert(idx, "[" + str(idx + 1) + "] " + val)
    label.pack_forget()
    label.pack()
    f.pack_forget() 
    start.pack_forget()  
    stop.pack_forget()
    delete_time.pack_forget()
    export_time.pack_forget()
    quit_butt.pack_forget()
    label.pack()
    listbox.pack()
    f.pack(expand = tk.TRUE, anchor = 'center') 
    start.pack(side="left")  
    stop.pack(side ="left")
    delete_time.pack(side = "left")
    export_time.pack(side = "left")
    quit_butt.pack(side = "left")
    counter=66600
    elapsed = 0
    label['text']='Stopwatch'

moves = ["U", "D", "F", "B", "R", "L"]
dir = []
dir1 = ["" for _ in range(randint(1, 3))]
dir2 = ["'" for _ in range(randint(1, 3))]
dir3 = ["2" for _ in range(randint(1, 3))]
dir.extend(dir1)
dir.extend(dir2)
dir.extend(dir3)

def gen_scramble(length):
    # Make array of arrays that represent moves ex. U' = ["U", "'"]
    s = valid([[choice(moves), choice(dir)] for x in range(length)])
    cube = sample(s, length)

    # Format scramble to a string with movecount
    return "".join(str(s[x][0]) + str(s[x][1]) + " " for x in range(len(s))) + "[" + str(length) + "]"

def valid(ar):
    # Check if Move behind or 2 behind is the same as the random move
    # this gets rid of "R R2" or "R L R2" or similar for all moves
    for x in range(1, len(ar)):
        while ar[x][0] == ar[x-1][0]:
            ar[x][0] = choice(moves)
    for x in range(2, len(ar)):
        while ar[x][0] == ar[x-2][0] or ar[x][0] == ar[x-1][0]:
            ar[x][0] = choice(moves)
    return ar

def scramble():
  s = gen_scramble(randint(20,25))
  scrambler["text"] = s

def call_delete():
    # selection = listbox.curselection()
    # listbox.delete(selection)
    # del time_data[selection[0]]
    items = listbox.curselection()
    try:
      for item in items:
        listbox.delete(item)
        del time_data[item]
    except:
      pass

def key_press(event):
  key = event.char
  Stop()

root = tk.Tk()
root.title("Rubik's Cube Scrambler")
root.geometry("300x200")
root["bg"] = "#66cdaa"
frame = tk.Frame(root)
frame.pack(fill = tk.BOTH, expand = True)

scrambler = tk.Button(frame,
                  text="Scramble",
                  bg = "#66cdaa",
                  compound = "c",
                  command=scramble)
scrambler['font'] = "Verdana 20"
scrambler.pack(fill = tk.BOTH, expand = True)  

label = tk.Label(root, text="Stopwatch\n", fg="black", font="Verdana 20 bold", bg = "#66cdaa")  
label.pack()  
f = tk.Frame(root) 
start = tk.Button(f, text='Start', width=6, command=lambda:Start(label))  
stop = tk.Button(f, text='Stop',width=6,state='disabled', command=Stop)
delete_time = tk.Button(f, text = "Delete Selected Time", width = 16, command = call_delete)
export_time = tk.Button(f, text = "Export Times", width = 10, command = export_times)

listbox = tk.Listbox(root, selectmode = "multiple", bg = "#66cdaa", relief = tk.SUNKEN)
for i in range(len(time_data)):
  listbox.insert(i, time_data[i])
listbox.pack()

f.pack(expand = tk.TRUE, anchor = 'center') 
start.pack(side="left")  
stop.pack(side ="left")
delete_time.pack(side = "left")
export_time.pack(side = "left")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

quit_butt = tk.Button(f, text = "Quit", width = 4, command = on_closing)
quit_butt.pack(side = "left")

root.bind("<space>", key_press)
root.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()