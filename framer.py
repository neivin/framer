from PIL import Image
from PIL import ImageFont, ImageDraw
import os
from pathlib import Path

# Invariant:
# All images are of the exact same aspect ratio
OUTPUT_SIZE = (1920, 1080)
BACKGROUND_COLOR = (249, 249, 249)  # f9f9f9

TOP_PADDING = 150
BOT_PADDING = 150

def get_resized_dimensions(output_height,
                           original_height, original_width, vert_padding):
    resized_height = output_height - vert_padding

    height_percent = resized_height / float(original_height)
    resized_width = int(float(height_percent) * float(original_width))

    return (resized_width, resized_height)


def write_text(image, xoff, yoff, dim):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    text_to_write = "Nikon L35AF | Kodak Portra 400"

    draw.text((xoff, yoff + dim[1] + 15), text_to_write, font=font, fill=(76, 85, 90))
    return image


def open_and_transform_image(folder, filename):
    im = Image.open(filename)
    image_size = im.size

    print(im.format, im.size, im.mode)
    new_dimensions = get_resized_dimensions(1080, im.size[1], im.size[0], TOP_PADDING + BOT_PADDING)

    print(new_dimensions)

    # copy image and resize to dimensions
    im_to_resize = im.copy()
    im_to_resize = im.resize(new_dimensions)

    x_offset = int(OUTPUT_SIZE[0] / 2 - new_dimensions[0] / 2)
    y_offset = TOP_PADDING

    # new blank image
    outputImage = Image.new(im.mode, OUTPUT_SIZE, BACKGROUND_COLOR)

    # Paste in the resized image
    outputImage.paste(im_to_resize, (x_offset, y_offset))
    # outputImage = write_text(outputImage, x_offset, y_offset, new_dimensions)

    if not os.path.exists(Path(folder) / "out"):
        os.makedirs(Path(folder) / "out")

    outfile_name = "framed_" + Path(filename).name
    output_path = Path(folder) / "out" / outfile_name
    outputImage.save(str(output_path))


def main(folder, extension):
    png_files = [f for f in os.listdir(folder) if f.endswith(extension)]

    for file in png_files:
        filepath = Path(folder) / file
        open_and_transform_image(folder, filepath)
        print("Success! Framed " + file)



if __name__ == "__main__":
    print(os.getcwd())
    PHOTO_FOLDER_PATH = Path("D:/Videos/palm_springs/final_photos")
    main(PHOTO_FOLDER_PATH, ".png")
