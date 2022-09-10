"""Stuufs utils pour momo, je sais même pas si je vais m'en serveir"""
import math

class Pos:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def move(self,vec):
        self.x+=vec.x
        self.y+=vec.y

    def dist(self,autrui):
        return math.sqrt((self.x-autrui.x)**2+(self.y-autrui.y)**2)
    
    def angle(self,autrui):
        return math.atan2(self.y-autrui.y,self.x-autrui.x)
    
    def pourpg(self):
        return (self.x,self.y)
    
    def __add__(self,other):
        x=self.x+other.x
        y=self.y+other.y
        return Pos(x=x,y=y)
    
    def __repr__(self):
        return 'Position : '+ str(self.pourpg())

def addvecs(*vecs):
    """fait la somme des vecteurs"""
    x = 0
    y = 0
    for vectot in vecs:
        x+=vectot.x
        y+=vectot.y
    return Vec(x=x,y=y)


class Vec:
    """Vecteur très bien faits"""
    
    def __init__(self,**args):
        """
        (x,y) ou (angle,long) ou (pa,pb)
        et genre pa et pb c'est des utis.Pos"""
        
        if 'x' in args:
            self.x = args['x']
            self.y = args['y']
            self.angle = math.atan2(self.y,self.x)
            self.long = Pos(0,0).dist(Pos(self.x,self.y))
        
        elif 'long' in args:
            self.angle = args.get('angle',0)
            self.long = args.get('long',1)
            self.x = math.cos(self.angle)*self.long
            self.y = math.sin(self.angle)*self.long
        else:
            self.angle = args['pa'].angle(args['pb'])
            self.long = args['pa'].dist(args['pb'])
            self.x = math.cos(self.angle)*self.long
            self.y = math.sin(self.angle)*self.long
    
    def update(self):
        self.x=math.cos(self.angle)*self.long
        self.y=math.sin(self.angle)*self.long
    
    def pointtoo(self,form:Pos,to:Pos):
        self.angle=form.angle(to)
        self.update()
    
    def __add__(self,other):
        x=self.x+other.x
        y=self.y+other.y
        return Vec(x=x,y=y)
    
    def __sub__(self,other):
        x=self.x-other.x
        y=self.y-other.y
        return Vec(x=x,y=y)
    
    def __mul__(self,other):
        return self.x*other.x+self.y*other.y
    
    def __floordiv__(self,other):
        return Vec(self.x/other,self.y/other)
    
    def __repr__(self):
        return "Vec : %0.2f, %0.2f" % (self.x,self.y)

if __name__=="__main__":
    a=Vec(x=1,y=2)
    b=Vec(long=1,angle=math.tau)
    print(a,b,sep="\n")
else:
    print("Services offerts par votre bien aimé captiane µ")
