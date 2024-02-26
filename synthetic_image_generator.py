from PIL import Image
import glob
import os
import random

import pprint
pp = pprint.PrettyPrinter()
import json

# object_classes = ["LIKE", "DISLIKE", "STAR", "TSON", "AD", "ADLOADER"]
object_classes = ["CHECKBOX", "FIRE", "BOMB"]

def generate_image_and_annotation(background_img, foreground_img, image_id, result):
    print(0)
    # read images
    img1 = Image.open(background_img)
    img2 = Image.open(foreground_img).convert("RGBA")
    # img1.show()

    # filename processing
    basename_without_ext_background_img = os.path.splitext(os.path.basename(background_img))[0]
    basename_without_ext_foreground_img = os.path.splitext(os.path.basename(foreground_img))[0]
    filename = basename_without_ext_background_img + "_" + basename_without_ext_foreground_img

    # extract class name
    object_class = basename_without_ext_foreground_img.split("_")[0]

    # random anchor position in background UI
    background_img_width, background_img_height = img1.size

    x = random.randint(64, background_img_width - 65)
    y = random.randint(64, background_img_height - 65)

    # random width/height of foreground objects
    # class_id center_x center_y width height
    resized_width = random.randint(16, 64)
    resized_height = random.randint(16, 64)
    size = (resized_width, resized_height)
    img2 = img2.resize(size, Image.ANTIALIAS)

    category = object_classes.index(object_class)
    x_center = (x + resized_width/2)/background_img_width
    y_center = (y + resized_height/2)/background_img_height
    wid = resized_width/background_img_width
    hei = resized_height/background_img_height

    yolo_txt = f"{category} {x_center} {y_center} {wid} {hei}"
    # generate superimposed UI
    # xmin and ymin
    img1.paste(img2, (x,y), img2)

    # random > 0.8 = test else train
    random_number = random.random()
    location = ""
    if random_number > 0.8:
        img1.save("output/images/test/" + object_class + "/" + filename + ".png","PNG")
        with open("output/images/test/" + object_class + "/" + filename + ".txt", 'w') as file:
            # Write content to the file
            file.write(yolo_txt)
    else:
        img1.save("output/images/train/" + object_class + "/" + filename + ".png","PNG")
        with open("output/images/train/" + object_class + "/" + filename + ".txt", 'w') as file:
            # Write content to the file
            file.write(yolo_txt)

    # # populating result["images"]
    # image = {}
    # image["width"] = background_img_width
    # image["height"] = background_img_height
    # image["id"] = image_id
    # image["file_name"] = "images/" + filename + ".png"
    # result["images"].append(image)

    # # populating result["annotations"]
    # annotation = {}
    # annotation["id"] = image_id
    # annotation["image_id"] = image_id
    # annotation["category_id"] = object_classes.index(object_class)
    # annotation["segmentation"] = []
    # annotation["bbox"] = [x, y, resized_width, resized_height]
    # annotation["ignore"] = 0
    # annotation["iscrowd"] = 0
    # annotation["area"] = resized_width * resized_height
    # result["annotations"].append(annotation)

def generate_synthetic_dataset():
    print(1)
    object_files = [file for file in glob.glob("C:/Users/91998/Downloads/DarkPatterns/dp_images/" + "*.*")]
    print(len(object_files))
    object_files.sort()
    # print("object_files: ", object_files)
    ui_files = [file for file in glob.glob("C:/Users/91998/Downloads/AidUI-Evaluation-Dataset/evaluation_dataset/web/images/" + "*.*")]
    print(len(ui_files))
    ui_files.sort()
    # print("ui_files: ", ui_files)

    # dictionary for image annotations
    result = {
        "images": []
        , "categories": []
        , "annotations": []
        , "info": {
            "year": 2024
            , "version": "1.0"
            , "contributor": "Label Studio"
        }}

    # populating result["categories"]
    for i in range(len(object_classes)):
        result["categories"].append({"id": i, "name": object_classes[i]})

    # generate superimposed UIs and annotations
    image_id = 0
    for i in range(len(object_files)):
        for j in range(len(ui_files)):
            if object_files[i][:2] != "._":
                foreground_img = object_files[i]
                background_img = ui_files[j]
                generate_image_and_annotation(background_img, foreground_img, image_id, result)
                print("done: ", image_id)
                image_id += 1
    # print image annotation result
    # pp.pprint(result)
    # write image annotation result
    with open('./output/result.json', 'w') as fp:
        json.dump(result, fp)

generate_synthetic_dataset()