#control panel
from threading import Thread
from Gui import *
from time import sleep
from charges import *
from emmath import *

class Panel2(Thread):
	def __init__(self,field):
		Thread.__init__(self)
		self.field=field
		self.field.panel=self
		self.activeCharge=None
		self.sel=None
		self.g=None

	def run(self):
		self.g=Gui()
		self.g.title('Control Panel')

		#charge
		self.chgla=self.g.la(text='Charge')
		self.g.gr(cols=3)
		minus=self.g.bu(text='-', command=Callable(self.addC, -1))
		self.chg=self.g.en()
		plus=self.g.bu(text='+', command=Callable(self.addC, 1))
		self.g.endgr()

		#position
		self.pos=self.g.la(text='Position')
		self.g.gr(cols=3)
		xla=self.g.la(text='x')
		yla=self.g.la(text='y')
		zla=self.g.la(text='z')
		self.x=self.g.en(text='')
		self.y=self.g.en(text='')
		self.z=self.g.en(text='')
		self.g.endgr()
		#menu
		self.men=self.g.mb(text='Change/ Add Charge')
		hi=self.g.mi(self.men, text='Add point charge', command=Callable(self.addPoint))
		self.g.mi(self.men, text='Add line charge', command=Callable(self.addLine))
		self.g.mi(self.men, text='Find voltage at point', command=self.findVolt)

		
		#add
		self.g.row([1,1])
		self.add=self.g.bu(text='Add')
		self.rem=self.g.bu(text='Delete', command=self.remove)
		self.g.endrow()
		#self.g.bu(text='Quit', command=self.end)
		
		self.disp=self.g.mb(text='Voltage Field')
		self.g.mi(self.disp, text='Voltage Field', command=self.showv)
		self.g.mi(self.disp, text='Electric Field', command=self.showe)
		#ans
		self.ans=self.g.la(text='')

		
		self.field.start()
		for chrg in self.field.charges:
			chrg.makeMi()
		self.g.mainloop()
		
	def showv(self):
		self.disp.config(text='Voltage Field')
		self.actf=self.field.vfield
		self.acte=self.field.vdots
		self.field.change=True
		for p in self.field.earrows:
			self.field.earrows[p].visible=False
		for p in self.field.vdots:
			self.field.vdots[p].visible=True
	def showe(self):
		self.disp.config(text='Electric Field')
		self.field.actf=self.field.efield
		self.field.acte=self.field.earrows
		self.field.change=True
		for p in self.field.earrows:
			self.field.earrows[p].visible=True
		for p in self.field.vdots:
			self.field.vdots[p].visible=False
		
	def addPoint(self):
		self.men.config(text='Add Point')
		self.pos.config(text='Position')
		self.add.config(command=Callable(self.addPCharge))
		
	def addLine(self):
		self.men.config(text='Add Line')
		self.pos.config(text='Equation in terms of t')
		self.add.config(command=Callable(self.addLCharge))
		self.field.change=True
		
	def addPCharge(self):
		pos=(int(self.x.get()), int(self.y.get()), int(self.z.get()))
		c=float(self.chg.get())
		p=Point(pos=pos, charge=c)
		self.addCharge(p)

	def addLCharge(self):
		eqn=(self.x.get(), self.y.get(), self.z.get())
		dens=self.chg.get()
		p=Line(eqn=eqn, density=dens)
		self.addCharge(p)


	def addCharge(self,p):
		self.field.charges.append(p)
		self.field.change=True
		p.panel=self
		p.makeMi()
		
	def findVolt(self):
		self.add.config(text='Get Voltage', command=self.getVolt)

	def getVolt(self):
		p=(int(self.x.get()), int(self.y.get()), int(self.z.get()))
		v=vAtPoint(p, self.field.charges)
		self.ans.config(text='Voltage at (%d, %d, %d): %g k'%(p[0],p[1],p[2],v))

		
	def remove(self):
		if not self.sel: return
		c=self.sel
		i=self.field.charges.index(c)
		self.men.menu.delete(i+3)
		self.field.charges.remove(c)
		c.s.visible=False
		del(c)
		self.field.change=True
		self.sel=None
		
	def select(self, charge):
		if self.sel: self.sel.revert()
		self.sel=charge
		charge.s.color=(1,1,1)
		self.updateLa()
		self.add.config(text='Update', command=Callable(self.update))

	def update(self):
		ch=self.chg.get()
		x,y,z=self.x.get(), self.y.get(), self.z.get()
		if len(ch)>0:
			self.sel.updateCharge(ch)
		self.updatePos(x,y,z)
		self.sel.updateMi()
		self.field.change=True
			

	def updateLa(self):
		self.chgla.config(text='Charge: %s'%str(self.sel.charge))
		p=self.sel.pos
		self.pos.config(text='Position: (%s, %s, %s)'%(str(p[0]), str(p[1]), str(p[2])))

	def addC(self, n):
		if not self.sel: return
		if isinstance(self.sel, Point):
			self.sel.charge+=n
		elif isinstance(self.sel, Line):
			self.sel.charge+=str(n)
		self.field.change=True
		self.updateLa()

	def updatePos(self, x,y,z):
		if not self.sel: return
		self.sel.updatePos(x,y,z)

	def end(self):
		self.field.go=False
		

