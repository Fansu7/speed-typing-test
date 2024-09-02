import customtkinter as ctk
from tkinter import messagebox
import time
import threading

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


SAMPLE_TEXT = ('In a quiet village nestled between rolling hills, time seemed to flow with a gentle ease. The '
               'mornings were painted with the soft light of dawn, as the sun rose slowly over the horizon, '
               'casting long shadows across the dew-covered fields. The villagers began their day with a sense of '
               'purpose, each task a part of the rhythm of life that had remained unchanged for generations. As the '
               'day warmed, the scent of fresh bread wafted from the bakery, mingling with the earthy aroma of the '
               'surrounding forest. By evening, the sky was ablaze with hues of orange and pink, and the village '
               'settled into a peaceful silence, the only sound being the occasional rustle of leaves in the evening '
               'breeze.')

def key_handler(event):
    global contador
    contador += 1
    if SAMPLE_TEXT[contador] == event.char:
        index = '%d.%d' %(1, contador+1)
        escrito.append(event.keysym)
        text.tag_add("right", 1.0, index)
    else:
        contador -= 1


def timer_fun(escrito):
    global segundos
    frase = ''
    root.bind("<Key>", key_handler)
    while segundos <= 10:
        timer_label.configure(text=str(segundos))
        segundos += 1
        time.sleep(1)
        root.update()

    root.unbind("<Key>")

    for letra in escrito:
        if letra == 'space':
            frase += ' '
        elif letra == 'comma':
            frase += ','
        elif letra == 'period':
            frase += '.'
        else:
            frase += letra

    palabras = frase.split()
    user_score(len(palabras), contador)


def user_score(palabras, key_count):
    kpm = round(key_count / 60, 2)
    wpm = round(palabras / 60, 2)
    messagebox.showinfo(title="User score", message=(f'Score:\n {wpm} word per minute / {kpm} keys pressed per minute.'))


def start():
    btn_start.pack_forget()
    timer_thread = threading.Thread(target=timer_fun, args=(escrito,))
    timer_thread.start()


def exit_window():
    root.destroy()
    exit()


#Main window
root = ctk.CTk()
root.geometry("1280x600")
root.configure(background="#ebebeb")

#Frames
main_frame = ctk.CTkCanvas(root, borderwidth=0, highlightthickness=0, background='#ebebeb')
btn_frame = ctk.CTkCanvas(root, borderwidth=0, highlightthickness=0, background='#ebebeb')

main_frame.pack(pady=10)
btn_frame.pack(pady=10)

contador = -1
segundos = 0
escrito = []

#Timer
timer_label = ctk.CTkLabel(master=main_frame, text=str(segundos), font=("arial", 20))
timer_label.pack(pady=40)

text = ctk.CTkTextbox(main_frame, width=1000, height=200, border_width=0, font=("arial", 20))
text.insert(index='insert', text=SAMPLE_TEXT)
text.configure(state='disabled')
text.pack(pady=10)
text.tag_config("right", foreground="green")
text.tag_config("restart", foreground="black")

btn_start = ctk.CTkButton(master=btn_frame, text="Start", command=start)
btn_start.pack(side="left", padx=10)

btn_exit = ctk.CTkButton(master=btn_frame, text="Exit", command=exit_window)
btn_exit.pack(side="right")

root.mainloop()




