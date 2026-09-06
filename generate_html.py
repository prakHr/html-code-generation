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

from htbuilder import div, ul, li, img, b, p, h1


# ============================================================
# TAG FUNCTIONS
# ============================================================

TAG_FUNCTIONS = {
    "div": div,
    "ul": ul,
    "li": li,
    "img": img,
    "b": b,
    "p": p,
    "h1": h1,
}


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

    if width is not None:
        dom = dom(width=width)

    if height is not None:
        dom = dom(height=height)

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
# GENERIC TAG CREATION
# ============================================================

def create_any_tag(tag_name, tag_string, i):

    if tag_name not in TAG_FUNCTIONS:

        raise ValueError(
            f"Unsupported HTML tag: {tag_name}"
        )

    tag_function = TAG_FUNCTIONS[tag_name]

    dom = tag_function(
        tag_string,
        _class=f"{tag_name}-tag-{i}"
    )

    return str(dom)


# ============================================================
# RECURSIVE TAG CREATION
# ============================================================

def create_recursive_tags(
    tag_name,
    content,
    counter=None
):

    """
    Recursively creates HTML tags.

    Supported structures:

    1. Simple list

        {
            "div": ["Hello1", "Hello2"]
        }

    2. Nested dictionary

        {
            "p": {
                "h1": ["Heading1"]
            }
        }

    3. Multiple nested levels

        {
            "div": {
                "section": {
                    "article": {
                        "p": {
                            "b": ["Hello"]
                        }
                    }
                }
            }
        }

    """

    # --------------------------------------------------------
    # Initialize counter
    # --------------------------------------------------------

    if counter is None:
        counter = {}


    # ========================================================
    # CASE 1:
    #
    # content is a LIST
    #
    # Example:
    #
    # "div": ["Hello1", "Hello2"]
    # ========================================================

    if isinstance(content, list):

        results = []

        for item in content:

            counter[tag_name] = (
                counter.get(tag_name, 0) + 1
            )

            results.append(
                create_any_tag(
                    tag_name,
                    item,
                    counter[tag_name]
                )
            )

        return results


    # ========================================================
    # CASE 2:
    #
    # content is a DICTIONARY
    #
    # Example:
    #
    # "p": {
    #     "h1": ["Heading1"]
    # }
    # ========================================================

    elif isinstance(content, dict):

        child_html = []

        for child_tag_name, child_content in content.items():

            child_html.extend(
                create_recursive_tags(
                    child_tag_name,
                    child_content,
                    counter
                )
            )


        # Increment parent tag counter

        counter[tag_name] = (
            counter.get(tag_name, 0) + 1
        )


        # Create parent containing
        # all generated child HTML

        return [
            create_any_tag(
                tag_name,
                "".join(child_html),
                counter[tag_name]
            )
        ]


    # ========================================================
    # CASE 3:
    #
    # content is a STRING / primitive
    #
    # Example:
    #
    # "div": "Hello"
    # ========================================================

    else:

        counter[tag_name] = (
            counter.get(tag_name, 0) + 1
        )

        return [
            create_any_tag(
                tag_name,
                str(content),
                counter[tag_name]
            )
        ]


# ============================================================
# CREATE ALL TAGS
# ============================================================

def create_list_of_any_tags(tag_names):

    results = []

    counter = {}


    for tag_dict in tag_names:

        for tag_name, content in tag_dict.items():

            results.extend(
                create_recursive_tags(
                    tag_name,
                    content,
                    counter
                )
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


    html_page = create_complete_html_page(
        title,
        "".join(created_tags)
    )


    return html_page


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    tag_names = [

        {
            "div": [
                "Hello1",
                "Hello2"
            ],

            "p": {

                "h1": [
                    "Heading1"
                ]*100

            }
        }

    ]


    html_page = automate_html_generation(
        tag_names,
        "Test Page"
    )


    print(html_page)
