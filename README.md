
![](rsc/banner.png)

A collection of cheat sheets and technical guides, focused on useful content, not just condensed documentation.

- Focus only on the most useful, practical, and concise information.
- Let the community contribute and review the content.
- centrilise with 1 entrypoint all your needs

<br><br>

# 📝 Add A Cheat Sheet

### Standard
All cheat sheets are based on a `{id}.md` files under `pages/`. So adding a cheat sheet on the site is simply adding a `{id}.md` file in sources.

pages muste follow a specifc path :
```
pages/{tech}/{title}/{id}.md
```
- `{tech}` technology name. Only a-z, A-Z, 0-9, - chars, and starts with uppercase (`[A-Z][a-zA-Z0-9-+]*`)
- `{title}` cheat sheet page title. Only space, a-z, A-Z, 0-9, -, _, [], () chars, and starts with uppercase (`[A-Z][a-zA-Z0-9-_ \[\]\(\)]*`)
- `{id}` must be a unique random alphanumeric 6 chars long word


### How

Whether you're adding a new cheat sheet or improving an existing one:

1. Fork the repository
2. Add or modify a page in the pages/ folder
3. (use cli to check the build of your page locally)
4. Create a Pull Request

<br><br>

# 🔧 CLI
the site building script is exposed has cli, allowing you to locally build the site to test your pages

#### Install dependencies
- make sure you have python3 and pip
- be sure to be on the project root
- ```shell
  pip install -r builder/requirements.txt
  ```

#### Build
```shell
# build all site
python builder/cheat-sheet.py --all

# build only home page and a specific pages/{tech}/{title}
python builder/cheat-sheet.py --page {tech}/{title}
```

