#!/usr/bin/python

from Tkinter import *
import tkMessageBox as box

class Application(Frame):
    def dropdown(self):
        #print "Value is ", self.text.get()
        if self.text.get() == "Bleed Damage" or self.text.get() == "Burning Damage" or self.text.get() == "Poison Damage" or self.text.get() == "Confusion Damage":
            self.leveltext.grid(column=0, row=1)
            self.level.grid(column=1, row=1)
            self.conddamtext.grid(column=0, row=2)
            self.conddam.grid(column=1, row=2)
            self.submit.grid_forget()
            self.submit2.grid(column=0, row=4)
            self.equations.grid(column=1, row=4)
            self.precisiontext.grid_forget()
            self.precision.grid_forget()
        elif self.text.get() == "Critical Chance":
            self.leveltext.grid(column=0, row=1)
            self.level.grid(column=1, row=1)
            self.precisiontext.grid(column=0, row=2)
            self.precision.grid(column=1, row=2)
            self.submit.grid_forget()
            self.submit2.grid(column=0, row=4)
            self.equations.grid(column=1, row=4)
            self.conddam.grid_forget()
            self.conddamtext.grid_forget()
    def createWidgets(self):
        #Enter level for stuff
        self.leveltext = Label(self, text="Level")
        self.level = Entry(self, bd=5)
        
        #Enter cond damage for stuff
        self.conddamtext = Label(self, text="Condition Damage")
        self.conddam = Entry(self, bd=5)
        
        #Enter precision for stuff
        self.precisiontext = Label(self, text="Precision")
        self.precision = Entry(self, bd=5)

        #option menu
        self.text = StringVar()
        self.text.set("Select one")
        self.option = OptionMenu(self, self.text, "Bleed Damage", "Burning Damage", "Poison Damage", "Confusion Damage", "Critical Chance")
        
        #Submit Button
        self.submit = Button(self)
        self.submit['text'] = "Submit",
        self.submit['command'] = self.dropdown
        
        #Submit Button
        self.submit2 = Button(self)
        self.submit2['text'] = "Reset",
        self.submit2['command'] = self.dropdown
        
        #second Submit Button
        self.equations = Button(self)
        self.equations['text'] = "Submit",
        self.equations['command'] = self.runequations

        self.option.grid(column=1, row=3)
        self.submit.grid(column=1, row=4)
        
    def runequations(self):
        if self.text.get() == "Bleed Damage":
            try:
                level = int(self.level.get())
            except ValueError:
                level = 0
            try:
                cond = int(self.conddam.get())
            except ValueError:
                cond = 0
            if level == 0 or cond == 0:
                box.showerror("Incorrect Values", "Could not get correct values. Please re-enter correct values into boxes (only numbers).")
            else:
                #condequation = 2.5*(0.5*level)+(0.05*cond)
                condequation = 0.05*cond+0.5*level+2.5
                bleedmessage = "You will do "+str(condequation)+" damage per second for each bleed you apply."
                box.showinfo("Bleed Damage", bleedmessage)
        elif self.text.get() == "Burning Damage":
            try:
                level = int(self.level.get())
            except ValueError:
                level = 0
            try:
                cond = int(self.conddam.get())
            except ValueError:
                cond = 0
            if level == 0 or cond == 0:
                box.showerror("Incorrect Values", "Could not get correct values. Please re-enter correct values into boxes (only numbers).")
            else:
                condequation = 0.25*cond+4.0*level+8
                burningmessage = "You will do "+str(condequation)+" damage per second for burning."
                box.showinfo("Burning Damage", burningmessage)
        elif self.text.get() == "Poison Damage":
            try:
                level = int(self.level.get())
            except ValueError:
                level = 0
            try:
                cond = int(self.conddam.get())
            except ValueError:
                cond = 0
            if level == 0 or cond == 0:
                box.showerror("Incorrect Values", "Could not get correct values. Please re-enter correct values into boxes (only numbers).")
            else:
                condequation = 0.10*cond+1.0*level+4
                poisonmessage = "You will do "+str(condequation)+" damage per second for Poison."
                box.showinfo("Poison Damage", poisonmessage)
        elif self.text.get() == "Confusion Damage":
            try:
                level = int(self.level.get())
            except ValueError:
                level = 0
            try:
                cond = int(self.conddam.get())
            except ValueError:
                cond = 0
            if level == 0 or cond == 0:
                box.showerror("Incorrect Values", "Could not get correct values. Please re-enter correct values into boxes (only numbers).")
            else:
                condequation = 0.15*cond+1.5*level+10
                condequationpvp = condequation/2
                confusionmessage = "You will do "+str(condequation)+" damage per skill use for confusion.\n You will do "+str(condequationpvp)+" damage per skill use for confusion in WvW and sPvP"
                box.showinfo("Confusion Damage", confusionmessage)
        elif self.text.get() == "Critical Chance":
            try:
                level = int(self.level.get())
            except ValueError:
                level = 0
            try:
                precision = int(self.precision.get())
            except ValueError:
                precision = 0
            if level == 0 or precision == 0:
                box.showerror("Incorrect Values", "Could not get correct values. Please re-enter correct values into boxes (only numbers).")
            else:
                baseprecision = round(0.1*(level*level)+3.162*level+21.89)
                critchanceequation = ((precision-baseprecision)/21)*4
                critchancemessage = "You have a "+str(critchanceequation)+"% chance to get a critical hit."
                box.showinfo("Critical Change", critchancemessage)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.master.title("Guild Wars 2 Equations")
app.master.minsize(100,200)
app.master.geometry("500x300")
app.mainloop()
root.destroy()