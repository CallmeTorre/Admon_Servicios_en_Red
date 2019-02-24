from PIL import ImageTk, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def _loadPhoto(os_type):
    if os_type == 'Darwin':
        photo = ImageTk.PhotoImage(file ="./data/images/osx.png")
    elif os_type == 'Windows':
        photo = ImageTk.PhotoImage(file ="./data/images/windows.png")
    else:
        photo = ImageTk.PhotoImage(file ="./data/images/linux.png")
    return photo
