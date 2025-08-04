import json
import argparse
from pathlib import Path
from Page import Page
import utils


def main() -> None:
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true', help='build all site')
    group.add_argument('--page', type=str, metavar='"pages/<category>/<name>"', help='build only the specified page')

    args = parser.parse_args()

    with open("builder/site/page.mustache", "r", encoding="utf-8") as f:
        template = f.read()

    try:
        if args.all:
            print("\033[34mParsing Pages/ \033[0m")
            pages = [Page.from_path(p) for p in utils.get_all_path()]
            print(f"\033[32m{len(pages)} pages parsed\033[0m")

            print("\033[34m\nChecking ids\033[0m")
            utils.check_id_dups(pages)
            print("\033[32mok\033[0m")

            print("\n\033[34mBuilding Pages\033[0m")
            for p in pages:
                p.build(template)
            print("\033[32mBuilt\033[0m")

            indexation = [ {"id":p.id,"title": p.title,"tech": p.tech} for p in pages ]
            Path("dist/indexation.js").write_text("const indexation = " + json.dumps(indexation,indent=2))

            print("\n\033[34mCopy rsc/\033[0m")
            utils.cp_rsc()
            print("\033[32mCopied\033[0m")
            return

        elif args.page:
            page = Page.from_path(args.page)
            page.build(template)

            print("\n\033[34mCopy rsc/\033[0m")
            utils.cp_rsc()
            print("\033[32mCopied\033[0m")

            print(f"\nfile://{page.dist_path.absolute()}")
            return

    except FileNotFoundError as e:
        print("\033[31mError:\033[0m")
        print(e)
    except ValueError as e:
        print("\033[31mError:\033[0m")
        print(e)

main()