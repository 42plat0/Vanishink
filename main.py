from tkinter import *
import tkinter as Tkinter

from imports.KeyHistory import KeyHistory
from imports.utils.String import String

# -----------------------------------------------------------------------------------------
# LOGIC
# -----------------------------------------------------------------------------------------

# Consts
Tkinter.LAST = "end-1c" # except newline

def get_text_in_area(area : Tkinter.Text, start_line_index: int = 0, char_line_index: int = 2) -> str:
    start_from = str(start_line_index) + "." + str(char_line_index)
    return area.get(start_from, Tkinter.LAST)

# Decorate in future
def vanish(area : Tkinter.Text) -> None:
    """ Clears visual text from text editor """
    def run_vanish():
        # depends on starting symbol
        # Shouldn't it be Editor.displaytext? even though
        if len(String.remove_substring(get_text_in_area(area), Editor.LINE_START)):
            area.delete('1.2')
            window.after(Editor.LINE_CLEAR_MS, run_vanish)
    
    run_vanish()

class TextEditor():
    """ Text editor of Vanishink"""
    LINE_CONSTANT_SYMBOL = "$"
    LINE_AFTER_C_SYMBOL = " "

    LINE_START = f"{LINE_CONSTANT_SYMBOL}{LINE_AFTER_C_SYMBOL}"

    LINE_CLEAR_MS = 30
    
    # Save text as mid point before saving to file on command
    # Probably a file would be better in future
    buffer : str = ""
    display_text : str = ""
    keys : KeyHistory = KeyHistory()

    def set_buffer(self, val: str) -> None:
        self.buffer = val


timer = None

Editor : TextEditor = TextEditor()

DISPLAY_CLEAR_COMBO : str = ["Return"]
WINDOW_EXIT_COMBO : str = "exit"
DELETE_BUTTON : str = "BackSpace" 
SLEEP_TIME : float = 0.1


def start_calculating(event):
    global timer
    
    # Reset timer
    if timer is not None:
        window.after_cancel(timer)

    pressed_key : str = event.keysym

    if String.is_equal(pressed_key, DELETE_BUTTON) and not String.is_empty(Editor.display_text):
        Editor.display_text = Editor.display_text[0 : len(Editor.display_text) - 1]
    elif event.char:                
        # TODO: idea -> by sentences
        Editor.keys.insert(pressed_key)
        Editor.display_text += event.char

    if Editor.keys.is_combination_executed(DISPLAY_CLEAR_COMBO):
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
    Editor.keys.clean()
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
            f.write(String.remove_substring(Editor.buffer, DISPLAY_CLEAR_COMBO))
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

window = Tkinter.Tk()
window.title('Vanishink')
window.config(bg=BG, padx=0, pady=0)

heading = Tkinter.Label(text=heading, font=HEAD_FONT, bg=BG, fg=FG, padx=0, pady=0)
instruction = Tkinter.Label(text=instruction, font=PARA_FONT2, fg=FG, bg=BG, pady=0)

typing_area = Tkinter.Text(font=PARA_FONT,  bg=BG, fg=FG, width=100, height=15, wrap='w',
                   highlightcolor=BORDER, highlightthickness=0, highlightbackground=BORDER,
                   padx=0, pady=0, insertbackground="#fff", insertborderwidth=0, insertwidth=10)

typing_area.insert("1.0", Editor.LINE_START)
# TODO dynamic event generation plz:)
typing_area.event_generate("<<Savingfile>>")
typing_area.event_add('<<Savingfile>>', '<Control-s>')
typing_area.bind('<<Savingfile>>', save_text_to_file)

typing_area.bind('<KeyPress>', start_calculating)

reset_btn = Tkinter.Button(text='Reset', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=reset_app, width=50)

save_btn = Tkinter.Button(text='Save', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=save_text_to_file, width=50)

typing_area.grid(row=3, column=0, columnspan=3)

window.mainloop()
