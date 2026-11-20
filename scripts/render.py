from pathlib import Path
import json, html, os, datetime
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'cards'; OUT.mkdir(exist_ok=True)
STATIC=os.getenv('STATIC')=='1'
BG='#081426'; PANEL='#10243c'; BLUE='#59c7ff'; WHITE='#eef6ff'; MUTED='#a8bed5'
def esc(s):return html.escape(str(s),quote=True)
def base(w,h,body):
    style='''<style><![CDATA[@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}@keyframes pulse{50%{opacity:.4}}@keyframes sweep{from{transform:translateX(-100%)}to{transform:translateX(110%)}}.reveal{animation:rise .8s ease-out both}.pulse{animation:pulse 2.5s infinite}@media(prefers-reduced-motion:reduce){*{animation:none!important}}]]></style>''' if not STATIC else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><rect width="{w}" height="{h}" rx="22" fill="{BG}"/><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="21" fill="none" stroke="#274565"/>{style}{body}</svg>'
def txt(x,y,s,size=20,color=WHITE,weight=500,extra=''):
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{esc(s)}</text>'
def write(name,w,h,body): (OUT/name).write_text(base(w,h,body),encoding='utf8')
hero=f'<circle cx="52" cy="49" r="6" fill="{BLUE}" class="pulse"/>'+txt(68,56,'OPEN TO INTERNSHIPS & COLLABORATIONS',15,BLUE,700)
hero+=f'<g class="reveal">{txt(48,143,"MUBEEN JAVED",66,WHITE,800)}{txt(50,194,"MERN STACK DEVELOPER",25,BLUE,700)}{txt(50,244,"I build polished, practical full-stack web applications.",21,MUTED)}{txt(50,278,"React  /  Node.js  /  Express  /  MongoDB",18,MUTED)}{txt(50,327,"Based in Lahore, Pakistan  ·  BSFT at ITU Lahore",17,WHITE)}</g>'
hero+='<path d="M50 351 H850" stroke="#284563"/>'+txt(50,381,'github.com/mmubeenjaved2006',16,BLUE)
write('hero.svg',900,408,hero)
for slug,num,title,sub,lines in [
 ('build','01','BUILD','Full-stack development',['React + Node.js','REST APIs + MongoDB']),
 ('design','02','DESIGN','Interactive experiences',['Responsive interfaces','Motion + thoughtful UX']),
 ('learn','03','GROW','Always learning',['Python + Django','Next.js + TypeScript'])]:
    b=f'<g class="reveal"><rect x="18" y="18" width="264" height="242" rx="16" fill="{PANEL}"/>'+txt(38,61,num,18,BLUE,700)+txt(38,111,title,32,WHITE,800)+txt(38,145,sub,16,MUTED)
    for i,line in enumerate(lines): b+=txt(38,190+i*29,line,15,WHITE)
    b+='</g>';write(slug+'.svg',300,278,b)
projects=[('ShopSphere','Full-stack e-commerce experience','https://shopsphere-frontend-gamma.vercel.app/'),('3D Portfolio','Interactive personal developer portfolio','https://mubeen-3d-portfolio.vercel.app/'),('Kelvin Weather','Responsive weather application','https://kelvin-weather.vercel.app/'),('Weather API','Weather lookup application','https://weather-api-rosy-zeta.vercel.app/'),('To-Do List','Simple task management application','https://todo-list-cyan-rho.vercel.app/')]
for i,(name,desc,url) in enumerate(projects,1):
    b=f'<g class="reveal"><rect x="18" y="16" width="824" height="116" rx="14" fill="{PANEL}"/>'+txt(38,53,f'PROJECT {i:02}',13,BLUE,700)+txt(38,87,name,26,WHITE,700)+txt(38,113,desc,16,MUTED)+txt(799,84,'↗',30,BLUE,600)+'</g>'
    write(f'project-{i}.svg',860,148,b)
# Only render graph when real public contribution data is available.
p=ROOT/'data'/'contributions.json'
if p.exists():
    data=json.loads(p.read_text(encoding='utf8')); days=data.get('days',[])
    if days:
        counts=[max(0,int(d['count'])) for d in days]; total=sum(counts)
        cells=''; cell=11; gap=4; cols=53
        for i,d in enumerate(days[-371:]):
            x=28+(i//7)*(cell+gap);y=85+(i%7)*(cell+gap)
            n=max(0,int(d['count']));color=['#142940','#17466a','#186a9c','#239dd3','#68d8ff'][0 if n==0 else 1 if n<3 else 2 if n<7 else 3 if n<15 else 4]
            delay=(i//7)*0.012
            cells+=f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{color}" class="reveal" style="animation-delay:{delay:.3f}s"><title>{esc(d["date"])}: {n} contributions</title></rect>'
        b=txt(28,43,'GITHUB CONTRIBUTIONS',21,WHITE,700)+txt(28,68,f'{total} public contributions in displayed period',15,MUTED)+cells
        write('activity.svg',860,226,b)
print('Rendered SVG cards successfully')
readme=ROOT/'README.md'
if (OUT/'activity.svg').exists():
    source=readme.read_text(encoding='utf8');a='<!-- ACTIVITY_START -->';z='<!-- ACTIVITY_END -->'
    if a in source and z in source:
        start=source.index(a)+len(a);end=source.index(z,start)
        source=source[:start]+'\n<img src="./cards/activity.svg" width="100%" alt="Real public GitHub contribution activity" />\n'+source[end:]
        readme.write_text(source,encoding='utf8')
