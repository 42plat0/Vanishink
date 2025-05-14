from tkinter import *

from imports.KeyHistory import KeyHistory

# -----------------------------------------------------------------------------------------
# LOGIC
# -----------------------------------------------------------------------------------------
from time import sleep

SLEEP_TIME : float = 0.1

def vanish(area : Text) -> None:
    # depends on starting symbol
    area.delete('1.2', 'end')


user_text = ""
timer = None

key_history : KeyHistory = KeyHistory() 

EXIT_COMBO : str = "jk" 

def exit_combo_remove(text : str) -> None:
    return "".join(text.split(EXIT_COMBO))

def start_calculating(event):
    global timer, user_text
    
    if timer is not None:
        window.after_cancel(timer)

    pressed_key : str = event.keysym

    if pressed_key == "BackSpace" and len(user_text):
        user_text = user_text[0: len(user_text) - 1]
        key_history.remove()
    elif event.char:
        user_text += event.char
        key_history.insert(event.char)
        print(key_history.items)

    # previous: pressed_key == "period" or pressed_key == "Return"
    # TODO: idea -> by sentences
    if key_history.is_combination_executed(EXIT_COMBO):
        timer = window.after(10, reset_app)
    

    return


def reset_app():
    global timer, user_text
    vanish(typing_area)
    user_text += "\n"
    timer = None
    key_history.clean()
    return


def save_text_to_file(e=None):
    global user_text
    if user_text == "":
        return
    try:
        # TODO generating infinite files if one exists or show it exists and options to choose 
        f = open('writeups.txt', 'r')
    except FileNotFoundError:
        f = open('writeups.txt', 'w')
        f.write(user_text)
        user_text = ""
        return
    else:
        cont = f.read()
        if cont == "":
            text_to_write = user_text
        # TODO -> check if text is the same? Can use an identifier when built as OOP
        else:
            text_to_write = f'\n{user_text}'

        with open('writeups.txt', 'a') as f:
            f.write(exit_combo_remove(text_to_write))
            # user_text += "\n"
    finally:
        return


# -----------------------------------------------------------------------------------------
# UI SETUP
# -----------------------------------------------------------------------------------------

BORDER = "#3C2C3E"
FG = 'white'
BG = "#000000"

FONT_FAMILY1 = 'Calibri'
FONT_FAMILY2 = 'Helvetica'

FONT_SIZE1 = 14
FONT_SIZE2 = 18
FONT_SIZE3 = 24

FONT_STYLE1 = 'normal'
FONT_STYLE2 = 'italic'
FONT_STYLE3 = 'bold'

PARA_FONT = (FONT_FAMILY1, FONT_SIZE1, FONT_STYLE3)
PARA_FONT2 = (FONT_FAMILY1, 12, FONT_STYLE2)
HEAD_FONT = (FONT_FAMILY2, FONT_SIZE3, FONT_STYLE1)

heading = "WRITE WITH MAGICAL INK"
instruction = "If you don't press any key for 5 seconds, the text you have written will disappear"

window = Tk()
window.title('Vanishink')
window.config(bg=BG, padx=0, pady=0)

heading = Label(text=heading, font=HEAD_FONT, bg=BG, fg=FG, padx=0, pady=0)
instruction = Label(text=instruction, font=PARA_FONT2, fg=FG, bg=BG, pady=0)

typing_area = Text(font=PARA_FONT,  bg=BG, fg=FG, width=100, height=15, wrap='w',
                   highlightcolor=BORDER, highlightthickness=0, highlightbackground=BORDER,
                   padx=0, pady=0, insertbackground="#fff", insertborderwidth=0, insertwidth=10)

typing_area.insert("1.0", "$ ")
# TODO dynamic event generation plz:)
typing_area.event_generate("<<Savingfile>>")
typing_area.event_add('<<Savingfile>>', '<Control-s>')
typing_area.bind('<<Savingfile>>', save_text_to_file)
typing_area.bind('<KeyPress>', start_calculating)

reset_btn = Button(text='Reset', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=reset_app, width=50)

save_btn = Button(text='Save', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=save_text_to_file, width=50)

# heading.grid(row=0, column=0, columnspan=3)
# instruction.grid(row=2, column=0, columnspan=3)
typing_area.grid(row=3, column=0, columnspan=3)
# reset_btn.grid(row=4, column=0)
# save_btn.grid(row=4, column=2)


window.mainloop()
