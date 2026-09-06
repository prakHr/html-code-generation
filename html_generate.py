import mpire
import os
os.environ["OMP_NUM_THREADS"] = "1"
import time
import multiprocessing 
from mpire import WorkerPool
from pprint import pprint
import itertools
import shutil
import random
from multiprocessing import Manager
from htbuilder import div
from htbuilder import div, ul, li, img, b

def create_div_tag(div_string,i):
    dom = div(div_string,_class=f"div-tag-{i}")
    return str(dom)

def create_list_of_div_tags(div_strings,progress_bar):
    num_cores = max(multiprocessing.cpu_count()//2,1)
    results = []
    for i, div_string in enumerate(div_strings):
        my_dict = {
            "div_string": div_string,
            "i": (i+1)
        }
        results.append(my_dict)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(create_div_tag, results, progress_bar=progress_bar)
    return results

def create_li(li_string,i):
    dom = li(li_string,_class=f"li-tag-{i}")
    return str(dom)


def create_list_of_li_tags(li_strings,progress_bar):
    num_cores = max(multiprocessing.cpu_count()//2,1)
    results = []
    for i, li_string in enumerate(li_strings):
        my_dict = {
            "li_string": li_string,
            "i":(i+1)
        }
        results.append(my_dict)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(create_li, results, progress_bar=progress_bar)
    return results

def create_bold_tag(bold_string,i):
    dom = b(bold_string,_class=f"b-tag-{i}")
    return str(dom)

def create_list_of_bold_tags(bold_strings,progress_bar):
    num_cores = max(multiprocessing.cpu_count()//2,1)
    results = []
    for i, bold_string in enumerate(bold_strings):
        my_dict = {
            "bold_string": bold_string,
            "i":(i+1)
        }
        results.append(my_dict)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(create_bold_tag, results, progress_bar=progress_bar)
    return results

def create_img_tag(img_src,i,width=None,height=None):
    dom = img(src=img_src,_class=f"img-tag-{i}")
    dom = dom if width is None else dom(width=width)
    dom = dom if height is None else dom(height=height)
    return str(dom)

def create_list_of_img_tags(img_srcs,progress_bar,width=None,height=None):
    num_cores = max(multiprocessing.cpu_count()//2,1)
    results = []
    for i, img_src in enumerate(img_srcs):
        my_dict = {
            "img_src": img_src,
            "i":(i+1),
            "width": width,
            "height": height
        }
        results.append(my_dict)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(create_img_tag, results, progress_bar=progress_bar)
    return results  


def create_any_tag(tag_name,tag_string,i):
    dom = eval(f"{tag_name}(tag_string,_class=f'{tag_name}-tag-{i}')")
    return str(dom)

def create_list_of_any_tags(tag_names,tag_strings,progress_bar):
    num_cores = max(multiprocessing.cpu_count()//2,1)
    results = []
    for i in range(len(tag_names)):
        my_dict = {
            "tag_name": tag_names[i],
            "tag_string": tag_strings[i],
            "i":(i+1)
        }
        results.append(my_dict)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(create_any_tag, results, progress_bar=progress_bar)
    return results

def create_complete_html_page(title,body_content):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        {body_content}
    </body>
    </html>
    """
    return html

def automate_html_generation(tag_names, tag_strings, title, progress_bar=True):
    created_tags = create_list_of_any_tags(tag_names, tag_strings, progress_bar)
    html_page = create_complete_html_page(title, "".join(created_tags))
    return html_page   

if __name__ == "__main__":
    tag_names = ["div", "li", "b", "img"]
    tag_strings = ["Hello", "World", "This", "Is", "A", "Test"]
    progress_bar = True 
    html_page = automate_html_generation(tag_names, tag_strings, "Test Page", progress_bar)
    print(html_page)