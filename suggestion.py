import tkinter as tk
from pynput import keyboard

from logic import get_suggestions

# Rolling input buffer
input_buffer = ''

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
    suggestions = get_suggestions(input_buffer)
    if suggestions:
        label.config(text="\n".join(suggestions))
        root.deiconify()
    else:
        root.withdraw()

# Keyboard event handler
def on_press(key):
    global input_buffer
    try:
        if key.char.isalnum():
            input_buffer += key.char
        elif key.char == ' ':
            input_buffer = ''  # Reset on space //need to implement caching
    except AttributeError:
        if key == keyboard.Key.backspace:
            input_buffer = input_buffer[:-1]
        elif key == keyboard.Key.space:
            input_buffer = ' '
        elif key == keyboard.Key.enter:
            input_buffer = ''
        else:
            return

    update_suggestions()

# Start keyboard listener in background
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Run UI loop (non-blocking keyboard thread)
root.mainloop()
