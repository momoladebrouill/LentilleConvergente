import random
import time
import pygame as pg
from datetime import date,datetime
import files.utis as utis
from files.utis import math

class wind:
    larg=750
    haut=750

def montr(texte,pos,coul=(255,255,255)):
    te=font.render(texte,False,coul)
    f.blit(te,pos)
    return te.get_rect()

B = 1 #La boucle d'activité
mid = utis.Pos(wind.larg/2,wind.haut/2)
a = utis.Pos(wind.larg/3,wind.haut/4)
p = a
foc = 50
fakefoc = 50
pressed = False
shownerd = True
showarbres = False

pg.init()
font = pg.font.SysFont("consolas",20)
icon = pg.Surface((100,100))
icon.fill(random.randrange(0,0xffffff))
icon.blit(font.render(' ',1,(255,0,0)),(0,0))
pg.display.set_icon(icon)
pg.display.set_caption("Shema optique focale du Capitaine µ")
f = pg.display.set_mode((wind.larg,wind.haut),pg.RESIZABLE)
fps = pg.time.Clock()

try:
    arbre=pg.image.load("files/arbre.png")
    arbrerect=arbre.get_rect()
except:
    arbre=pg.Surface((100,100))
    arbre.blit(font.render("FranceSus",True,(255,255,255)),(0,0))
    arbre.blit(font.render("µ",True,(255,255,255)),(40,40))
    arbrerect=arbre.get_rect()

while B:
    fps.tick(60)
    pg.display.flip()
    f.fill(0)
    
    ### Les calculs (pas rénaux)
    
    # De A vers F'
    ang=math.atan2(mid.y-a.y,foc)
    v=utis.Vec(long=5000,angle=ang)

    # De A vers O
    vcentr=utis.Vec(long=5000,angle=mid.angle(a))

    # De A vers F
    t=utis.Pos(mid.x-foc,mid.y).angle(a);
    y=utis.math.tan(t)*foc + mid.y;

    # Point B (point reflété)
    b=utis.Pos(mid.x+utis.math.tan(math.pi/2-ang)*(y-a.y),y);

    # Gamma
    gam=(mid.y-b.y)/(mid.y-a.y)
    
    ### Los dibujos
    
    # Quadrillage
    pg.draw.line(f,0xffffff,(0,mid.y),(wind.larg,mid.y))
    pg.draw.line(f,0xffffff,(mid.x,0),(mid.x,wind.haut))
    
    # Ligne du haut
    pg.draw.line(f,0xffff00,(a.x,a.y),(mid.x,a.y));
    pg.draw.line(f,0x555500,a.pourpg(),b.pourpg())
    pg.draw.line(f,0xffff00,(mid.x,a.y),(mid.x+v.x,a.y+v.y))
    
    # Ligne centrale
    pg.draw.line(f,0xffff00,(a.x,a.y),(a.x+vcentr.x,a.y+vcentr.y))

    # Ligne du bas
    pg.draw.line(f,0xffff00,a.pourpg(),(mid.x,y))
    pg.draw.line(f,0x555500,(mid.x,y),(b.x,y));
    pg.draw.line(f,0xffff00,(mid.x,y),(mid.x+5000,y));
    
    # Point A (objet initial)
    pg.draw.circle(f,0xff00ff,a.pourpg(),5)
    pg.draw.line(f,0xff00ff,a.pourpg(),(a.x,mid.y));
    
    # Point B (objet reflété)
    pg.draw.line(f,0xff00,(b.x,mid.y),b.pourpg());
    pg.draw.circle(f,0xff00,b.pourpg(),5);

    # Point O (Optique)
    pg.draw.circle(f,0xff,mid.pourpg(),5)

    # Points F et F'
    pg.draw.circle(f,0xff0000,(mid.x-foc,mid.y),5)
    pg.draw.circle(f,0xff0000,(mid.x+foc,mid.y),5)

    # Les arbres
    if showarbres and b.x<wind.larg:
        # Arbre A
        haut=mid.y-a.y
        ab=pg.transform.scale(arbre,(int(abs(haut/arbrerect.height*arbrerect.width)),int(abs(haut))))
        if haut<=0:
            pt=mid.y
            ab=pg.transform.flip(ab,False,True)
        else:
            pt=a.y
        f.blit(ab,(a.x-ab.get_rect().width/2,pt))

        #Arbre B
        if b.x>mid.x:
            haut=mid.y-b.y
            ab=pg.transform.scale(arbre,(int(abs(haut/arbrerect.height*arbrerect.width)),int(abs(haut))))
            if haut<=0:
                pt=mid.y
                ab=pg.transform.flip(ab,False,True)
            else:
                pt=b.y
            f.blit(ab,(b.x-ab.get_rect().width/2,pt))
    
    #Nomer les points
    montr("A",(a.x-15,a.y-15),(255,0,255))
    montr("B",(a.x,mid.y+10),(255,0,255))
    montr("A'",(b.x+10,b.y+10),(0,255,0))
    montr("B'",(b.x,mid.y+10),(0,255,0))
    montr("F",(mid.x-foc+10,mid.y+10),(255,0,0))
    montr("F'",(mid.x+foc+10,mid.y+10),(255,0,0))
    montr("O",(mid.x+10,mid.y+10),(0,0,255))

    # Description de l'image
    
    adj="Image %s, %s et %s ." %(
            "virtuelle" if b.x < mid.x else "réelle",
            "droite" if gam > 0 else "renversée",
            "agrandie" if abs(gam) > 1 else "rétrécie")
    
    # Affichahge stats de nerds
    
    if shownerd:
        #NO
        decal=montr("BA Taille  : %i px" % (mid.y - a.y),(0,0),(255,0,255)).height
        montr("BO Distance lentille : %i px" % (mid.x-a.x),(0,decal))
        #NE
        montr("B'A' Taille de l'image formé : %i px" % (mid.y-b.y),(mid.x+10,0),(0,255,0))
        montr("B'O Distance lentille : %i px" % (mid.x-b.x), (mid.x+10,decal))
        #SO
        montr("OF' Distance focale : %i px " % fakefoc,(0,wind.haut-decal),(255,0,0))
        montr(f"Gamma γ : {gam}",(0,wind.haut-2*decal))
        montr(adj,(0,wind.haut-3*decal))
        #SE
        montr("A pour montrer les arbres",(wind.larg-300,wind.haut-60))
        montr("S pour télécharger l'image",(wind.larg-300,wind.haut-40))
        montr("H pour afficher les stats",(wind.larg-300,wind.haut-20))
    
    # Déplacement de la focale et du point de l'user
    
    foc+=(fakefoc-foc)/10
    if pressed:
        posi = pg.mouse.get_pos()
        p = utis.Pos(posi[0],posi[1])
    goto = utis.Vec(long=p.dist(a)/7,angle=p.angle(a))
    a.x += goto.x
    a.y += goto.y
        
    # Event listener

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            B=0
        elif event.type == pg.MOUSEBUTTONUP:
            if event.dict['button']==4:
                fakefoc+=10
            elif event.dict['button']==5:
                fakefoc-=10
            fakefoc=abs(fakefoc)
            pressed=False
        elif event.type == pg.MOUSEBUTTONDOWN:
            pressed=True
        elif event.type==pg.VIDEORESIZE:
            wind.haut,wind.larg=event.h,event.w
            mid=utis.Pos(wind.larg/2,wind.haut/2)
            a=utis.Pos(wind.larg/3,wind.haut/4)
        elif event.type==pg.KEYUP:
            keu = event.dict['key']
            if keu == pg.K_UP:
                fakefoc+=10
            elif keu == pg.K_DOWN:
                fakefoc-=10
            elif keu == pg.K_s:
                today = date.today()
                now = datetime.now()
                pg.image.save(f,today.strftime("%d %B %Y")+','+now.strftime("%H.%M.%S")+".png")
                for i in range(10):
                    time.sleep(0.1)
                    f.blit(font.render('Image téléchargée !!!',
                        True,
                        (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),
                        (wind.larg-300,wind.haut-80))
                    pg.display.flip()
                time.sleep(1)
            elif keu == pg.K_h:
                shownerd = not shownerd
            elif keu == pg.K_a:
                showarbres = not showarbres
            fakefoc = abs(fakefoc)

