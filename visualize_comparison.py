import os
import glob
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# define const
font_path = "./arial.ttf"
prediction1_path = "./last_predicted/"
prediction2_path = "./predicted/"
input_path = "./TestA/"
output_path = "./demo/"
max_image = -1
count_image = 0

files = glob.glob(input_path + "*")

def concatenate(image1, image2):
    ret = Image.new('RGB', (image1.width + image2.width, image1.height))
    ret.paste(image1, (0, 0))
    ret.paste(image2, (image1.width, 0))
    return ret

def drawBbox(box, image):
    font = ImageFont.truetype(font_path, 16)
    pdraw = ImageDraw.Draw(image)
    polygon_pts = []
    for i in range(0, 8, 2):
        polygon_pts.append((int(box[i]), int(box[i + 1])))
    pdraw.polygon(polygon_pts, fill=None, outline=(36, 255, 12, 255))
    pdraw.text(polygon_pts[0], "", (36,255,12), font=font)
    
for file in files:
    
    if (count_image == max_image):
        print("Max image exceeded. Stopped!")
        break
    if (count_image != -1):
        count_image += 1
        
    filename = os.path.basename(file)
    
    f1 = open(prediction1_path + filename + ".txt", "r", encoding="utf8")
    bboxes1 = f1.read()
    f1.close()
    bboxes1 = bboxes1.split("\n")
    
    f2 = open(prediction2_path + filename + ".txt", "r", encoding="utf8")
    bboxes2 = f2.read()
    f2.close()
    bboxes2 = bboxes2.split("\n")
    
    image1 = Image.open(file)
    image2 = Image.open(file)
    
    for bbox in bboxes1:
        box = bbox.split(",")
        if len(box) < 8:
            continue
        drawBbox(box, image1)
    
    for bbox in bboxes2:
        box = bbox.split(",")
        if len(box) < 8:
            continue
        drawBbox(box, image2)

    vis = concatenate(image1, image2)
    vis.save(os.path.join(output_path , filename))