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
from htbuilder import html,head,title,base,link,meta,style,body,header,nav,main,section,article,aside,footer,address,h1,h2,h3,h4,h5,h6,p,br,hr,pre,blockquote,div,span,a,abbr,b,bdi,bdo,cite,code,data,dfn,em,i,kbd,mark,q,rp,rt,ruby,s,samp,small,strong,sub,sup,time,u,var,wbr,img,audio,video,source,track,picture,map,area,iframe,embed,object,param,canvas,script,noscript,template,ol,ul,li,dl,dt,dd,table,caption,colgroup,col,tbody,thead,tfoot,tr,th,td,form,textarea,button,select,option,optgroup,label,fieldset,legend,datalist,output,progress,meter,details,summary,dialog,figure,figcaption,ins,search,menu

def create_any_tag(
    tag_name,
    tag_string,
    i,
    **attributes
):

    if tag_name == "img":

        dom = img(
            src=attributes.get("src"),
            width=attributes.get("width"),
            height=attributes.get("height"),
            _class=f"{tag_name}-tag-{i}"
        )

    else:

        dom = eval(
            f"{tag_name}("
            f"tag_string,"
            f"_class=f'{tag_name}-tag-{i}'"
            f")"
        )

    return str(dom)
# ============================================================
# CREATE TAG LIST
# ============================================================

def create_tag_list(tag_name, tag_content):

    results = []

    # --------------------------------------------------------
    # CASE 1
    #
    # tag_content is a list
    #
    # Example:
    #
    # "p": ["p1", "p2"]
    # --------------------------------------------------------

    if isinstance(tag_content, list):

        for i, tag_string in enumerate(
            tag_content,
            start=1
        ):

            my_dict = {
                "tag_name": tag_name,
                "tag_string": tag_string,
                "i": i
            }

            results.append(my_dict)

        return results


    # --------------------------------------------------------
    # CASE 2
    #
    # tag_content is a dictionary
    #
    # Example:
    #
    # "div": {
    #     "p": ["p1", "p2"]
    # }
    # --------------------------------------------------------

    elif isinstance(tag_content, dict):

        child_results = []

        for child_tag_name, child_tag_content in tag_content.items():

            child_results.extend(
                create_tag_list(
                    child_tag_name,
                    child_tag_content
                )
            )

        return child_results


    # --------------------------------------------------------
    # CASE 3
    #
    # Single string
    # --------------------------------------------------------

    else:

        my_dict = {
            "tag_name": tag_name,
            "tag_string": str(tag_content),
            "i": 1
        }

        results.append(my_dict)

        return results


# ============================================================
# RECURSIVE HTML CREATION
# ============================================================

def create_recursive_html(
    tag_name,
    tag_content,
    counter=None
):

    if counter is None:
        counter = {}


    # ========================================================
    # SPECIAL CASE: IMG
    # ========================================================

    if tag_name == "img" and isinstance(tag_content, dict):

        results = []

        for img_name, img_data in tag_content.items():

            if not isinstance(img_data, dict):
                continue

            counter[tag_name] = (
                counter.get(tag_name, 0) + 1
            )

            results.append(
                create_any_tag(
                    tag_name,
                    "",
                    counter[tag_name],
                    src=img_data.get("src"),
                    width=img_data.get("width"),
                    height=img_data.get("height")
                )
            )

        return results


    # ========================================================
    # LIST
    #
    # Example:
    #
    # "p": ["p1", "p2"]
    # ========================================================

    if isinstance(tag_content, list):

        results = []

        for tag_string in tag_content:

            counter[tag_name] = (
                counter.get(tag_name, 0) + 1
            )

            results.append(
                create_any_tag(
                    tag_name,
                    tag_string,
                    counter[tag_name]
                )
            )

        return results


    # ========================================================
    # DICTIONARY
    #
    # Example:
    #
    # "div": {
    #     "p": ["p1", "p2"]
    # }
    # ========================================================

    elif isinstance(tag_content, dict):

        child_html = []

        for child_tag_name, child_tag_content in tag_content.items():

            child_html.extend(
                create_recursive_html(
                    child_tag_name,
                    child_tag_content,
                    counter
                )
            )

        counter[tag_name] = (
            counter.get(tag_name, 0) + 1
        )

        parent_html = create_any_tag(
            tag_name,
            "".join(child_html),
            counter[tag_name]
        )

        return [parent_html]


    # ========================================================
    # STRING
    # ========================================================

    else:

        counter[tag_name] = (
            counter.get(tag_name, 0) + 1
        )

        return [
            create_any_tag(
                tag_name,
                str(tag_content),
                counter[tag_name]
            )
        ]
# ============================================================
# CREATE LIST OF ANY TAGS - LEVEL 1
# ============================================================

def create_list_of_any_tags_1(my_dicts):
    my_dict = my_dicts

    results = []

    counter = {}

    for tag_name, tag_content in my_dict.items():

        results.extend(
            create_recursive_html(
                tag_name,
                tag_content,
                counter
            )
        )

    return results


# ============================================================
# CREATE LIST OF ANY TAGS - LEVEL 2
# ============================================================

def create_list_of_any_tags_2(tag_names):

    num_cores = max(
        multiprocessing.cpu_count() // 2,
        1
    )

    results = []

    for my_dict in tag_names:

        results.append(
            {
                "my_dicts": my_dict
            }
        )

    with WorkerPool(
        n_jobs=num_cores,
        daemon=False
    ) as pool:

        results = pool.map(
            create_list_of_any_tags_1,
            results,
            progress_bar=True
        )

    return results


# ============================================================
# CREATE LIST OF ANY TAGS
# ============================================================

def create_list_of_any_tags(tag_names):

    results = create_list_of_any_tags_2(
        tag_names
    )

    return results


# ============================================================
# COMPLETE HTML PAGE
# ============================================================

def create_complete_html_page(
    title,
    body_content
):

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


# ============================================================
# AUTOMATE HTML GENERATION
# ============================================================

def automate_html_generation(
    tag_names,
    title,
    num_of_html_pages
):

    created_tags = create_list_of_any_tags(
        tag_names
    )

    rv = []

    for create_tag in created_tags:

        rv += create_tag

    html_page = create_complete_html_page(
        title,
        "".join(rv)
    )
    
    html_pages = []
    for i in range(num_of_html_pages):
        html_pages.append(html_page)
    return html_pages


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    tag_names = [

        {
            "div": {
                "p": [
                    "p1",
                ]*1000,

                "b": {
                    "b": [
                        "b1"
                    ],

                    "b": [
                        "b2"
                    ],

                    "h1": [
                        "h1"
                    ]
                },

                "img": {
                    "img1": {
                        "src": "image1.jpg",
                        "width": 500,
                        "height": 300
                    },

                    "img2": {
                        "src": "image2.jpg",
                        "width": 800,
                        "height": 600
                    }
                }
            }
        }

    ]
    html_pages = automate_html_generation(
        tag_names,
        "From a boy with a dream!",
        int(pow(10,6))
    )
    print((html_pages)[0])
