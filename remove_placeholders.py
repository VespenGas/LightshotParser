# -*- coding: utf-8 -*-

#Written by: VespenGas
#Use this function to remove imgur placeholders in given lib

import os
import pathlib

folder_name = 'imgs_end'

def main():
    global folder_name
    
    with open('placeholder1.png', 'rb') as placeholder:
        placeholder_content = placeholder.read()
    
    
    assert os.path.isdir(folder_name)
    dir_path = os.path.join(os.getcwd(), folder_name)
    image_list = list(pathlib.Path(dir_path).glob('*'))
    
    for image_path in image_list:
        with open(str(image_path), 'rb') as image:
            image_content = image.read()
        if image_content == placeholder_content:
            os.remove(image_path)
    return 0
if __name__ == '__main__':
    main()
