#!/usr/bin/python
#
# CalAMarRes - Calculadora Automatica para Ressonancia Magnetica
#              (Portuguese for Automatic MR calculator ;)
#
# Calculates Normalized Signal (or Attenuation factor)
# from given Tissue (T1/T2/PD) and Sequence (TE/TR) parameters
# using the formula PD * exp(-TE/T1) * (1-exp(-(TR-TE)/T1))
#
# just a little programming exercise that uses Text input, Buttons and sliders
#
# License GPL
# 

from math import exp;

try:
    # Python2
    import Tkinter as tk;
except ImportError:
    # Python3
    import tkinter as tk;

# predefined Tissue Parameters 
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2822798/
#
# CSF
T1_CSF_def = 4000; 
T2_CFS_def = 2470; 
PD_CSF_def = 0.97;
#
T1_GM_def  = 1034; 
T2_GM_def  = 93;   
PD_GM_def  = 0.78;
#
T1_WM_def  = 660; 
T2_WM_def  = 73;  
PD_WM_def  = 0.65;

# to reproduce the LCModel attenuation factor of 0.7 
# valid for WM, PRESS TE=30-35ms
#
# T1 = 660
# T2 = 80
# PD = 1.0 (LCModel takes this into account in WCONC)
# TE = 30
# TR = 4000
# should give ATT = 0.6857
#

    
# predefined initial Sequence parameters
#
TE_def = 30;
TR_def = 2000



class CalAMaRes(tk.Frame):
    def __init__(self, parent=tk.Tk()):
        tk.Frame.__init__(self, parent);
        self.parent = parent;
        self.parent.title('CalAMarRes');
        # variable Definition & Initialization
        self.T1_value=T1_WM_def; self.T1_text = tk.IntVar(); self.T1_text.set(self.T1_value);
        self.T2_value=T2_WM_def; self.T2_text = tk.IntVar(); self.T2_text.set(self.T2_value); 
        self.PD_value=PD_WM_def; self.PD_text = tk.IntVar(); self.PD_text.set(self.PD_value);
        self.TE = tk.IntVar(); self.TE.set(TE_def);
        self.TR = tk.IntVar(); self.TR.set(TR_def);
        self.ATT = tk.IntVar();
        # tk.Scale sider for TE 
        self.TE_scale = tk.Scale(self.master,
            command=self.Update,
            variable=self.TE,
            from_=0, to=300, resolution=1,
            length=500, tickinterval=20,
            showvalue='yes', 
            orient='horizontal');
        self.TE_scale.set(self.TE.get());
        self.TE_Label = tk.Label(self.master, text='TE');
        # tk.Scale sider for TR
        self.TR_scale = tk.Scale(self.master,
            command=self.Update,
            variable=self.TR,
            from_=0, to=6000, resolution=1, 
            length=500, tickinterval=500, 
            showvalue='yes', 
            orient='horizontal');
        self.TR_scale.set(self.TR.get());
        self.TR_Label = tk.Label(self.master, text='TR');
        # tk.Label Names for Entry
        self.T1_Label = tk.Label(self.master, text='T1'); 
        self.T2_Label = tk.Label(self.master, text='T2'); 
        self.PD_Label = tk.Label(self.master, text='PD');
        # tk.Entry for T1, T2, PD
        self.T1_Entry = tk.Entry(self.master, textvariable=self.T1_text, validate="key", 
                        validatecommand=(self.register(self.validateT1), '%d', '%i', '%P', '%s'));      
        self.T2_Entry = tk.Entry(self.master, textvariable=self.T2_text, validate="key", 
                        validatecommand=(self.register(self.validateT2), '%d', '%i', '%P', '%s'));
        self.PD_Entry = tk.Entry(self.master, textvariable=self.PD_text, validate="key", 
                        validatecommand=(self.register(self.validatePD), '%d', '%i', '%P', '%s'));
        # bind arrow keys on Entry(s)
        def FocusT1(event): self.T1_Entry.focus();
        def FocusT2(event): self.T2_Entry.focus();
        def FocusPD(event): self.PD_Entry.focus();
        self.T1_Entry.bind('<Down>', FocusT2);
        self.T2_Entry.bind('<Down>', FocusPD);
        self.T2_Entry.bind('<Up>',   FocusT1);
        self.PD_Entry.bind('<Up>',   FocusT2);
        # tk.Button for reset buttons
        self.WM_button  = tk.Button(self.master, text="WM",  font=('', 26), command=self.WM_reset);
        self.GM_button  = tk.Button(self.master, text="GM",  font=('', 26), command=self.GM_reset);
        self.CSF_button = tk.Button(self.master, text="CSF", font=('', 26), command=self.CSF_reset);
        # tk.Label to show result
        self.ATT_Label = tk.Label(self.master, font=('', 26), textvariable=self.ATT);
        # Layout
        # ---------------------
        # | L | E | B | B | B |
        # | L | E | ^ | ^ | ^ |
        # | L | E | ^ | ^ | ^ |
        # | L | S | < | < | < |
        # | L | S | < | < | < |
        # |   |   |   |   |   |
        # |   | L | < | < | < |
        # ---------------------
        self.T1_Label.grid(row=0, column=0, sticky=tk.W); self.T1_Entry.grid (row=0, column=1, sticky=tk.W+tk.W);       
        self.T2_Label.grid(row=1, column=0, sticky=tk.W); self.T2_Entry.grid (row=1, column=1, sticky=tk.W+tk.W); 
        self.PD_Label.grid(row=2, column=0, sticky=tk.W); self.PD_Entry.grid (row=2, column=1, sticky=tk.W+tk.W);     
        self.WM_button.grid (row=0, rowspan=3, column=2, sticky=tk.W);
        self.GM_button.grid (row=0, rowspan=3, column=3, sticky=tk.W);
        self.CSF_button.grid(row=0, rowspan=3, column=4, sticky=tk.W);    
        self.TE_Label.grid(row=3, column=0, sticky=tk.W); self.TE_scale.grid (row=3, column=1, columnspan=4, sticky=tk.W); 
        self.TR_Label.grid(row=4, column=0, sticky=tk.W); self.TR_scale.grid (row=4, column=1, columnspan=4, sticky=tk.W); 
        self.empty = tk.Label(self.master, text=''); self.empty.grid    (row=5, column=0, sticky=tk.W);    
        self.ATT_Label.grid(row=6, column=1, columnspan=4, sticky=tk.W);



    def Update(self, value):
        T1 = float(self.T1_value);
        T2 = float(self.T2_value);
        PD = float(self.PD_value);
        TE = float(self.TE_scale.get());
        TR = float(self.TR_scale.get());
        # just for safety (negative values should never actually occur)
        T1=abs(T1); T2=abs(T2); PD=abs(PD);
        TE=abs(TE); TR=abs(TR);
        if TR<TE: # TR can't be less than TE
            TR, TE = TE, TR
            self.TR_scale.set(TR);
            self.TE_scale.set(TE);
            return;    
        # avoid division by zero
        if T1==0 and T2!=0:
            att = PD * exp(-TE/T2);
        if T1!=0 and T2==0:
            att = PD * (1-exp(-(TR-TE)/T1));
        if T1==0 and T2==0:
            att = PD;
        if T1!=0 and T2!=0: # this is the normal case
             att = PD * exp(-TE/T2) * (1-exp(-(TR-TE)/T1));       
        s = "ATT = %.4f" % att;
        # show result 
        self.ATT.set(s);
        # uncomment line below for debug
        # print "T1=%.0f T2=%.0f PD=%.4f TE=%.0f TR=%.0f ATT=%.4f" % (T1, T2, PD, TE, TR, att);

        
    def validateT1(self, action, index, new_text, prior_text):
        if new_text=='': # the field is being cleared
            self.T1_value = 0;
            self.Update(self); return True;
        try:
            self.T1_value = int(new_text);
        except ValueError:
            return False;
        if self.T1_value<0: return False;
        if self.T1_value<self.T2_value: # in case of T1<T2 modify T2
            self.T2_value = self.T1_value;
            self.T2_text.set(self.T1_value);           
        self.Update(self); return True;
        
      
    def validateT2(self, action, index, new_text, prior_text):
        if new_text=='': # the field is being cleared
            self.T2_value = 0;
            self.Update(self); return True;
        try:
            self.T2_value = int(new_text);
        except ValueError:
            return False;
        if self.T2_value<0: return False;
        if self.T2_value>self.T1_value: # in case of T2>T1 modify T1
            self.T1_value = self.T2_value;
            self.T1_text.set(self.T2_value);           
        self.Update(self); return True;                  
        
    def validatePD(self, action, index, new_text, prior_text):
        if action == "-1": # initial .set command
            self.PD_value = float(new_text);
            self.Update(self); return True;  # return without checks
        if new_text=='': # the field is being cleared
            self.PD_value = 0;      
            self.Update(self); return True;
        try:
            self.PD_value = float(new_text);
            if self.PD_value>1: # upper bound
                self.PD_value = 1;
                # Start update visualization
                # from http://stupidpythonideas.blogspot.com.br/2013/12/tkinter-validation.html
                self.PD_Entry.delete(0, tk.END);
                self.PD_Entry.insert(0,self.PD_value);
                self.after_idle(lambda: self.PD_Entry.config(validate='key'));
                # End update visualization
            if self.PD_value<0: # lower bound
                self.PD_value = 0;
                # Start update visualization
                # from http://stupidpythonideas.blogspot.com.br/2013/12/tkinter-validation.html
                self.PD_Entry.delete(0, tk.END);
                self.PD_Entry.insert(0,self.PD_value);
                self.after_idle(lambda: self.PD_Entry.config(validate='key'));
                # End update visualization        
            self.Update(self); return True;
        except ValueError:
            return False;
            
    def WM_reset(self):
        self.T1_value = T1_WM_def; self.T1_text.set(self.T1_value);
        self.T2_value = T2_WM_def; self.T2_text.set(self.T2_value);
        self.PD_value = PD_WM_def; self.PD_text.set(self.PD_value);
        
    def GM_reset(self):
        self.T1_value = T1_GM_def; self.T1_text.set(self.T1_value);
        self.T2_value = T2_GM_def; self.T2_text.set(self.T2_value);
        self.PD_value = PD_GM_def; self.PD_text.set(self.PD_value);
        
    def CSF_reset(self):
        self.T1_value = T1_CSF_def; self.T1_text.set(self.T1_value);
        self.T2_value = T2_CFS_def; self.T2_text.set(self.T2_value);
        self.PD_value = PD_CSF_def; self.PD_text.set(self.PD_value);

        
CalAMaRes().mainloop();
