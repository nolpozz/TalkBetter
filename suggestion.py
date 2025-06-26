import tkinter as tk
from pynput import keyboard

from logic import get_suggestions, get_word_score

# Rolling input buffer
input_buffer = ''
sentence_buffer = ''

# Tkinter UI setup
root = tk.Tk()
root.overrideredirect(True)  # No window decorations 
root.wm_attributes("-topmost", True)  # Always on top
root.geometry("+100+100")  # Position
label = tk.Label(root, text="", justify="left", bg="white", fg="black", font=("Arial", 12), anchor="w", relief="solid", bd=1, padx=5, pady=3)
label.pack()
root.withdraw()  # Hide initially

# Update UI with new suggestions 
def update_suggestions():
    word_score = get_word_score(input_buffer)
    if word_score is None:
        print("word score none")
        word_score = 0
    suggestions = get_suggestions(input_buffer)
    if suggestions:
        formatted = [f"{word} ({word_score - float(score):.2f})" for word, score in suggestions]
        label.config(text="\n".join(formatted))
        root.deiconify()
    else:
        root.withdraw()


# Keyboard event handler
def on_press(key):
    global input_buffer
    global sentence_buffer
    try:
        if key.char.isalnum():
            sentence_buffer += key.char
            input_buffer += key.char
        elif key.char == ' ':
            input_buffer = ''  # Reset on space //need to implement caching
            sentence_buffer += key.char
        elif key.char == '.':
            input_buffer = ''
            sentence_buffer = ''
    except AttributeError:
        if key == keyboard.Key.backspace:
            if(input_buffer != ''):
                input_buffer = input_buffer[:-1]
            else:
                input_buffer = ''
            if(sentence_buffer != ''):
                sentence_buffer = sentence_buffer[:-1]
            else:
                sentence_buffer = ''
        elif key == keyboard.Key.space:
            input_buffer = ''
            sentence_buffer += ' '
        elif key == keyboard.Key.enter:
            input_buffer = ''
            sentence_buffer = ''
        else:
            return

    update_suggestions()

# Start keyboard listener in background wh
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Run UI loop (non-blocking keyboard thread)
root.mainloop()
