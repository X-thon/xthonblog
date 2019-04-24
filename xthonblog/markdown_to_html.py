#标准库
import codecs

from markdown import Markdown, extensions



def markdown_to_html(file):
    #使用codecs打开文件
    with codecs.open(file, mode='r', encoding='utf-8', errors='ignore') as f:
        body = f.read()
        md = Markdown(extensions=['fenced_code', 'codehilite(css_lass=highlight, linenums=None)', 'meta', 'admonition', 'tables'])
        content = md.convert(body)
        meta = md.Meta if hasattr(md, 'Meta') else {}