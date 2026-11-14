import math,json,sys,base64,random
W,H=1600,900
def pts(f,n=80): return [(i*W/n, f(i/n)) for i in range(-2,n+3)]
def path(p): return 'M'+' L'.join(f'{x:.0f} {y:.0f}' for x,y in p)
main=lambda x: (880-560*x+70*math.sin(2*math.pi*1.3*x+1)+30*math.sin(2*math.pi*3.4*x+2))*0.625
sec=lambda x: (520-140*x+55*math.sin(2*math.pi*1.8*x+4))*0.625
thr=lambda x: (760-320*x+40*math.sin(2*math.pi*2.4*x+.5))*0.625
def curtain(f,gid,scale,clip):
    p=pts(f); out=[]
    # glow climbing up from the rim: copies of the rim shifted upward, wider and fainter
    layers=[(0,'#b8ffe0',1,7),(8,'#6affb4',.8,18),(22,'#45f0a2',.6,32),(42,'#33d6ae',.42,50),(70,'#2cb8c4',.3,68),(105,'#5a86e0',.2,86),(145,'#8a5ae0',.14,104)]
    for dy,c,o,w in layers:
        q=[(x,y-dy*scale) for x,y in p]
        out.append(f'<path d="{path(q)}" stroke="{c}" stroke-opacity="{o}" stroke-width="{w*scale:.0f}" fill="none" stroke-linecap="round"/>')
    return f'<g mask="url(#{clip})">'+''.join(out)+'</g>'
random.seed(4)
stars=''.join(f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,H):.0f}" r="{random.choice([.6,.7,.8,1,1.2]):.1f}" fill="#e6f2ff" opacity="{random.uniform(.15,.7):.2f}"/>' for _ in range(140))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05090f"/><stop offset="1" stop-color="#0b1922"/></linearGradient>
<linearGradient id="ends" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity=".85"/></linearGradient>
<linearGradient id="endsB" x1="0" x2="1"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff" stop-opacity=".5"/><stop offset=".95" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="endsC" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".3" stop-color="#fff" stop-opacity=".35"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="rays" width="23" height="900" patternUnits="userSpaceOnUse">
  <rect width="23" height="900" fill="#fff" opacity=".8"/><rect x="3" width="5" height="900" fill="#fff"/><rect x="13" width="3" height="900" fill="#fff" opacity=".9"/>
</pattern>
<filter id="soft" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="9 14"/></filter>
<filter id="bloom" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
<mask id="mA"><rect width="{W}" height="{H}" fill="url(#ends)"/></mask>
<mask id="mB"><rect width="{W}" height="{H}" fill="url(#endsB)"/></mask>
<mask id="mC"><rect width="{W}" height="{H}" fill="url(#endsC)"/></mask>
<mask id="mR"><rect width="{W}" height="{H}" fill="url(#rays)"/></mask>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}
<g filter="url(#bloom)" opacity=".85">{curtain(main,'g',1,'mA')}</g>
<g filter="url(#soft)"><g mask="url(#mR)">{curtain(sec,'g',.8,'mB')}{curtain(thr,'g',.6,'mC')}{curtain(main,'g',1,'mA')}</g></g>
</svg>'''
svg=' '.join(svg.split())
open(sys.argv[1],'w').write(svg); print(len(svg))
html='<html><body style="margin:0;height:100vh;background:#f0f"><img style="width:100%;height:100%;object-fit:cover" src="data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()+'"></body></html>'
open(sys.argv[2],'w').write(html)
