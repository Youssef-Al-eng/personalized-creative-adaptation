"""Deterministic palette adaptation for raster artwork with preservation metrics."""
from __future__ import annotations
import json, math, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def create_asset(path:Path,size:int=128,variant:int=0)->None:
    im=Image.new('RGBA',(size,size),(242,238,226,255)); d=ImageDraw.Draw(im)
    if variant==0:
        d.ellipse((15,15,size-15,size-15),fill=(33,85,104,255)); d.polygon([(size//2,27),(size-27,size//2),(size//2,size-27),(27,size//2)],fill=(216,139,79,255))
        d.ellipse((size//2-12,size//2-12,size//2+12,size//2+12),fill=(246,221,150,255))
    elif variant==1:
        d.rounded_rectangle((18,18,size-18,size-18),radius=18,fill=(99,72,125,255)); d.rectangle((34,34,size-34,size-34),fill=(224,119,103,255)); d.ellipse((48,48,80,80),fill=(244,211,126,255))
    else:
        d.polygon([(size//2,12),(size-12,size-12),(12,size-12)],fill=(44,126,89,255)); d.ellipse((40,47,88,95),fill=(222,164,66,255)); d.rectangle((58,68,70,116),fill=(84,73,57,255))
    im.save(path)

def adapt(source:Path,destination:Path,palette:list[tuple[int,int,int]],method:str)->None:
    if method not in {'palette','tint','none'}: raise ValueError('method must be palette, tint, or none')
    if not palette or any(len(c)!=3 or any(v<0 or v>255 for v in c) for c in palette): raise ValueError('palette must contain RGB triples')
    image=Image.open(source).convert('RGBA'); pixels=image.load()
    if method=='palette':
        for y in range(image.height):
            for x in range(image.width):
                r,g,b,a=pixels[x,y]
                if a==0: continue
                # nearest requested palette color, with a luminance-scaled blend retaining tonal order
                target=min(palette,key=lambda c:(r-c[0])**2+(g-c[1])**2+(b-c[2])**2)
                lum=(.299*r+.587*g+.114*b)/255
                pixels[x,y]=tuple(round(min(255,max(0,ch*(.55+.45*lum)))) for ch in target)+(a,)
    elif method=='tint':
        tint=palette[0]
        for y in range(image.height):
            for x in range(image.width):
                r,g,b,a=pixels[x,y]
                if a: pixels[x,y]=tuple(round(.72*value+.28*color) for value,color in zip((r,g,b),tint))+(a,)
    image.save(destination)

def _edge_rmse(a:Image.Image,b:Image.Image)->float:
    ea=a.convert('L').filter(ImageFilter.FIND_EDGES); eb=b.convert('L').filter(ImageFilter.FIND_EDGES)
    return math.sqrt(sum((x-y)**2 for x,y in zip(ea.get_flattened_data(),eb.get_flattened_data()))/max(1,a.width*a.height))/255

def _palette_distance(im:Image.Image,palette:list[tuple[int,int,int]])->float:
    pix=list(im.convert('RGB').get_flattened_data())
    return sum(min(math.dist(p,c) for c in palette) for p in pix)/max(len(pix),1)/math.sqrt(3*255**2)

def run(out:Path)->dict:
    out.mkdir(parents=True,exist_ok=True)
    palettes={"coastal":[(40,83,96),(230,155,95),(245,225,170)],
              "orchid":[(74,53,98),(199,113,150),(244,204,183)],
              "forest":[(38,82,61),(157,181,100),(230,191,104)]}
    rows=[]
    for asset_id in range(3):
        src=out/f'asset_{asset_id}.png'; create_asset(src,variant=asset_id)
        if asset_id==0: src.replace(out/'source.png'); src=out/'source.png'
        original=Image.open(src).convert('RGBA')
        for profile,palette in palettes.items():
            for method in ('none','tint','palette'):
                dest=out/f'{profile}_asset_{asset_id}_{method}.png'; adapt(src,dest,palette,method); image=Image.open(dest).convert('RGBA')
                rows.append({'asset_id':asset_id,'profile':profile,'method':method,'palette_distance':_palette_distance(image,palette),
                    'edge_rmse':_edge_rmse(original,image),'dimensions_preserved':image.size==original.size,'bytes':dest.stat().st_size})
                if asset_id==0 and profile=='coastal':
                    image.save(out/f'{method}.png')
    report={'asset':'three original deterministic geometric illustrations; not user art',
            'profile_count':len(palettes),'asset_count':3,'human_evaluation':'not conducted',
            'profiles':palettes,'metrics':rows}
    (out/'metrics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

if __name__=='__main__': print(json.dumps(run(Path('results')),indent=2))
