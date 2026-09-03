import sys, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

INK='#171520'; ACC='#6B1D2E'; PORC='#FBFAF8'

class Face:
    def __init__(self, path):
        self.f=TTFont(path); self.gs=self.f.getGlyphSet(); self.cmap=self.f.getBestCmap()
        self.upm=self.f['head'].unitsPerEm; self.hmtx=self.f['hmtx']
        os2=self.f['OS/2']; self.cap=getattr(os2,'sCapHeight',700)/self.upm
    def run(self, text, size, tracking=0.0, x=0.0, y=0.0):
        """Return (d, width). tracking in em. y is baseline."""
        s=size/self.upm; d=[]; cx=x; centers=[]
        for i,ch in enumerate(text):
            g=self.cmap[ord(ch)]; adv=self.hmtx[g][0]*s
            pen=SVGPathPen(self.gs, ntos=lambda v: fmt(v)); self.gs[g].draw(TransformPen(pen,(s,0,0,-s,cx,y)))
            d.append(pen.getCommands()); centers.append(cx+adv/2)
            cx+=adv + (tracking*size if i<len(text)-1 else 0)
        return ' '.join(p for p in d if p), cx-x, centers

STROKE='M-3.6,3.2 L0.4,-3.8 C1.2,-4.4 2.2,-4 2.4,-3 L4,2.6 C2.4,3.9 -1.4,4.1 -3.6,3.2 Z'  # ~8 units wide
RULE='M0,0 C30,-1.6 60,1.4 92,0.3 C124,-0.8 156,1.2 188,0.2 C214,-0.6 236,0.8 260,-0.4'      # 260 wide

def fmt(v): return f'{v:.2f}'.rstrip('0').rstrip('.')

def wordmark(face, sans, size=100, tracking=0.03, ink=INK, acc=ACC, pr=False, dot=False):
    d,w,centers=face.run('IMAGINATION',size,tracking,0,0)
    cap=face.cap*size; sw=size*0.145/8
    parts=[f'<path fill="{ink}" d="{d}"/>']
    top=-cap-size*0.06; bottom=size*0.06
    if dot:
        parts.append(f'<path fill="{acc}" transform="translate({fmt(centers[0])},{fmt(-cap-size*0.15)}) scale({fmt(sw)})" d="{STROKE}"/>')
        top=-cap-size*0.30
    if pr:
        pd,pw,_=sans.run('PR',size*0.19,0.42)
        parts.append(f'<path fill="{ink}" opacity=".8" transform="translate({fmt(w/2-pw/2)},{fmt(size*0.36)})" d="{pd}"/>')
        bottom=size*0.40
    return parts,w,top,bottom

def svg(parts,w,top,bottom,pad=0.0,extra_w=0):
    h=bottom-top
    body='\n  '.join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(-pad-extra_w/2)} {fmt(top-pad)} {fmt(w+2*pad+extra_w)} {fmt(h+2*pad)}" role="img" aria-label="Imagination">\n  {body}\n</svg>\n')

def stacked(face,sans,size=100,tracking=0.03,ink=INK,acc=ACC):
    parts,w,top,_=wordmark(face,sans,size,tracking,ink,acc,pr=False)
    rw=w*0.82; parts.append(f'<path fill="none" stroke="{acc}" stroke-width="{fmt(size*0.014)}" stroke-linecap="round" transform="translate({fmt(w/2-rw/2)},{fmt(size*0.24)}) scale({fmt(rw/260)},1)" d="{RULE}"/>')
    td,tw,_=sans.run('PUBLIC RELATIONS · LONDON',size*0.155,0.30)
    parts.append(f'<path fill="{ink}" opacity=".8" transform="translate({fmt(w/2-tw/2)},{fmt(size*0.50)})" d="{td}"/>')
    return parts,w,top,size*0.55

def monogram(face,size=100,ink=INK,acc=ACC,pair=False,dot=False):
    text='IP' if pair else 'I'
    d,w,centers=face.run(text,size,0.06,0,0); cap=face.cap*size; sw=size*0.17/8
    parts=[f'<path fill="{ink}" d="{d}"/>']
    if dot: parts.append(f'<path fill="{acc}" transform="translate({fmt(centers[0])},{fmt(-cap-size*0.15)}) scale({fmt(sw)})" d="{STROKE}"/>')
    return parts,w,-cap-size*(0.30 if dot else 0.06),size*0.05

def favicon(face,bg=ACC,fg=PORC):
    size=62; d,w,centers=face.run('I',size,0,0,0); cap=face.cap*size; sw=size*0.19/8
    cx=50-w/2; cy=50+cap/2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Imagination">\n'
            f'  <circle cx="50" cy="50" r="50" fill="{bg}"/>\n'
            f'  <path fill="{fg}" transform="translate({fmt(cx)},{fmt(cy)})" d="{d}"/>\n</svg>\n')

if __name__=='__main__':
    facefile=sys.argv[1]; outdir=sys.argv[2]
    face=Face(facefile); sans=Face('IS-600.ttf')
    open(f'{outdir}/wordmark.svg','w').write(svg(*wordmark(face,sans),pad=6))
    open(f'{outdir}/wordmark-light.svg','w').write(svg(*wordmark(face,sans,ink='#F3EEE8'),pad=6))
    open(f'{outdir}/wordmark-burgundy.svg','w').write(svg(*wordmark(face,sans,ink=ACC),pad=6))
    open(f'{outdir}/wordmark-mono.svg','w').write(svg(*wordmark(face,sans,ink='currentColor'),pad=6))
    open(f'{outdir}/stacked.svg','w').write(svg(*stacked(face,sans),pad=8))
    open(f'{outdir}/stacked-light.svg','w').write(svg(*stacked(face,sans,ink='#F3EEE8',acc='#DE9AA6'),pad=8))
    open(f'{outdir}/mark-i.svg','w').write(svg(*monogram(face),pad=8))
    open(f'{outdir}/mark-i-light.svg','w').write(svg(*monogram(face,ink='#F3EEE8'),pad=8))
    open(f'{outdir}/favicon.svg','w').write(favicon(face))
    print('done', outdir)
