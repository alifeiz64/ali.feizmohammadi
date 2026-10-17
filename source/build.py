#!/usr/bin/env python3
"""Build the academic website. Python 3 standard library only."""
from pathlib import Path
import argparse
import html
import json
import math
import shutil
from itertools import groupby

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', default='dist', help='Output directory, relative to this script')
parser.add_argument('--base-url', default='', help='Optional canonical URL, including repository path')
parser.add_argument('--base-path', default='/', help='Absolute path for the custom 404 page')
parser.add_argument('--private-preview', action='store_true', help='Prevent indexing of a review copy')
args = parser.parse_args()
OUT = ROOT / args.output
OUT.mkdir(parents=True, exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
papers = json.loads((ROOT / 'content/publications.json').read_text())
talks = json.loads((ROOT / 'content/talks.json').read_text())
teaching = json.loads((ROOT / 'content/teaching.json').read_text())
by_id = {p['arxiv']: p for p in papers}
e = lambda text: html.escape(str(text), quote=True)
ARXIV = 'https://arxiv.org/search/?query=Feizmohammadi%2C+Ali&searchtype=author&abstracts=show&order=-announced_date_first&size=50'
EMAIL = 'ali.feizmohammadi@utoronto.ca'
NAV = [('index.html', 'Home'), ('research.html', 'Research'), ('publications.html', 'Publications'), ('talks.html', 'Talks'), ('teaching.html', 'Teaching')]

def ext(url, label, cls=''):
    return f'<a href="{e(url)}" class="{e(cls)}" target="_blank" rel="noopener noreferrer">{label}</a>'

def layout(filename, title, description, body):
    links = ''.join(f'<a href="{path}"'+(' aria-current="page"' if path == filename else '')+f'>{label}</a>' for path, label in NAV)
    canonical = f'<link rel="canonical" href="{e(args.base_url.rstrip("/") + "/" + ("" if filename == "index.html" else filename))}">' if args.base_url else ''
    robots = '<meta name="robots" content="noindex,nofollow">' if args.private_preview else ''
    base = f'<base href="{e(args.base_path)}">' if filename == '404.html' else ''
    person = {'@context':'https://schema.org','@type':'Person','name':'Ali Feizmohammadi','jobTitle':'Research Associate','affiliation':{'@type':'CollegeOrUniversity','name':'University of Toronto'},'email':EMAIL,'knowsAbout':['Inverse problems','Partial differential equations','Geometric analysis','Spectral theory'],'sameAs':['https://sites.google.com/view/alifeizmohammadi/', ARXIV]}
    if args.base_url: person['url'] = args.base_url
    schema = f'<script type="application/ld+json">{json.dumps(person,ensure_ascii=False)}</script>' if filename == 'index.html' else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{e(title)}</title><meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#1e333c"><meta name="author" content="Ali Feizmohammadi">
  <meta property="og:type" content="website"><meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}"><meta property="og:site_name" content="Ali Feizmohammadi">
  {base}{canonical}{robots}
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script>
  {schema}
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>
<header class="site-header"><div class="container header-inner">
  <a class="brand" href="index.html" aria-label="Ali Feizmohammadi — home">A. Feizmohammadi<small>Mathematics</small></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav class="site-nav" id="site-nav" aria-label="Main navigation">{links}<a href="#contact">Contact</a></nav>
</div></header>
<main id="main" class="container">{body}</main>
<footer class="site-footer" id="contact"><div class="container">
  <div class="footer-main"><div><p class="footer-name">Ali Feizmohammadi</p>
    <p>Department of Mathematics<br>University of Toronto · St. George<br>Toronto, Canada</p></div>
    <div class="footer-contact"><p class="eyebrow">Contact</p><a class="email-link" href="mailto:{EMAIL}">{EMAIL}</a>
      <div class="footer-links">{ext(ARXIV,'arXiv ↗')}{ext('https://www.math.toronto.edu/','Department ↗')}<a href="publications.html">Publications →</a></div>
    </div>
  </div>
  <div class="footer-bottom"><span>© 2026 Ali Feizmohammadi</span><a href="#main">Back to top ↑</a></div>
</div></footer>
</body></html>'''

def art():
    # Original vector line drawing: a decorative, projected family of wavefronts.
    lines = []
    for k in range(22):
        r = .16 + k * .039
        pts = []
        for n in range(241):
            t = 2*math.pi*n/240
            x = 205 + 183*r*math.cos(t) + 16*r*r*math.sin(2*t)
            y = 202 + 122*r*math.sin(t) - 54*math.exp(-((x-205)/92)**2)*(1-r*r)
            pts.append(f'{x:.2f},{y:.2f}')
        color = '#467176' if k%5 else '#9a684e'
        opacity = '.7' if k%5 else '.85'
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="{.65 if k%5 else .9}"/>')
    meridians=[]
    for a in [-2.65,-2.1,-1.55,-1.0,-.45,.15,.7,1.25]:
        pts=[]
        for n in range(181):
            r=-.98+n*1.96/180
            x=205+183*r*math.cos(a)+16*r*r*math.sin(2*a)
            y=202+122*r*math.sin(a)-54*math.exp(-((x-205)/92)**2)*(1-r*r)
            pts.append(f'{x:.2f},{y:.2f}')
        meridians.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#467176" stroke-opacity=".22" stroke-width=".6"/>')
    return '<svg viewBox="0 0 410 385" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M28 335H382M28 40V335" stroke="#becbc3" stroke-width=".6"/><path d="M24 60h8M24 150h8M24 240h8M80 331v8M200 331v8M320 331v8" stroke="#b8c7bd" stroke-width=".6"/>'+''.join(meridians+lines)+'<circle cx="350" cy="232" r="3.3" fill="#8d4f35"/><path d="M355 233l25 14" stroke="#8d4f35" stroke-width=".8"/><text x="374" y="260" font-family="Georgia,serif" font-style="italic" font-size="14" fill="#8d4f35">∂Ω</text></svg>'

def home_paper(pid):
    p=by_id[pid]
    label='Preprint' if p['status']=='preprint' else p['journal']
    coauthors=[a for a in p['authors'] if a!='Ali Feizmohammadi']
    who='With '+', '.join(coauthors) if coauthors else 'Single-authored'
    return f'''<article class="home-paper"><div class="paper-label">{p['year']}<span>{e(label)}</span></div><div><h3><a href="publications.html#paper-{pid}">{e(p['title'])}</a></h3><p>{e(who)}</p></div><a class="row-arrow" href="publications.html#paper-{pid}" aria-label="Details for {e(p['title'])}">↗</a></article>'''

home=f'''
<section class="hero" aria-labelledby="home-name"><div>
  <p class="eyebrow">University of Toronto · Mathematics</p>
  <h1 id="home-name"><span>Ali</span><span>Feizmohammadi</span></h1>
  <p class="intro">I study inverse problems for partial differential equations, with a focus on the interplay between analysis and geometry.</p>
  <p class="position"><strong>Research Associate, Department of Mathematics</strong><br>University of Toronto · St. George</p>
  <div class="hero-actions"><a class="button" href="research.html">Explore my research <span aria-hidden="true">↗</span></a><a class="text-link" href="publications.html">Publications <span aria-hidden="true">→</span></a></div>
</div><figure class="hero-art">{art()}<figcaption class="art-caption"><span>Analysis &amp; geometry</span><span>Inverse problems<br>Partial differential equations</span></figcaption></figure></section>
<aside class="honor-strip" aria-label="Award"><span class="honor-label">Recognition</span>{ext('https://ipia.site/wp/calderon-prizes/','Calderón Prize, 2025 <span aria-hidden="true">↗</span>')}<p>Inverse Problems International Association</p></aside>
<section class="section" aria-labelledby="recent-heading"><p class="eyebrow section-kicker">Research</p><div class="section-heading"><h2 id="recent-heading">Recent work</h2><a class="text-link" href="publications.html">Full bibliography <span aria-hidden="true">→</span></a></div><div>
  {''.join(home_paper(pid) for pid in ['2610.06766','2609.28047','2407.16866','2507.22723'])}
</div></section>
<section class="about-section" aria-labelledby="about-heading"><div class="about-copy"><p class="eyebrow section-kicker">Background</p><h2 id="about-heading">About me</h2>
  <p>I am a Research Associate in the Department of Mathematics at the University of Toronto, St. George, for September 2026–August 2027. My work concerns the recovery of coefficients and geometry from partial boundary, spectral, and wave data.</p>
  <p>Previously, I was an Assistant Professor at the University of Toronto Mississauga, a Simons Postdoctoral Fellow at the Fields Institute, and a Research Associate at University College London.</p>
  <a class="text-link" href="teaching.html">Teaching experience <span aria-hidden="true">→</span></a>
</div><div><p class="eyebrow section-kicker">Appointments</p><ol class="timeline">
  <li><time>2026–2027</time><div><strong>University of Toronto · St. George</strong><span>Research Associate</span></div></li>
  <li><time>2022–2026</time><div><strong>University of Toronto Mississauga</strong><span>Assistant Professor</span></div></li>
  <li><time>2021–2022</time><div><strong>Fields Institute</strong><span>Simons Postdoctoral Fellow</span></div></li>
  <li><time>2018–2021</time><div><strong>University College London</strong><span>Research Associate</span></div></li>
</ol></div></section>'''

def reading(pid):
    p=by_id[pid]
    return f'<a class="reading-item" href="publications.html#paper-{pid}">{e(p["title"])}<small>{e(p["journal"] or "Preprint")} · {p["year"]} ↗</small></a>'

research='''<div class="page-intro"><p class="eyebrow">Research</p><h1>Inverse problems,<br>analysis &amp; geometry.</h1><p class="lead">How much can we learn about a differential equation—or the geometry on which it is defined—from observations of its solutions?</p></div>'''
research_areas=[
 ('01','Geometric inverse problems',
  'My research concerns uniqueness and reconstruction in inverse boundary value problems. A central theme is the Calderón problem: recovering the coefficients of an elliptic equation, or the underlying geometry, from boundary measurements.',
  'I study these questions on Riemannian manifolds, for linear and nonlinear equations, and in settings where only partial data are available.',
  ['2110.07500','2009.10280']),
 ('02','Waves & Lorentzian geometry',
  'For wave equations, the geometry of propagation is central to understanding what boundary observations determine. I study inverse problems on Lorentzian manifolds and the unique continuation questions that underlie them.',
  'This work brings together Carleman estimates, geometric analysis, and the behavior of waves in curved spacetimes.',
  ['2008.07508','2112.01663']),
 ('03','Spectral & nonlocal problems',
  'I investigate how coefficients and geometry can be recovered from incomplete spectral information and from local measurements for fractional differential operators.',
  'These problems connect inverse spectral theory, unique continuation, and nonlocal equations. They also lead to questions about recovery from a single passive observation of an evolving solution.',
  ['2407.16866','2507.22723'])
]
for num,title,p1,p2,refs in research_areas:
    research+=f'<section class="research-row"><span class="research-num" aria-hidden="true">{num}</span><div class="research-text"><h2>{e(title)}</h2><p>{e(p1)}</p><p>{e(p2)}</p></div><aside class="research-reading" aria-label="Related papers"><h3>Related papers</h3>{"".join(reading(pid) for pid in refs)}</aside></section>'
research+='''<aside class="methods-note"><h2>Methods &amp; themes</h2><p>Unique continuation · Carleman estimates · Microlocal analysis · Spectral theory · Riemannian and Lorentzian geometry</p></aside>'''

def paper_html(p):
    pid=p['arxiv']
    search=' '.join([p['title'],*p['authors'],str(p['year']),p['journal'],p['doi'],pid])
    journal=(f'<em>{e(p["journal"])}</em> <span class="details">· {e(p["details"])} · {p["year"]}</span>' if p['journal'] else f'{e(p["details"])} · {p["year"]}')
    links=(ext('https://doi.org/'+p['doi'],'Journal ↗') if p['doi'] else '')+ext('https://arxiv.org/abs/'+pid,'arXiv ↗')+ext('https://arxiv.org/pdf/'+pid,'PDF ↗')
    return f'''<article class="paper" id="paper-{pid}" data-status="{p['status']}" data-search="{e(search)}"><h3>{ext('https://arxiv.org/abs/'+pid,e(p['title']))}</h3><p class="paper-authors">{e(', '.join(p['authors']))}</p><p class="paper-venue">{journal}</p><div class="paper-links">{links}</div></article>'''

publications=f'''<div class="page-intro"><p class="eyebrow">Publications</p><h1>Papers &amp; preprints</h1><p class="lead">Research in inverse problems, partial differential equations, and geometry.</p><div class="page-links">{ext(ARXIV,'View on arXiv ↗','text-link')}<a class="text-link" href="publications.bib" download>Download bibliography ↓</a></div></div>
<div class="publication-tools" hidden><div class="filter-buttons" role="group" aria-label="Filter by publication type">'''
for key,label in [('all','All'),('published','Published'),('preprint','Preprints'),('earlier','Earlier work')]:
    n=len(papers) if key=='all' else len([p for p in papers if p['status']==key])
    publications+=f'<button type="button" class="filter-button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{label}<span>{n}</span></button>'
publications+='''</div><div class="search-wrap"><label for="paper-search" class="sr-only">Search publications by title, author, journal, or year</label><svg width="15" height="15" viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="5.5" stroke="currentColor" stroke-width="1.4"/><path d="m12 12 5 5" stroke="currentColor" stroke-width="1.4"/></svg><input type="search" id="paper-search" placeholder="Search title, author, year…" autocomplete="off"></div></div><p class="result-count" id="result-count" role="status" aria-live="polite">37 papers</p>
<div id="empty-results" class="empty-state" hidden><p>No papers match this search.</p><button id="reset-search" type="button">Clear the search and show all papers</button></div>'''
for key,title,subtitle in [('preprint','Preprints','2024–2026'),('published','Publications','2019–2026'),('earlier','Earlier manuscripts','Unpublished work')]:
    group=sorted([p for p in papers if p['status']==key],key=lambda p:p['year'],reverse=True)
    publications+=f'<section class="pub-section" aria-label="{title}"><div class="pub-group-heading"><h2>{title}</h2><span>{subtitle}</span></div>'
    for year,items in groupby(group,key=lambda p:p['year']):
        publications+=f'<div class="pub-year"><h3>{year}</h3><div>'+''.join(paper_html(p) for p in items)+'</div></div>'
    publications+='</section>'
publications+='''<section class="dissertation"><h2>PhD dissertation</h2><div><h3><a href="https://hdl.handle.net/1807/89822" target="_blank" rel="noopener noreferrer">Recovery of a Potential from Boundary Data in Locally Conformally Transversally Anisotropic Geometries ↗</a></h3><p>University of Toronto, 2018</p></div></section>'''

talkpage='''<div class="page-intro"><p class="eyebrow">Talks &amp; visits</p><h1>Lectures &amp; conversations</h1><p class="lead">Conference lectures, seminars, and research visits.</p></div><div class="recordings">'''
for t in [talks[1],talks[2]]:
    talkpage+=f'''<a class="recording" href="{e(t['video'])}" target="_blank" rel="noopener noreferrer"><span class="play-icon" aria-hidden="true">▶</span><div><p class="eyebrow">Recorded lecture · {t['month']} {t['year']}</p><h2>{e(t['event'])}</h2><p>{e(t['place'])} · Watch recording ↗</p></div></a>'''
talkpage+='</div><div class="talk-archive">'
for year,items in groupby(talks,key=lambda t:t['year']):
    talkpage+=f'<section class="talk-year" aria-label="Talks and visits in {year}"><h2>{year}</h2><ul class="talk-list">'
    for t in items:
        badge='<span class="plenary">Plenary lecture</span>' if t['plenary'] else ''
        video=ext(t['video'],'Video ↗','video-link') if t['video'] else ''
        talkpage+=f'<li><time>{t["month"]}</time><div><h3>{e(t["event"])}{badge}</h3><p>{e(t["place"])}</p></div>{video}</li>'
    talkpage+='</ul></section>'
talkpage+='</div>'

teachpage='''<div class="page-intro"><p class="eyebrow">Teaching</p><h1>Teaching mathematics</h1><p class="lead">Courses taught at the University of Toronto.</p></div><div class="teaching-intro"><p>My teaching has ranged from introductions to mathematical proof and calculus to linear algebra, complex variables, and partial differential equations.</p><p class="teaching-note">The list below includes both instruction and course coordination.</p></div><table class="teaching-table"><caption class="sr-only">Teaching experience, most recent first</caption><thead><tr><th scope="col">Term</th><th scope="col">Course</th><th scope="col">Role</th></tr></thead><tbody>'''
for t in teaching:
    role='Instructor &amp; coordinator' if t['coordinator'] else 'Instructor'
    cls=' coordinator' if t['coordinator'] else ''
    teachpage+=f'<tr><td class="term">{t["term"]} {t["year"]}</td><td class="course">{e(t["course"])}<small>{t["code"]}</small></td><td class="role{cls}">{role}</td></tr>'
teachpage+='''</tbody></table><section class="outreach"><p class="eyebrow section-kicker">Beyond the classroom</p><h2>Mathematical problem solving</h2><p>From 2013 to 2017, I prepared students at the University of Toronto Mississauga for the <a href="https://web.math.rochester.edu/people/faculty/dangeba/urmo.html" target="_blank" rel="noopener noreferrer">Rochester Mathematics Olympiad ↗</a>.</p></section>'''

notfound='''<div class="not-found"><p class="eyebrow">404 · Page not found</p><h1>A different direction.</h1><p>This page may have moved. You can return to the homepage or browse the publication list.</p><div class="hero-actions"><a class="button" href="index.html">Return home →</a><a class="text-link" href="publications.html">Publications →</a></div></div>'''

pages=[
 ('index.html','Ali Feizmohammadi — Mathematics','Ali Feizmohammadi, Research Associate at the University of Toronto. Inverse problems, partial differential equations, and geometric analysis.',home),
 ('research.html','Research — Ali Feizmohammadi','Research in geometric inverse problems, wave equations on Lorentzian manifolds, spectral theory, and fractional equations.',research),
 ('publications.html','Publications — Ali Feizmohammadi','Publications and preprints by Ali Feizmohammadi, with journal, arXiv, and PDF links and a downloadable bibliography.',publications),
 ('talks.html','Talks & Visits — Ali Feizmohammadi','Conference lectures, seminars, research visits, and recorded talks by Ali Feizmohammadi.',talkpage),
 ('teaching.html','Teaching — Ali Feizmohammadi','Teaching and course coordination at the University of Toronto: mathematics, calculus, analysis, and differential equations.',teachpage),
 ('404.html','Page not found — Ali Feizmohammadi','Return to Ali Feizmohammadi’s academic website.',notfound)
]
for filename,title,description,body in pages:
    (OUT/filename).write_text(layout(filename,title,description,body),encoding='utf-8')

def bib_value(s):
    return s.replace('Lᵖ',r'$L^p$').replace('–','--').replace('&',r'\&')

bib=['% Bibliography for Ali Feizmohammadi. UTF-8; suitable for BibLaTeX/Biber.\n% Publication status reflects the personal website reviewed on 17 October 2026.\n']
for p in sorted(papers,key=lambda p:p['year'],reverse=True):
    fields={'title':'{'+bib_value(p['title'])+'}','author':' and '.join(p['authors']),'year':str(p['year']),'eprint':p['arxiv'],'archivePrefix':'arXiv','url':'https://arxiv.org/abs/'+p['arxiv']}
    kind='article' if p['status']=='published' else 'misc'
    if p['journal']: fields['journal']=p['journal']
    if p['doi']: fields['doi']=p['doi']
    if p['details']: fields['note']=p['details'].replace('–','--')
    bib.append('@'+kind+'{Feizmohammadi'+p['arxiv'].replace('.','')+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items())+'\n}\n')
(OUT/'publications.bib').write_text('\n'.join(bib),encoding='utf-8')
(OUT/'.nojekyll').write_text('')
if args.private_preview:
    (OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
elif args.base_url:
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+args.base_url.rstrip('/')+'/sitemap.xml\n')
    urls=[args.base_url.rstrip('/')+'/'+('' if file=='index.html' else file) for file,_,_,_ in pages if file!='404.html']
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(url)+'</loc></url>' for url in urls)+'</urlset>\n')
else:
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n')
print(f'Built {len(pages)} pages, {len(papers)} papers, {len(talks)} talks and visits, and {len(teaching)} teaching records in {OUT}')
