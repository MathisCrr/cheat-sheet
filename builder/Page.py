import chevron
import markdown
import re
import urllib.parse
from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor
from pathlib import Path
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name




# --- Markdown custom parser ---
class CustomCodeBlockPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(r'^\`\`\`(\w+)?\n(.*?)\n\`\`\`', re.MULTILINE | re.DOTALL)

    def run(self, lines: list[str]) -> list[str]:
        text = "\n".join(lines)
        def repl(match: re.Match[str] ) -> str:
            lang = match.group(1) or 'text'
            code = match.group(2)
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(nowrap=False)
            highlighted = highlight(code, lexer, formatter)

            return f"""
<div class="code-block">
    <div class="code-header">
        <p class="language">{lang}</p>
        <div><img class="copy" src="../rsc/assets/copy.svg"></div>
    </div>
    {highlighted}
</div>
"""
        return self.FENCED_BLOCK_RE.sub(repl, text).split('\n')

class CustomCodeBlockExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.preprocessors.register(CustomCodeBlockPreprocessor(md), 'custom_code_block', 25)





# --- Page class ---
class Page:
    id         : str
    tech       : str
    title      : str
    title_url  : str
    pages_path : Path
    dist_path  : Path
    _regex_id = r'[0-9]{5}'


    def __init__(self,tech:str,title:str,id_:str):

        tech_re = r'[A-Z][a-zA-Z0-9-+]*'
        if not re.fullmatch(tech_re, tech):
            raise ValueError(
f"""The page '{tech}/{title}' has invalid tech name ({tech}) :
must match {tech_re} (only a-z, A-Z, 0-9, - chars, and start by uppercase)."""
            )

        title_re = r'[A-Z][a-zA-Z0-9-_ \[\]\(\)]*'
        if not re.fullmatch(title_re, title):
            raise ValueError(
f"""The page \033[36m'{tech}/{title}'\033[0m has invalid title ({title}) :
Must match \033[36m{title_re}\033[0m (only space, a-z, A-Z, 0-9, -, _, [], () chars, and start with uppercase)."""
            )

        if not re.fullmatch(self._regex_id, id_):
            raise ValueError(f"Id '{id_}' ({tech}/{tech}/{id_}) has invalid format : must match '{self._regex_id}'")

        self.tech       = tech
        self.title      = title
        self.title_url  = urllib.parse.quote(self.title)
        self.pages_path = Path(f"pages/{tech}/{title}/{id_}.md")
        self.dist_path  = Path(f"dist/{id_}/index.html")
        self.id = id_

    @classmethod
    def from_path(cls,path:str) -> "Page":
        """
        Creat a Page object from a str path like "{tech}/{title}"
        """

        print(f"parsing '{path}'")
        p = Path(path)

        # check that path is only {category}/{name}
        if len(p.parts) != 2:
            raise ValueError(f"Path must contains 2 elements ('{{category}}/{{name}}'), but '{p}' contains '{len(p.parts)}' element(s).")

        tech, title = p.parts

        # Check that pages/{category}/{name} exist
        abs_path = Path("pages") / p
        if not abs_path.exists():
            raise FileNotFoundError(f"Path '{p}' doesn't exist under 'pages/'.")
        if not abs_path.is_dir():
            raise NotADirectoryError(f"Path '{p}' do not  point to a directory.")

        # Check if the path contains exactly 1 file
        files = [f for f in abs_path.iterdir() if f.is_file()]
        if len(files) != 1:
            raise ValueError(f"Path '{p}' must contains exactly 1 file, but found {len(files)}.")

        # Check file format validity
        file_regex = fr'({cls._regex_id})\.md'
        match = re.fullmatch(file_regex, files[0].name)
        if not match:
            raise ValueError(f"""Can't extract id from file '{files[0]}' : invalid format : File name must match {file_regex}""")

        return Page(tech, title,  match.group(1))


    def build(self,template: str) -> None:
        print(f"building {self.pages_path}")
        md = self.pages_path.read_text(encoding='utf-8')
        html = markdown.markdown(md, tab_length=2, extensions=[CustomCodeBlockExtension()])
        dist_path = Path(f"dist/{self.id}")
        dist_path.mkdir(parents=True, exist_ok=True)

        (dist_path / "index.html").write_text(
            chevron.render(template,
                           {
                               "content": html,
                               "page": {
                                   "id": self.id,
                                   "tech": self.tech,
                                   "title": self.title,
                                   "title_url": self.title_url,
                               }
                           }),
            encoding="utf-8"
        )
