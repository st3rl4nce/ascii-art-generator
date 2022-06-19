import cv2, os, argparse

from PIL import Image

from asciifyImg import asciify
from sketchify import skechify

def save_ascii_vid(input, output, s, bg, gs):
    """
        function to convert an video into ASCII art
        inp: input file name - str
        oup: output file name - str
        s: skechify - bool => True: the frames will be skechified and then ascifiied
        bg: background color of ascii art - int => 1:white ,0:black
        gs: grayscale - bool => True: grayscale sketch(pencil like)
        returns output filename - oup
    """
    cap = cv2.VideoCapture(input)
    # extracting frames from video
    ret, frame = cap.read()
    inp = "inp-img.png"
    out = "out-img.png"
    skout = "out-skch.png"
    # copying the frame data into an image
    cv2.imwrite(inp, frame)
    while (os.path.exists(inp)) == False:
        cap = cv2.VideoCapture(input)
        ret, frame = cap.read()
        cv2.imwrite(inp, frame)

    chk = 1

    if s:
        skout=skechify(inp, out, gs)
        asciify(skout, out, bg)
    else:
        asciify(inp, out, bg)
    op = Image.open(out)

    frame_width, frame_height = op.size
    size = (frame_width, frame_height)
    res = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"mp4v"), 15, size)
    osrc = cv2.imread(out)

    res.write(osrc)
    print("frame_count: ")
    while ret:
        print("%d..." % chk)
        ret, frame = cap.read()
        if frame is None:
            break
        cv2.imwrite(inp, frame)
        if s:
            skout=skechify(inp, out, gs)
            asciify(skout, out, bg)
        else:
            asciify(inp, out, bg)
        osrc = cv2.imread(out)
        cv2.imshow("Frame", osrc)
        # writing the asciified/skechified output to video's frames
        res.write(osrc)
        chk += 1
    res.release()
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
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-gs",
        "--pencilsketch",
        help="to make the sketch grayscale(like a pencil sketch)",
        type=bool,
        default=False,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    inp = args.filein
    oup = args.fileout
    bg = args.background
    f = args.skechify
    gs = args.pencilsketch
    ret = save_ascii_vid(inp, oup, f, bg, gs)
    if os.path.exists("inp-img.png"):
        os.remove("inp-img.png")
    if os.path.exists("out-img.png"):
        os.remove("out-img.png")
    print("The video was successfully saved at "+ ret)
