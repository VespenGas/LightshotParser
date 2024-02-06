# -*- coding: utf-8 -*-

import os
import requests
import secrets
from bs4 import BeautifulSoup
import time
import validators

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

def create_dir(dirname:str = 'images'):
    pwd = os.getcwd()
    new_dir = os.path.join(pwd, dirname)
    if os.path.isdir(new_dir) == False:
        os.mkdir(path=new_dir)
    return new_dir

def generate_link(suffix = None):
    site_prefix = 'https://prnt.sc/'
    if suffix == None:
        site_suffix = secrets.randbelow(1000000)
    else:
        assert isinstance(suffix, int), 'Suffix should be a 6-digit number - not a number'
        assert len(str(suffix))==6, 'Suffix should be a 6-digit number - more/less than 6 digits'
        site_suffix = suffix
    site_link = ''.join([site_prefix, str(site_suffix)])
    return site_link

def get_img_link(link:str):
    global UserAgent
    with requests.Session():
        page = requests.get(link, headers={'User-Agent': UserAgent,
                                           'referer': 'https://prnt.sc/'})
        pass
    if page.ok:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        img_link = soup.find(id="screenshot-image", class_="no-click screenshot-image").get('src')
        print(f'Image link: {img_link}')
        if not img_link:
            print('Image not found on the Lightshot page!')
            return 1, 
        img_name = img_link.rpartition('/')[2]
        return img_link, img_name
    elif page.status_code == 403:
        print('Restricted!')
        return 1,
    elif page.status_code == 404:
        print('Page does not exist!')
        return 1,
    else:
        print('Unknown code, maybe redirect: {page.status_code} for {link}')
        return 1,
    
def save_img(img_link:str, img_name:str, new_dir:str):
    print('Accessing image on host...')
    global UserAgent
    with requests.Session():
        if validators.url(img_link) == True:
            img_page = requests.get(img_link, headers={'User-Agent': UserAgent})
        else:
            print('Nonexistant image (broken URL).')
            return 1
        if img_page.ok:
            print('Saving image...')
            with open(os.path.join(new_dir, img_name), 'wb') as img:
                img.write(img_page.content)
            print(f'Saved as {img_name}')
            return 0
        elif img_page.status_code == 404:
            print(f'Image does not exist ({img_page})')
        elif img_page.status_code == 403:
            print('Image forbidden!')
        else:
            print(f'Unknown code (maybe redirect): {img_page.status_code} for {img_link}')
        pass
    pass

def main():
    sleep_time_min = 1
    sleep_time_max = 4
    #min and max inter-cycle timeouts
    max_iter = 10000000
    #how many image pages will be processed
    reverse_order = True
    reverse = 1 if reverse_order == False else -1
    print('Scraping started')
    img_dir = create_dir('imgs_end' if reverse_order == True else 'imgs')
    suffixes = list(range(100000, min(100000+max_iter, 1000000)))[::reverse]
    for suffix in suffixes:
        site_link = generate_link(suffix=suffix)
        print(site_link)
        img_link, img_name = get_img_link(site_link)
        save_img(img_link, img_name, img_dir)
        print('Cycle complete, timeout waiting...')
        time.sleep(secrets.randbelow(sleep_time_max)+sleep_time_min)
    print('Done!')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())




