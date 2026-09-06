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
from htbuilder import div, ul, li, img, b, p


# ============================================================
# DIV TAG
# ============================================================

def create_div_tag(div_string, i):

    dom = div(
        div_string,
        _class=f"div-tag-{i}"
    )

    return str(dom)


def create_list_of_div_tags(div_strings, progress_bar):

    num_cores = max(
        multiprocessing.cpu_count() // 2,
        1
    )

    results = []

    for i, div_string in enumerate(div_strings):

        my_dict = {
            "div_string": div_string,
            "i": i + 1
        }

        results.append(my_dict)

    with WorkerPool(
        n_jobs=num_cores,
        daemon=False
    ) as pool:

        results = pool.map(
            create_div_tag,
            results,
            progress_bar=progress_bar
        )

    return results


# ============================================================
# LI TAG
# ============================================================

def create_li(li_string, i):

    dom = li(
        li_string,
        _class=f"li-tag-{i}"
    )

    return str(dom)


def create_list_of_li_tags(li_strings, progress_bar):

    num_cores = max(
        multiprocessing.cpu_count() // 2,
        1
    )

    results = []

    for i, li_string in enumerate(li_strings):

        my_dict = {
            "li_string": li_string,
            "i": i + 1
        }

        results.append(my_dict)

    with WorkerPool(
        n_jobs=num_cores,
        daemon=False
    ) as pool:

        results = pool.map(
            create_li,
            results,
            progress_bar=progress_bar
        )

    return results


# ============================================================
# BOLD TAG
# ============================================================

def create_bold_tag(bold_string, i):

    dom = b(
        bold_string,
        _class=f"b-tag-{i}"
    )

    return str(dom)


def create_list_of_bold_tags(bold_strings, progress_bar):

    num_cores = max(
        multiprocessing.cpu_count() // 2,
        1
    )

    results = []

    for i, bold_string in enumerate(bold_strings):

        my_dict = {
            "bold_string": bold_string,
            "i": i + 1
        }

        results.append(my_dict)

    with WorkerPool(
        n_jobs=num_cores,
        daemon=False
    ) as pool:

        results = pool.map(
            create_bold_tag,
            results,
            progress_bar=progress_bar
        )

    return results


# ============================================================
# IMAGE TAG
# ============================================================

def create_img_tag(
    img_src,
    i,
    width=None,
    height=None
):

    dom = img(
        src=img_src,
        _class=f"img-tag-{i}"
    )

    dom = (
        dom
        if width is None
        else dom(width=width)
    )

    dom = (
        dom
        if height is None
        else dom(height=height)
    )

    return str(dom)


def create_list_of_img_tags(
    img_srcs,
    progress_bar,
    width=None,
    height=None
):

    num_cores = max(
        multiprocessing.cpu_count() // 2,
        1
    )

    results = []

    for i, img_src in enumerate(img_srcs):

        my_dict = {
            "img_src": img_src,
            "i": i + 1,
            "width": width,
            "height": height
        }

        results.append(my_dict)

    with WorkerPool(
        n_jobs=num_cores,
        daemon=False
    ) as pool:

        results = pool.map(
            create_img_tag,
            results,
            progress_bar=progress_bar
        )

    return results


# ============================================================
# ANY TAG
# ============================================================

def create_any_tag(tag_name, tag_string, i):

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
    title
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

    return html_page


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    tag_names = [

        {
            "div": {
                "p": [
                    "p1",
                 ],
                 "b":{
                    "b":['b1']*10000
                }
            }
        }
        

    ]

    html_page = automate_html_generation(
        tag_names,
        "The world bows at the legends feet. He won the world cup!"
    )

    print(html_page)
