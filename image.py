from PIL import Image
import screeninfo

def crop_to_aspect_ratio(image, aspect_ratio):
    # Calculate dimensions of the crop box
    image_ratio = image.width / image.height
    if image_ratio > aspect_ratio:
        crop_width = int(image.height * aspect_ratio)
        crop_height = image.height
    else:
        crop_width = image.width
        crop_height = int(image.width / aspect_ratio)
    
    # Calculate center coordinates
    center_x = image.width // 2
    center_y = image.height // 2
    
    # Calculate crop box coordinates
    left = max(0, center_x - crop_width // 2)
    upper = max(0, center_y - crop_height // 2)
    right = min(image.width, left + crop_width)
    lower = min(image.height, upper + crop_height)
    
    # Crop the image
    cropped_image = image.crop((left, upper, right, lower))
    
    return cropped_image

def generateBG(screen, path):
    # screen is actually an array consist of 0 and 1, with index correspond to which display
    # for example: [0, 1] means set wallpaper on display 2, and disable wallpaper on display 1
    
    # get all screen
    screens = screeninfo.get_monitors()
    # check whether screen provided enough info about screens
    if (len(screen) != len(screens)): raise ValueError
    # generate a background for each monitor
    images = []
    for i in range(len(screens)):
        if (screen[i] == 0):
            images.append(Image.new('RGB', (screens[i].width, screens[i].height), (0, 0, 0)))
        elif (screen[i] == 1):
            image = Image.open(path)
            aspect_ratio = int(screens[i].width) / int(screens[i].height)
            cropped = crop_to_aspect_ratio(image, aspect_ratio)
            resized = cropped.resize((int(screens[i].width),  int(screens[i].height)), Image.Resampling.LANCZOS)
            images.append(resized)
    
    # combine all generated background to a single image
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('out.jpg')