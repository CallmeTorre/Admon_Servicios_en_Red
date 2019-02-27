from PIL import ImageTk, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def _loadPhoto(os_type):
    if 'Darwin' in os_type:
        photo = ImageTk.PhotoImage(file ="./data/images/osx.png")
    elif 'Windows' in os_type:
        photo = ImageTk.PhotoImage(file ="./data/images/windows.png")
    else:
        photo = ImageTk.PhotoImage(file ="./data/images/linux.png")
    return photo
