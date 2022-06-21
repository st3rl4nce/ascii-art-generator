import shutil
import cv2, os, argparse

from PIL import Image

from asciifyImg import asciify
from sketchify import skechify


def save_ascii_vid(input, output, s, bg, gs, rs):
    """
    function to convert an video into ASCII art
    inp: input file name - str
    oup: output file name - str
    s: skechify - int => 1: the frames will be skechified and then ascifiied
    bg: background color of ascii art - int => 1:white ,0:black
    gs: grayscale - int => 1: grayscale sketch(pencil like)
    rs: resolution of the output - int => 1: resizes the output to input resolution, 0: none
    returns output filename - oup
    """

    chk = 1
    dir = "../temp"
    if not os.path.exists(dir):
        os.mkdir(dir)
    # Extracting the frames and asciifying them
    cap = cv2.VideoCapture(input)
    while True:
        inp = "../temp/oup"+str(chk)+".png"
        out = inp
        skout = inp
        print("frame: %d..." % chk)
        ret, frame = cap.read()
        if ret == False:
            break
        if frame is None:
            break
        cv2.imwrite(inp, frame)
        if s==1:
            skout = skechify(inp, out, gs)
            asciify(skout, out, bg, rs)
        else:
            asciify(inp, out, bg, rs)
        chk += 1
    
    # writing the frames to the  video
    ouplist = os.listdir(dir)
    n_f = len(ouplist)
    opchk = Image.open("../temp/"+ouplist[0])
    fw, fh = opchk.size
    size = (fw,fh)
    res = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"mp4v"), 30, size)
    for i in range(n_f):
        name = "oup" + "{:1d}".format(i+1) + ".png"
        path = os.path.join("../temp",name)
        print(path)
        img = cv2.imread(path)
        cv2.imshow("Frame", img)
        res.write(img)
    res.release()
    shutil.rmtree(dir)
    return output


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
    parser.add_argument(
        "-s",
        "--skechify",
        help="flag to set skechify the video",
        type=int,
        default=0,
    )
    parser.add_argument(
        "-gs",
        "--pencilsketch",
        help="to make the sketch grayscale(like a pencil sketch)",
        type=int,
        default=0,
    )
    parser.add_argument(
        "-rs",
        "--resize",
        help="flag to set the resize to source true or false, resize to input: 1, else: 0(default) ",
        type=int,
        default=0,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    inp = args.filein
    oup = args.fileout
    bg = args.background
    f = args.skechify
    gs = args.pencilsketch
    rs=args.resize
    ret = save_ascii_vid(inp, oup, f, bg, gs, rs)
    print("The video was successfully saved at " + ret)
