#################### PARAMETERS
BLUE_SHIRTS_PATH = "./Resources/shirt_dataset/labeled"
UNLABELED_SHIRTS_PATH = "./Resources/shirt_dataset/unlabeled"
OUTPUT_PATH = "./Blue_shirts_detected"
FILE_EXTENSIONS = ["jpg", "jpeg", "png"]
IMGS_PER_ROW = 5
IMG_HEIGHT, IMG_WIDTH = 240, 240
lowerb = [90, 25, 0]
upperb = [125, 255, 255]
AREA_THRESHOLD = 9000

#################### PRINT COLORS
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
GREY = "\x1b[90m"
RESET = "\x1b[0m"


def print_clr(msg, color=RESET):
    print(color + msg + RESET)
