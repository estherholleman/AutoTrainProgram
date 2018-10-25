from Tkinter import *
import tkMessageBox
from secondary.secondary_windows import *
from secondary.experiment import *
import tkFont
import os
import thread
import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class Main_Application(Frame):
    
    
    def __init__(self, root):
        """Setting up all buttons used and frames used in application (hidden and visible)"""
        #Set up filemenu
        self.root = root
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New project", command=self.new_project)
        self.filemenu.add_command(label="Open project", command=self.open_project)
        self.menubar.add_cascade(label="Projects", menu=self.filemenu)
        self.root.config(menu=self.menubar)
        self.root.title("Experimenter 0.9")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Setup Tabs
        self.manager = ttk.Notebook(self.root)
        self.Start_Tab = ttk.Frame(self.manager)
        self.E_Tab = ttk.Frame(self.manager)
        self.S_Tab = ttk.Frame(self.manager)
        #Setup start tab
        self.manager.add(self.Start_Tab, text='General info')
        self.TitleFont = tkFont.Font(family="Times", size=16,weight="bold")
        self.g1 = Label(self.Start_Tab, text='Welcome to the Experimenter',justify = CENTER, width = 70, height=5,font=self.TitleFont).pack()
        self.customFont = tkFont.Font(family="Times", size=12,weight="bold")
        instr = "To start create a new project or load saved one from the menu Projects."
        self.g2 = Label(self.Start_Tab, text=instr,justify = CENTER, width = 70, height=5,font=self.customFont).pack()
        #Setup all features used in experimenter tab
        self.setup_exerimenter()
        self.manager.add(self.E_Tab, text='Experimenter Tab',state='disabled')
        #Setup analysis tab
        self.manager.add(self.S_Tab, text='Analysis Tab',state='disabled')
        self.manager.pack(expand=1, fill="both")
    
    def setup_exerimenter(self):
        """
        Function for setting up experimenter tab
        """
        Frame2 = Frame(self.E_Tab)
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)    
        
        self.Dialog = Frame(self.E_Tab)
        self.dia1 = Label(self.Dialog, text='',bg="grey",justify = LEFT,anchor=NW, width = 70, height=5)
        self.dia2 = Label(self.Dialog, text='',bg="grey",justify = LEFT,anchor=NW, width = 70, height=2)
        self.dia3 = Label(self.Dialog, text='',bg="grey",justify = LEFT,anchor=NW, width = 70, height=2)
        self.dia4 = Label(self.Dialog, text='',bg="grey",justify = LEFT,anchor=NW, width = 70, height=16)
        self.start = Button(self.Dialog, text="START BLOCK", command=lambda: self.start_block())
        self.edit= Button(self.Dialog, text="CHANGE BLOCK", command=self.choose_block)
        self.overwrite = Button(self.Dialog, text="CHANGE & OVERWRITE", command=self.overwrite_block)
        
        self.cont= Button(self.Dialog, text="CONTINUE TO 2 TRIAL", command=lambda: self.next_trial())
        self.finish = Button(self.Dialog, text="FINISH BLOCK", command=lambda: self.finish_block())
        self.reward = Button(self.Dialog, text="ADDITIONAL FOOD", command=lambda: self.add_reward())
        self.trial_cancel = Button(self.Dialog, text="CANCEL TRIAL", command=lambda: self.cancel_trial())
        self.additional_l = Label(self.Dialog, justify = LEFT, text="Aditional info:",anchor=NW)
        self.additional_v = StringVar()
        self.additional_e = Text(self.Dialog, width = 50, height=4)
        
        self.Settings = Frame(self.E_Tab)
        self.Settings.grid(row = 0, column = 3, rowspan = 6, columnspan = 2, sticky = W+E+N+S)
        self.S = Label(self.Settings, text="Settings", width = 50)
        self.change_S = Button(self.Settings, text="CHANGE SETTINGS", command=lambda: self.change_settings())
        self.sync = Button(self.Settings, text="SYNCHRONIZE ARDUINO", command=lambda: self.setup())
        self.console = Text(self.Settings,width = 40, height=10)
        self.console.config()
        self.scrl = Scrollbar(self.Settings, command=self.console.yview)
        self.console.config(yscrollcommand=self.scrl.set)
        #Experimenter variables
        
        
    def setup_analysis(self):
        """
        Function for setting up analisis tab
        """
        stat_matrix = []
        for an in range(1):
            for n_ in range(len(self.params["done_blocks"])/self.experiment.n_animals):
                n = n_*self.experiment.n_animals +an
                if self.params["done_blocks"][n] == 1:
                    numbers = [n/(self.experiment.n_blocks*self.experiment.n_animals)%self.experiment.n_days +1,
                                n/self.experiment.n_animals%self.experiment.n_blocks+1,n%self.experiment.n_animals+1]
                    stat_matrix.append(self.experiment.calculate_error(numbers))
        stat_matrix = np.array(stat_matrix).T
        f = Figure(figsize=(10,8), dpi=100)
        for i in range(3):
            a = f.add_subplot(3,1,i)
            a.plot(stat_matrix[i],'*-')
            a.set_xlim(-0.5, len(stat_matrix[i])+0.5)
        try:
            self.c_widget.destroy()
            self.canvas = FigureCanvasTkAgg(f, master=self.S_Tab)
        except:
            self.canvas = FigureCanvasTkAgg(f, master=self.S_Tab)
        self.canvas.show()
        self.c_widget = self.canvas.get_tk_widget()
        self.c_widget.pack()
                    
        
    def new_project(self):
        """
        Creates new project
        """
        # Open dialog and save params to self.params
        self.experiment = Recording_App("new",main_app = self)
        temp_root = Toplevel()
        sub_app = settings_window(temp_root, self.experiment)
        temp_root.mainloop()
        self.params = sub_app.params
        # Update and save settings, prepare app for project
        self.experiment.settings_updated()
        self.experiment.save()
        self.setup()
        
    def open_project(self):
        """
        Opens existing project
        """
        temp_root = Toplevel()
        sub_app = browse_window(temp_root)
        temp_root.mainloop()
        self.path = sub_app.path
        self.experiment = Recording_App("path", self.path, main_app = self)
        self.params = self.experiment.params
        self.setup()
        #self.setup_analysis()
    
    def on_closing(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.experiment.ser.close()
            except:
                None
            root.destroy()
    
    def change_settings(self):
        """enables change of not protected settings"""
        temp_root = Toplevel()
        sub_app = settings_window(temp_root, self.experiment, edit = True)
        temp_root.mainloop()
        self.params = sub_app.params
        self.experiment.settings_updated()
        self.experiment.save()
        self.setup()
    
    
    def setup(self):
        """
        Function prepares aplication for current project
        """
        #Reset current block id
        self.block_id = 0
        #Enable tabs
        self.manager.tab(self.E_Tab, state='normal')
        self.manager.tab(self.S_Tab, state='normal')
        #Set up massage dialog
        self.Dialog.grid(row = 0, column = 0, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
        self.dia1.grid(row=0, column=0,columnspan = 3)
        self.dia1.config(text=self.block_info())
        self.dia2.grid(row=1, column=0,columnspan = 3)
        self.dia2.config(text ='')
        self.dia3.grid(row=2, column=0,columnspan = 3)
        self.dia3.config(text = '')
        self.dia4.grid(row=3, column=0,columnspan = 3)
        self.dia4.config(text = '')
        #Set up buttons
        self.start.grid(row=4, column=0, sticky = W + E)
        self.edit.grid(row=4, column=1)
        self.overwrite.grid(row=4, column=2)
        #Set up settings info
        self.S.grid(row=0, column=0,columnspan = 2)
        l_list=[]
        for ix, key in enumerate(self.experiment.params["order"]):
            l_list.append(Label(self.Settings, justify = LEFT, anchor=W, width = 30, text=self.params[key]["name"]))
            l_list[-1].grid(row=ix+1, column=0,sticky = W)
            l_list.append(Label(self.Settings, justify = LEFT,anchor=W, width = 20, text=self.params[key]["updated"]))
            l_list[-1].grid(row=ix+1, column=1,sticky = W)
        self.change_S.grid(row=ix+2, column=0)
        self.sync.grid(row=ix+2, column=1)
        self.console.grid(row=ix+3, column=0, columnspan = 2)
        self.scrl.grid(row=ix+3, column=2, sticky='ns')
        try:
            self.experiment.ser.close()
        except:
            None
        try:
            ser = serial.Serial(self.params["adress"]["updated"], 115200, timeout=5)
            ser.close()
            arduino = True
        except:
            arduino = False
        if arduino:
            thread.start_new_thread(self.experiment.upload_settings,())
        else:
            print 'Arduino not found! Plug it in and press SYNCHRONIZE ARDUINO button'
            print 40*'-'
        
    def block_info(self, edit = False):
        '''
        takes boolean parameter "edit". 
        edit = False: function prepare block info for first not 
        started block
        edit = True: function prepare block info for selected block
        '''
        string = 'Current block info:\n'
        names = self.experiment.params["names"]
        if not edit:
            for n in range(self.block_id,len(self.params["undone_blocks"])):
                if self.params["undone_blocks"][n] == 1:
                    break
        else:
            n = self.block_id    
        if self.params["undone_blocks"][n] == 2:
            self.dia2.config(text = 'Block started but not finished!',bg = 'grey',justify = LEFT,anchor=NW)
        self.numbers = [n/(self.experiment.n_blocks*self.experiment.n_animals)%self.experiment.n_days +1,
                    n/self.experiment.n_animals%self.experiment.n_blocks+1,n%self.experiment.n_animals+1]
        for i,el in enumerate(self.experiment.params["order"][1:4]):
            string+=names[i]+'   :   ' + str(self.numbers[i]) + '\n'
        self.block_id = n
        return string
    
    def start_block(self):
        '''
        Function starts selected block
        '''
          #Saves the fact that the block is started
        self.params["undone_blocks"][self.block_id] = 2
        self.params["done_blocks"][self.block_id] = 1
        self.experiment.save()
        #Hide buttons
        self.start.grid_forget()
        self.edit.grid_forget()
        self.overwrite.grid_forget()
        #Generate flavors for one block
        self.block_list = self.experiment.genarate_flavors()
        ###Setup recurence button up to n = len(block_list)
        self.n=1
        self.run_trial()
    
    def run_trial(self):
        self.reward.grid_forget()
        self.trial_cancel.grid_forget()
        self.additional_l.grid_forget()
        self.additional_e.grid_forget()
        self.additional_reward = 0
        self.trial_info = {}
        if self.block_list[self.n-1] == 0:
            self.dia2.config(text = "TRIAL NR "+str(self.n) +" "+ self.params["tastes"][0],bg = 'green')
        else:
            self.dia2.config(text = "TRIAL NR "+str(self.n) +" "+ self.params["tastes"][1],bg = 'brown')
        if self.n<len(self.block_list):
            if self.block_list[self.n] == 0:
                self.dia3.config(text = "NEXT TASTE " +  self.params["tastes"][0],bg = 'green')
            else:
                self.dia3.config(text = "NEXT TASTE " + self.params["tastes"][1],bg = 'brown')
        else:
            self.dia3.config(text ="No more trials", bg = 'grey')
        self.cont.grid_forget()
        thread.start_new_thread(self.experiment.send_flavour,(self, self.block_list[self.n-1],self.numbers))
    
    def after_thread(self):
        if self.n==int(self.params["block"]["updated"]):
            self.additional_l.grid(row=4, column=0)
            self.additional_e.grid(row=4, column=1)
            self.finish.grid(row=4, column = 2)
        else:
            self.cont.config(text= "CONTINUE TO %s TRIAL"%(self.n+1))
            self.cont.grid(row=4, column=2)
        self.additional_l.grid(row=5, column=0)
        self.additional_e.grid(row=6, column=0)
    
    def save_trial_dict(self):
        self.trial_info["nr"] = self.n
        self.trial_info["parameters"] = self.numbers
        self.trial_info["taste"] = self.block_list[self.n-1]
        self.trial_info["additional_reward"] = self.additional_reward
        self.trial_info["additional_info"] = self.additional_e.get('1.0', 'end')
        self.additional_e.delete('1.0', 'end')
        self.experiment.save_trial(self.trial_info)
    
    def next_trial(self):
        """prepares the gui for the next trial"""
        self.save_trial_dict()
        self.n+=1
        self.run_trial()
    
    
    def finish_block(self):
        self.trial_cancel.grid_forget()
        self.save_trial_dict()
        self.start.grid(row=4, column=0, sticky = W + E)
        self.edit.grid(row=4, column=1)
        self.overwrite.grid(row=4, column=2)
        self.finish.grid_forget()
        self.additional_l.grid_forget()
        self.additional_e.grid_forget()
        self.reward.grid_forget()
        self.n = 0
        self.params["undone_blocks"][self.block_id] = 0
        self.params["done_blocks"][self.block_id] = 1
        self.dia2.config(text = 'Block finished! Press START to begin next block or press EDIT to change current block',bg = 'grey',justify = LEFT,anchor=NW)
        #self.summary(self.block_id)
        self.dia1.config(text = self.block_info())
        self.experiment.save()
        #self.setup_analysis()
    
    
    def add_reward(self):
        self.additional_reward +=1
        thread.start_new_thread(self.experiment.give_additional_reward,(self.block_list[self.n-1],))
        
    def cancel_trial(self):
        thread.start_new_thread(self.experiment.cancel_trial,(self.block_list[self.n-1],))
    
    def choose_block(self):
        temp_root = Toplevel()
        sub_app = block_window(temp_root, self.experiment, self.params["undone_blocks"])
        temp_root.mainloop()
        self.block_id = int(sub_app.clicked)
        self.dia1.config(text = self.block_info(edit = True))
    
    def overwrite_block(self):
        temp_root = Toplevel()
        sub_app = block_window(temp_root, self.experiment, self.params["done_blocks"])
        temp_root.mainloop()
        self.block_id = int(sub_app.clicked)
        self.dia1.config(text = self.block_info(edit = True))
    
    def summary(self, n):
        names = self.experiment.params["names"]
        summary = 'Previous block info:\n'
        for i,el in enumerate(self.experiment.params["order"][1:4]):
            summary+=names[i]+'   :   ' + str(self.numbers[i]) + '\n'
        self.numbers = [n/(self.experiment.n_blocks*self.experiment.n_animals)%self.experiment.n_days +1,
                    n/self.experiment.n_animals%self.experiment.n_blocks+1,n%self.experiment.n_animals+1]
        summary += '\nAnimal accuracy:\n'
        summary += 'Accuracy: {}\nSensitivity: {}\nSpecificity : {}\nPrecision apple: {}\nPrecision bacon: {}\n'.format(*self.experiment.calculate_error(self.numbers))
        self.dia3.config(text=summary)
        
    def donothing(self):
       filewin = Toplevel(self.root)
       button = Button(filewin, text="Do nothing button")
       button.pack()


root = Tk()
App = Main_Application(root)
root.mainloop()

