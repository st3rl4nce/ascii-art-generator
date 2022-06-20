import cv2, argparse
from cv2 import COLOR_BGR2GRAY
from asciifyImg import asciify


def skechify(inp, oup, gs):
    """
    function to convert an image into a sketch
    inp: input file name - str
    oup: output file name - str
    gs: grayscale - int => 1: grayscale sketch(pencil like)
    returns output filename - oup
    """
    img = cv2.imread(inp)
    gray = img
    if gs==1:
        gray = cv2.cvtColor(img, COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv, (111, 111), 0)
    blrinv = cv2.bitwise_not(blur)
    skch = cv2.divide(gray, blrinv, scale=256.0)
    cv2.imwrite(oup, skch)
    return oup


# funciton to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filein", help="File name of the input image.")
    parser.add_argument("fileout", help="File name of the output image.")
    parser.add_argument(
        "-a",
        "--asciify",
        help="flag to set if we want to asciify the result or not, defaults to true",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-bg",
        "--background",
        help="to set background for ascii art(if chosen)",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-gs",
        "--grayscale",
        help="to make the sketch grayscale(like a pencil sketch)",
        type=int,
        default=0,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    inp = args.filein
    oup = args.fileout
    gs = args.grayscale
    bg = args.background
    a = args.asciify
    if a==1:
        trgt = skechify(inp, oup, gs)
        ret = asciify(trgt, oup, bg)
    else:
        ret = skechify(inp, oup, gs)
    print("The file has been succesfully saved at " + ret)
