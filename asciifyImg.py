import cv2, argparse
import numpy as np

from PIL import Image, ImageDraw, ImageOps, ImageFont

# Characters used for Mapping to Pixels
Character = {
    "standard": "@%#*+=-:. ",
    "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
}

# function to get the essential data
def get_data(mode):
    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=20)
    scale = 2
    char_list = Character[mode]
    return char_list, font, scale


def asciify(inp, oup, bg):
    """
    function to convert an image into ASCII art
    inp: input file name - str
    oup: output file name - str
    bg: background color of ascii art - int => 1:white ,0:black
    returns output filename - oup
    """
    # Making Background Black or White
    if bg == 1:
        bg_code = (255, 255, 255)
    elif bg == 0:
        bg_code = (0, 0, 0)
    # Reading Input Image
    image = cv2.imread(inp)

    # Extracting height and width from Image
    height, width, _ = image.shape

    # Getting the character List, Font and Scaling characters for square Pixels
    char_list, font, scale = get_data("complex")
    num_chars = len(char_list)
    # num_cols =
    num_cols = 300

    # Defining height and width of each cell==pixel
    cell_w = width / num_cols
    cell_h = scale * cell_w
    num_rows = int(height / cell_h)

    # Calculating Height and Width of the output Image
    char_width, char_height = font.getsize("A")
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows

    # Making a new Image using PIL
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    # changing the color scheme to match with that of PIL(opencv: BGR to PIL: RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # mapping for rgb
    for i in range(num_rows):
        for j in range(num_cols):
            partial_image = image[
                int(i * cell_h) : min(int((i + 1) * cell_h), height),
                int(j * cell_w) : min(int((j + 1) * cell_w), width),
                :,
            ]
            partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (
                cell_h * cell_w
            )
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            line = char_list[
                min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)
            ]
            draw.text(
                (j * char_width, i * char_height),
                line,
                fill=partial_avg_color,
                font=font,
            )

    # Inverting Image and removing excess borders
    if bg == 1:
        cropped_image = ImageOps.invert(out_image).getbbox()
    elif bg == 0:
        cropped_image = out_image.getbbox()

    # Saving the new Image
    out_image = out_image.crop(cropped_image)
    out_image.save(oup)
    return oup


# funciton to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filein", help="File name of the input image.")
    parser.add_argument("fileout", help="File name of the output image.")
    parser.add_argument(
        "-bg",
        "--background",
        help="flag to set the background color of ascii, white: 1, black: 0",
        type=int,
        default=1,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    inp = args.filein
    oup = args.fileout
    bg = args.background  # optional defaults to white
    ret = asciify(inp, oup, bg)
    print("The file has been succesfully saved at " + ret)
