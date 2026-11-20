"""Read GitHub's public contributions HTML; fail rather than invent data."""
from urllib.request import Request,urlopen
from html.parser import HTMLParser
from pathlib import Path
import json,re,datetime
USER='mmubeenjaved2006'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.days={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag not in ('td','tool-tip','rect'):return
  date=a.get('data-date') or a.get('data-iso-date'); count=a.get('data-count')
  if date and count is not None and re.fullmatch(r'\d{4}-\d{2}-\d{2}',date):self.days[date]=int(count)
req=Request(f'https://github.com/users/{USER}/contributions',headers={'User-Agent':'Mozilla/5.0 GitHub-profile-README'})
page=urlopen(req,timeout=25).read().decode('utf-8')
parser=Parser();parser.feed(page)
if len(parser.days)<300:raise RuntimeError(f'Could only parse {len(parser.days)} days. GitHub may have changed its public HTML. Existing graph is preserved.')
days=[{'date':k,'count':v} for k,v in sorted(parser.days.items())]
path=Path(__file__).resolve().parents[1]/'data'/'contributions.json';path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps({'user':USER,'days':days},indent=2)+'\n',encoding='utf8')
print('Fetched',len(days),'real contribution days')
