#math
k=9*10**9
from charges import Point, Line

def calcv(point, pos, q):
	"""
	calculates voltage at a point generated by a single charge
	"""
	r=dist(point, pos)
	if r<.005: return 0.0
	return k*q/r

def calce(point, pos, q):
	r=dist(point, pos)
	if r<.005: return (0,0,0)
	sc=k*q/r**3 #scale factor
	a=point[0]-pos[0]
	b= point[1]-pos[1]
	c= point[2]-po2[2]
	return [sc*a, sc*b, sc*c]
	

def dist(p1, p2):
	"""
	calculates distance between points
	"""
	tot=0.0
	for i in range(len(p1)):
		tot+= (p1[i] -p2[i])**2
	return tot**.5

def vAtPoint(p, charges):
	v=0
	for c in charges:
		if isinstance(c, Point):
			v+=calcv(p, c.pos, c.charge)
		elif isinstance(c, Line):
			for x,y,z,q in zip(c.x, c.y, c.z, c.lam):
				v+=calcv(p, (x,y,z),q)
	return v
	
def eAtPoint(p, charges):
	e=[0,0,0]
	for c in charges:
		if isinstance(c, Point):
			f=calce(p, c.pos, c.charge)
			for i in range(len(e)):
				e[i]+=f[i]
		elif isinstance(c, Line):
			for x,y,z,q in zip(c.x, c.y, c.z, c.charge):
				f=calce(p, (x,y,z),q)
				for i in range(len(e)):
					e[i]+=f[i]
	return e
