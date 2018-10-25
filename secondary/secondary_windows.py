from Tkinter import *
import Tkinter,tkFileDialog
import ttk as ttk
import numpy as np
import os


class browse_window:       

	def __init__(self, root):
		self.root = root
		Label(self.root, text="""Choose project:""",justify = LEFT, padx = 20).pack()
		self.tree = ttk.Treeview(self.root)
		self.tree.pack()
		projects = next(os.walk('experiments/'))[1]
		for ix, key in enumerate(projects):
			self.tree.insert("","end", text=projects[ix])
		
		self.tree.bind("<Double-1>", self.OnDoubleClick)
			
	def OnDoubleClick(self, event):
		item = self.tree.selection()[0]
		self.path = "experiments/" + self.tree.item(item,"text")
		self.root.quit()
		self.root.destroy()

class settings_window():       

	def __init__(self, root, experiment, edit = False):     
		#Browse Bar
		self.experiment = experiment
		self.root = root
		self.path = ''
		self.params = self.experiment.params
		projects = next(os.walk('experiments/'))[1]
		protected = self.experiment.params["protected"]
		if not edit:
			if self.params["name"]["default"] in projects:
				free = False
				n = 1
				while not free:
					if self.params["name"]["default"] + '('+ str(n) +')' in projects:
						n+=1
					else:
						self.params["name"]["default"] += '('+ str(n) +')' 
						free = True
		self.cb = []
		self.cb_v = []
		for ix, key in enumerate(self.experiment.params["order"]):
			label = Label(self.root, justify = LEFT, text=self.params[key]["name"],anchor=W).grid(row=ix+1, column=0)
			self.cb_v.append(StringVar())
			try:
				self.cb_v[ix].set(self.params[key]["updated"])
			except:
				self.cb_v[ix].set(self.params[key]["default"])
			self.cb.append(Entry(self.root, textvariable=self.cb_v[ix]))
			self.cb[ix].grid(row=ix+1, column=1)
			if (edit and key in protected):
				self.cb[ix].configure(state='disabled')
		self.cbutton= Button(self.root, text="Save", command=self.save_file).grid(row=len(self.params)+1, column=2, sticky = W + E)
	
	def save_file(self):
		for ix, key in enumerate(self.experiment.params["order"]):
			self.params[key]["updated"] = self.cb_v[ix].get()
		self.root.quit()
		self.root.destroy()

class block_window:
	
	def __init__(self, root, experiment, choices):
		self.root = root
		self.experiment = experiment
		self.n = 0
		self.v=[]
		keys = self.experiment.params["order"][2:5]
		self.maxi = [int(self.experiment.params[key]["updated"]) for key in keys]
		self.names = self.experiment.params["names"]
		Label(self.root, text="""Choose the day, block and animal:""",justify = LEFT, padx = 20).pack()
		self.tree = ttk.Treeview(self.root)
		self.tree.pack()
		j = 0
		k = 0
		l = 0
		for i,n in enumerate(choices):
			l+=1
			if i%(len(choices)/self.maxi[0]) == 0:
				k = 0
				j += 1
				if np.sum(choices[i:i+len(choices)/self.maxi[0]]) != 0:
					self.tree.insert("",j,"d%s"%(j), text="Day %s" % (j))
			if i%self.maxi[2] == 0:
				l = 1
				k += 1
				if np.sum(choices[i:i+self.maxi[2]]) != 0:
					self.tree.insert("d%s" %(j),j, "b%s" % (i/self.maxi[2]), text="Block %s" % (k))
			if n == 1:
				self.tree.insert("b%s" %(i/self.maxi[2]),j, "%s" % (i), text="Animal %s" % (l))

		self.tree.bind("<Double-1>", self.OnDoubleClick)

	def OnDoubleClick(self, event):
		item = self.tree.selection()[0]
		if self.tree.item(item,"text")[:6] == "Animal":
			self.clicked = item
			self.root.quit()
			self.root.destroy()
