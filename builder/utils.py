from collections import defaultdict
from Page import Page
import os
import re
import shutil



def cp_rsc() -> None:
    shutil.copytree("builder/site/rsc", "dist/rsc", dirs_exist_ok=True)
    shutil.copyfile("builder/site/index.html", "dist/index.html")
    shutil.copyfile("builder/site/CNAME", "dist/CNAME")
    for item in os.listdir("builder/site/favicon"):
        s = os.path.join("builder/site/favicon", item)
        d = os.path.join("dist", item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)


def get_all_path() -> list[str]:
    res = []
    for root, _, files in os.walk("pages"):
        if len(files) == 0:
            continue
        deep =  len(root.split(os.sep)) -1
        if deep != 2:
            raise ValueError(f"Invalid path depth '{root}' : pages should contains exactly 2 sub directories ( pages/{{tech}}/{{title}} ) but get '{deep}'")
        files_nb = len(files)
        if files_nb != 1:
            raise ValueError(f"Invalid files number in 'pages/{root}' : must contains exactly 1 file ({{id}}.md) but get '{files_nb}'")
        res.append( re.sub(r"^pages/", "", root ))
    return  res


def get_free_ids(pages: list[Page]) -> list[str]:
    """
    Get all free ids regarding given pages
    """
    existing_ids = set(obj.id for obj in pages)
    return [
        f"{i:05d}" for i in range(100000)
        if f"{i:05d}" not in existing_ids
    ]


def check_id_dups(pages: list[Page]) -> None:
    """
    Check that there is no duplicated id in given pages
    """
    by_id = defaultdict(list)
    for obj in pages:
        by_id[obj.id].append(obj)
    duplicates = [(id_, objs) for id_, objs in by_id.items() if len(objs) > 1]
    if len(duplicates) != 0:
        msg = ""
        for id_,pages in duplicates:
            msg += f"\033[33m{id_} :\033[0m\n"
            for page in pages:
                msg += f"  - {page.pages_path}\n"

        free_ids = get_free_ids(pages)
        msg += f"\033[35mSome free ids :\033[0m\n"
        for i in range(len(duplicates)):
            print(f"  - {free_ids[i]}")

        raise ValueError(f"Duplicates ids found :\n{msg}")

