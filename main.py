from tkinter import *

from imports.KeyHistory import KeyHistory
from imports.utils.String import String

# -----------------------------------------------------------------------------------------
# LOGIC
# -----------------------------------------------------------------------------------------
from time import sleep


def vanish(area : Text) -> None:
    """ Clears visual text from text editor """
    # depends on starting symbol
    area.delete('1.2', 'end')

class TextEditor():
    """ Text editor(?) of Vanishink"""
    buffer : str = ""
    display_text : str = ""
    Keys : KeyHistory = KeyHistory()

    def set_buffer(self, val: str) -> None:
        self.buffer = val


timer = None

Editor : TextEditor = TextEditor()

BUFFER_CLEAR_COMBO : str = "jk"
WINDOW_EXIT_COMBO : str = "exit"
SLEEP_TIME : float = 0.1


def start_calculating(event):
    global timer
    
    if timer is not None:
        window.after_cancel(timer)

    pressed_key : str = event.keysym

    print(pressed_key)
    if String.is_equal(pressed_key, "BackSpace") and not String.is_empty(Editor.display_text):
        Editor.display_text = Editor.display_text[0 : len(Editor.display_text) - 1]
        Editor.Keys.remove()
    elif event.char:
        Editor.display_text += event.char
        Editor.Keys.insert(event.char)

    # TODO: idea -> by sentences
    if Editor.Keys.is_combination_executed(BUFFER_CLEAR_COMBO):
        timer = window.after(10, reset_app)
    
    if String.is_equal(Editor.buffer, WINDOW_EXIT_COMBO): 
        close_window()
    
    return

def close_window() -> None:
    window.destroy()
    return

def reset_app():
    global timer
    if not String.is_empty(Editor.buffer):
        Editor.set_buffer(Editor.buffer + "\n")
    Editor.set_buffer(Editor.buffer + Editor.display_text)

    timer = None
    Editor.display_text = ""

    vanish(typing_area)
    Editor.Keys.clean()
    return


def save_text_to_file(e=None):
    if not String.is_empty(Editor.display_text):
        if String.is_empty(Editor.buffer):
            Editor.set_buffer(Editor.display_text)
        else:
            Editor.set_buffer(Editor.buffer + Editor.display_text)

    Editor.display_text = ""

    try:
        # TODO generating infinite files if one exists or show it exists and options to choose 
        f = open('writeups.txt', 'r')
    except FileNotFoundError:
        f = open('writeups.txt', 'w')
        f.write(Editor.buffer)
        return
    else:
        with open('writeups.txt', 'w') as f:
            f.write(String.remove_substring(Editor.buffer, BUFFER_CLEAR_COMBO))
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

typing_area.grid(row=3, column=0, columnspan=3)

window.mainloop()
