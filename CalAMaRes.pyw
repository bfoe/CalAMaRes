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


def Update():
    T1 = float(T1_value);
    T2 = float(T2_value);
    PD = float(PD_value);
    # alternative code    
    #try:  T1 = float(T1_tkEntry.get());
    #except: T1 = 0 
    #try:  T2 = float(T2_tkEntry.get());
    #except: T2 = 0 
    #try:  PD = float(PD_tkEntry.get());
    #except: PD = 0     
    TE = float(TE_tkScale.get()); #TE = float(PD_tkEntry.get()); 
    TR = float(TR_tkScale.get()); #TR = float(PD_tkEntry.get()); 
    # just for safety (negative values should never actually occur)
    T1=abs(T1); T2=abs(T2); PD=abs(PD);
    TE=abs(TE); TR=abs(TR);
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
    ATT_tkVar.set(s);
    # uncomment line below for debug
    # print "T1=%.0f T2=%.0f PD=%.4f TE=%.0f TR=%.0f ATT=%.4f" % (T1, T2, PD, TE, TR, att);

def validateTE(TE):
    TE = float(TE); #TE = float(TE_tkScale.get());
    TR = float(TR_tkScale.get());
    if TR<TE: # TR can't be less than TE
        TR, TE = TE, TR
        TR_tkScale.set(TR);
        TE_tkScale.set(TE);
    Update();
        
def validateTR(TR):
    TE = float(TE_tkScale.get());
    TR = float(TR); #TR = float(TR_tkScale.get());
    if TR<TE: # TR can't be less than TE
        TR, TE = TE, TR
        TR_tkScale.set(TR);
        TE_tkScale.set(TE);
    Update(); 
    
def validateT1(action, index, new_text, prior_text):
    global T1_value, T2_value
    if new_text=='': # the field is being cleared
        T1_value = 0;
        Update(); return True;
    try:
        T1_value = int(new_text);
    except ValueError:
        return False;
    if T1_value<0: return False;
    if T1_value<T2_value: # in case of T1<T2 modify T2
        T2_value = T1_value;
        T2_tkVar.set(T1_value);           
    Update(); return True;
    
  
def validateT2(action, index, new_text, prior_text):
    global T1_value, T2_value
    if new_text=='': # the field is being cleared
        T2_value = 0;
        Update(); return True;
    try:
        T2_value = int(new_text);
    except ValueError:
        return False;
    if T2_value<0: return False;
    if T2_value>T1_value: # in case of T2>T1 modify T1
        T1_value = T2_value;
        T1_tkVar.set(T2_value);           
    Update(); return True;                  
    
def validatePD(action, index, new_text, prior_text):
    global PD_value
    if action == "-1": # initial .set command
        PD_value = float(new_text);
        Update(); return True;  # return without checks
    if new_text=='': # the field is being cleared
        PD_value = 0;      
        Update(); return True;
    try:
        PD_value = float(new_text);
        if PD_value>1: # upper bound
            PD_value = 1;
            # Start update visualization
            # http://stupidpythonideas.blogspot.com.br/2013/12/tkinter-validation.html
            PD_tkEntry.delete(0, tk.END);
            PD_tkEntry.insert(0,PD_value);
            root.after_idle(lambda: PD_tkEntry.config(validate='key'));
            # End update visualization
        if PD_value<0: # lower bound
            PD_value = 0;
            # Start update visualization
            # http://stupidpythonideas.blogspot.com.br/2013/12/tkinter-validation.html
            PD_tkEntry.delete(0, tk.END);
            PD_tkEntry.insert(0,PD_value);
            root.after_idle(lambda: PD_tkEntry.config(validate='key'));
            # End update visualization        
        Update(); return True;
    except ValueError:
        return False;
        
def WM_reset():
    global T1_value, T2_value, PD_value
    T1_value = T1_WM_def; T1_tkVar.set(T1_value);
    T2_value = T2_WM_def; T2_tkVar.set(T2_value);
    PD_value = PD_WM_def; PD_tkVar.set(PD_value);
    Update();
    
def GM_reset():
    global T1_value, T2_value, PD_value
    T1_value = T1_GM_def; T1_tkVar.set(T1_value);
    T2_value = T2_GM_def; T2_tkVar.set(T2_value);
    PD_value = PD_GM_def; PD_tkVar.set(PD_value);
    Update();
    
def CSF_reset():
    global T1_value, T2_value, PD_value
    T1_value = T1_CSF_def; T1_tkVar.set(T1_value);
    T2_value = T2_CFS_def; T2_tkVar.set(T2_value);
    PD_value = PD_CSF_def; PD_tkVar.set(PD_value);
    Update();

        
root = tk.Tk()
root.title('CalAMarRes');\
# variable Definition & Initialization
T1_value=T1_WM_def; T1_tkVar = tk.IntVar(); T1_tkVar.set(T1_WM_def);
T2_value=T2_WM_def; T2_tkVar = tk.IntVar(); T2_tkVar.set(T2_WM_def); 
PD_value=PD_WM_def; PD_tkVar = tk.IntVar(); PD_tkVar.set(PD_WM_def);
TE_tkVar  = tk.IntVar(); TE_tkVar.set(TE_def);
TR_tkVar  = tk.IntVar(); TR_tkVar.set(TR_def);
ATT_tkVar = tk.IntVar();
# tk.Scale sider for TE 
TE_tkScale = tk.Scale(root, command=validateTE, variable=TE_tkVar, 
    from_=0, to=300, resolution=1, 
    length=500, tickinterval=20, 
    showvalue='yes', orient='horizontal');
TE_tkScale.set(TE_tkVar.get());
TE_tkLabel = tk.Label(root, text='TE ');
# tk.Scale sider for TR
TR_tkScale = tk.Scale(root, command=validateTR, variable=TR_tkVar, 
    from_=0, to=6000, resolution=1, 
    length=500, tickinterval=500, 
    showvalue='yes', orient='horizontal');
TR_tkScale.set(TR_tkVar.get());
TR_tkLabel = tk.Label(root, text='TR ');
# tk.Label Names for Entry
T1_tkLabel = tk.Label(root, text='T1 '); 
T2_tkLabel = tk.Label(root, text='T2 '); 
PD_tkLabel = tk.Label(root, text='PD ');
# tk.Entry for T1, T2, PD
T1_tkEntry = tk.Entry(root, textvariable=T1_tkVar, validate="key", 
    validatecommand=(root.register(validateT1), '%d', '%i', '%P', '%s'));
T2_tkEntry = tk.Entry(root, textvariable=T2_tkVar, validate="key", 
    validatecommand=(root.register(validateT2), '%d', '%i', '%P', '%s'));
PD_tkEntry = tk.Entry(root, textvariable=PD_tkVar, validate="key", 
    validatecommand=(root.register(validatePD), '%d', '%i', '%P', '%s'));
# bind arrow keys on Entry(s)
def FocusT1(event): T1_tkEntry.focus();
def FocusT2(event): T2_tkEntry.focus();
def FocusPD(event): PD_tkEntry.focus();
T1_tkEntry.bind('<Down>', FocusT2);
T2_tkEntry.bind('<Down>', FocusPD);
T2_tkEntry.bind('<Up>',   FocusT1);
PD_tkEntry.bind('<Up>',   FocusT2);
# tk.Button for reset buttons
WM_tkButton  = tk.Button(root, text="WM",  font=('', 26), command=WM_reset);
GM_tkButton  = tk.Button(root, text="GM",  font=('', 26), command=GM_reset);
CSF_tkButton = tk.Button(root, text="CSF", font=('', 26), command=CSF_reset);
# tk.Label to show result
ATT_tkLabel = tk.Label(root, font=('', 26), textvariable=ATT_tkVar);
# Layout
# -------------------------------------------------------------
# | T1_Label | T1_Entry  | WM_Button | GM_Button | CSF_Button |
# | T2_Label | T2_Entry  |    ^      |    ^      |     ^      |
# | PD_Label | PD_Entry  |    ^      |    ^      |     ^      |
# | TE_Label | TE_Scale  |    <      |    <      |     <      |
# | TR_Label | TR_Scale  |    <      |    <      |     <      |
# |  empty   |    <      |    <      |    <      |     <      |
# |          | ATT_Label |    <      |    <      |     <      |
# -------------------------------------------------------------
#
# T1,T2,PD
T1_tkLabel.grid(row=0, column=0, sticky=tk.W);      #T1_Label
T1_tkEntry.grid (row=0, column=1, sticky=tk.W+tk.W);#T2_Entry     
T2_tkLabel.grid(row=1, column=0, sticky=tk.W);      #T2_Label
T2_tkEntry.grid (row=1, column=1, sticky=tk.W+tk.W);#T2_Entry
PD_tkLabel.grid(row=2, column=0, sticky=tk.W);      #PD_Label
PD_tkEntry.grid (row=2, column=1, sticky=tk.W+tk.W);#PD_Entry     
# Reset
WM_tkButton.grid (row=0, rowspan=3, column=2, sticky=tk.W);#WM_Button
GM_tkButton.grid (row=0, rowspan=3, column=3, sticky=tk.W);#GM_Button
CSF_tkButton.grid(row=0, rowspan=3, column=4, sticky=tk.W);#CSF_Button    
# TE, TR
TE_tkLabel.grid(row=3, column=0, sticky=tk.W);               #TE_Label
TE_tkScale.grid (row=3, column=1, columnspan=4, sticky=tk.W);#TE_Entry
TR_tkLabel.grid(row=4, column=0, sticky=tk.W);               #TR_Label 
TR_tkScale.grid (row=4, column=1, columnspan=4, sticky=tk.W);#TR_Entry
# Result
empty = tk.Label(root, text=''); # to create an empty line for spacing
empty.grid    (row=5, column=0, columnspan=5, sticky=tk.W);  #empty  
ATT_tkLabel.grid(row=6, column=1, columnspan=4, sticky=tk.W);#ATT_Label


root.mainloop()