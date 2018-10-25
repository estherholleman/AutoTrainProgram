import numpy as np
import pickle
import itertools
from random import randint
import numpy as np
import time
import serial
import os
import csv
import sys

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')




class Recording_App(object):
    def __init__(self, data_type, data=None, main_app = None):
        self.fieldnames = ["trial_nr","flavour", "animal_answer", "reaction_time", "reward_size","additional_reward", "aditional_info"]
        self.thread_finished = False
        self.main_app = main_app
        sys.stdout = StdoutRedirector(main_app.console)
        if data_type == "new":
            #Setup dictionary with names and default values
            self.params = {
                            "name":{"name": "Experiment name", "default":"Project"},
                            "day":{"name":"Number of days", "default":10},
                            "block":{"name":"Block size", "default":20},
                            "block_daily":{"name":"Blocks per day", "default":3},
                            "n_animals":{"name":"Number of animals","default":3},
                            "adress": {"name":"Arduino port","default":"COM9"},
                            "r3_time": {"name": "Max time to get 3 x reward [ms]", "default":0},
                            "r2_time": {"name": "Max time to get 2 x reward [ms]", "default":5000},
                            "r1_time": {"name": "Max time to get 1 x reward [ms]", "default":60000}
                            }
            #Setup order of data (file name should befirst, block should be the last one)        
            self.params["order"] = ["name","adress", "day", "block_daily", "n_animals","block","r1_time", "r2_time", "r3_time"]
            self.params["tastes"] = ["apple","bacon"]
            self.params["protected"] = ["name", "n_animals","block_daily"]
            #Setup names for one block description
            self.params["names"] = ['Day', 'Block number', 'Animal number']
        elif data_type == "path":
            path = data + "/config.pkl"
            self.params = load_obj(path)
            self.n_days = int(self.params["day"]["updated"])
            self.n_blocks = int(self.params["block_daily"]["updated"])
            self.n_animals = int(self.params["n_animals"]["updated"])
            
    def settings_updated(self):
            self.n_days = int(self.params["day"]["updated"])
            self.n_blocks = int(self.params["block_daily"]["updated"])
            self.n_animals = int(self.params["n_animals"]["updated"])
            new_undone = np.ones(self.n_days*self.n_blocks*self.n_animals)
            new_done = np.zeros(self.n_days*self.n_blocks*self.n_animals)
            try:
                x = len(self.params["undone_blocks"])
                for i in range(x):
                    new_undone[i] = self.params["undone_blocks"][i]
                    new_done[i] = self.params["done_blocks"][i]
            except:
                None
            self.params["undone_blocks"] = new_undone 
            self.params["done_blocks"] = new_done
            
    def save(self):
            if not os.path.exists("experiments/"+self.params["name"]["updated"]):
                os.makedirs("experiments/"+self.params["name"]["updated"])
            path = "experiments/"+self.params["name"]["updated"]+ "/config.pkl"
            save_obj(self.params, path)
    
    def genarate_flavors(self, choices = ['apple', 'bacon']):
        in_row = 1
        p_x= randint(0, len(choices)-1)
        choices_list = [p_x]
        while len(choices_list) < int(self.params["block"]["updated"]):
            x = randint(0, len(choices)-1)
            if p_x == x:
                if in_row <3:
                    in_row +=1
                    choices_list.append(x)
                    p_x = x
                else:
                    continue
            else:
                choices_list.append(x)
                p_x = x
                in_row = 1
                
                  # check for number of alternations in a row
            if len(choices_list) > 19:
                d = np.diff(choices_list)
                flavChange = np.nonzero(d)
                nflavChange = len(flavChange[0])
                
                if nflavChange > 10:
                    in_row = 1
                    p_x= randint(0, len(choices)-1)
                    choices_list = [p_x]      
                
        return choices_list 
    
    def upload_settings(self):
        self.sett_uploaded = False
        self.ser = serial.Serial(self.params["adress"]["updated"], 115200, timeout=5)
        time.sleep(2)
        boolean = True
        print 'Connecting to arduino'
        c = 1
        while boolean:
            self.ser.write(str(0))
            ard_message = int(self.ser.readline())
            try:
                if ard_message == 0:
                    boolean = False
            except:
                sys.stdout.write("\r %s attempt (if problem continues, unplug and plug arduino, then run program again)"% c)
                c+=1
        print "Uploading settings:"
        for i in range(3):
            self.ser.write(self.params["r%s_time"%(3-i)]["updated"])
            boolean = True
            c = 1
            while boolean:
                ard_message = int(self.ser.readline())
                try:
                    if ard_message == int(self.params["r%s_time"%(3-i)]["updated"]):
                        print '- ' + "r%s_time"%(3-i) + ' : ' + str(ard_message)
                        boolean = False
                except:
                    sys.stdout.write("\r %s attempt "% c)
                    c+=1
        print "Settings uploaded"
        print 40*'-'
        self.sett_uploaded = True
        
    def send_flavour(self,main,taste, numbers):
        while True:
            try:
                while not self.sett_uploaded:
                    continue
                boolean = True
                c = 1
                while boolean:
                    self.ser.write(str(1))
                    ard_message = int(self.ser.readline())
                    try:
                        if ard_message == 1:
                            boolean = False
                    except:
                        sys.stdout.write("\r %s attempt"% c)
                        c+=1
                c = 1
                boolean = True
                while boolean:
                    self.ser.write(str(taste))
                    ard_message = int(self.ser.readline())
                    try:
                        if ard_message == int(taste):
                            boolean = False
                    except:
                        sys.stdout.write("\r %s attempt"% c)
                        c+=1
                    print "Taste send: " + str(ard_message) + '(' + self.params["tastes"][ard_message] + '). ' + 'Trial in progress'
                    self.main_app.reward.grid(row=4, column=0)
                    self.main_app.trial_cancel.grid(row=5, column=1)
                for i in ["animal_answer","reaction_time","reward_size"]:
                    boolean = True
                    c = 1
                    while boolean:
                        ard_message = self.ser.readline()
                        try:
                            ard_message = int(ard_message)
                            print i + ' : ' + str(ard_message)
                            main.trial_info[i] = int(ard_message)
                            boolean = False
                        except:
                            c+=1
                print 40*'-'
                break
            except:
                print "Trial failed! Program will retry do connect with arduino"
                self.ser.close()                
                self.upload_settings()
                print 40*'-'
        main.after_thread()
    
    def give_additional_reward(self,taste):
        print 40*'-'
        boolean = True
        c = 1
        while boolean:
            self.ser.write(str(2))
            break
        print "Additional food applied"
        print 40*'-'
        
    def cancel_trial(self,taste):
        print 40*'-'
        boolean = True
        c = 1
        while boolean:
            self.ser.write(str(3))
            break
        print "Trial canceled"
        print 40*'-'
        
    def save_trial(self,trial_info):
        numbers = trial_info["parameters"]
        new_path = "experiments/"+self.params["name"]["updated"]+ '/trial_data/Day_{}/Block_{}'.format(numbers[0], numbers[1])
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if trial_info["nr"] == 1 :
            with open(new_path+'/Animal_{}.csv'.format(numbers[2]), 'wb') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, quoting=csv.QUOTE_NONE,escapechar=' ')
                writer.writeheader()
                writer.writerow({
                                "trial_nr":trial_info["nr"], "flavour": trial_info["taste"], "animal_answer": trial_info["animal_answer"],
                                "reaction_time": trial_info["reaction_time"], "reward_size":trial_info["reward_size"],
                                "additional_reward": trial_info["additional_reward"], "aditional_info": trial_info["additional_info"]})    
        else:
            with open(new_path+'/Animal_{}.csv'.format(numbers[2]), 'ab') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, quoting=csv.QUOTE_NONE,escapechar=' ')
                writer.writerow({
                                "trial_nr":trial_info["nr"], "flavour": trial_info["taste"], "animal_answer": trial_info["animal_answer"],
                                "reaction_time": trial_info["reaction_time"], "reward_size":trial_info["reward_size"],
                                "additional_reward": trial_info["additional_reward"], "aditional_info": trial_info["additional_info"]})    
    
    
    
    
    
    
    
    
    
    
    
    def load_block_results(self,numbers):
        block_results = []
        path = "experiments/"+self.params["name"]["updated"]+ '/trial_data/Day_{}/Block_{}//Animal_{}.csv'.format(
        numbers[0], numbers[1],numbers[2])
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                block_results.append([row[el] for el in self.fieldnames])
        return block_results
        
    def calculate_error(self, numbers):
        TP = 0.
        TN = 0.
        FP = 0.
        FN = 0.
        block_results = self.load_block_results(numbers)
        for trial in block_results:
            if trial[1] == '1' and trial[2] == '1':
                TP+=1
            elif trial[1] == '0' and trial[2] == '0':
                TN+=1
            elif trial[1] == '1' and trial[2] == '0':
                FN+=1
            elif trial[1] == '0' and trial[2] == '1':
                FP+=1
        stats = [(TP+TN)/(TP+TN+FP+FN),TP/(TP+FN),TN/(FP+TN),TN/(TN+FN),TP/(TP+FP)]
        return stats
        
        
        
def save_obj(obj, path):
    with open( path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            
def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

