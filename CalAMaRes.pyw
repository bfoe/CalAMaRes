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

import os;
import sys;
from math import exp;
try: import Tkinter as tk;     # Python2
except: 
    try: import tkinter as tk; # Python3
    except: print "Error: tkinter not found"; sys.exit(1)           

# predefined Tissue Parameters 
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2822798/
#
# CSF
T1_CSF_def = 4000; 
T2_CSF_def = 2470; 
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
# should give ATT = 0.6856
#

# predefined initial Sequence parameters
#
TE_def = 30;
TR_def = 2000


def Update (t1, t2, pd, te, tr):
    #print "Input:  t1=%s t2=%s pd=%s te=%s tr=%s" % (t1, t2, pd, te, tr); # debug
    T1 = float_(t1);
    T2 = float_(t2);
    PD = float_(pd);
    TE = float_(te);
    TR = float_(tr);
    # avoid division by zero
    if T1 == 0: T1 = sys.float_info.min;
    if T2 == 0: T2 = sys.float_info.min;
    if pd == '': PD = 1;    
    # just for safety (negative values should never actually occur)
    T1=abs(T1); T2=abs(T2); PD=abs(PD);
    TE=abs(TE); TR=abs(TR);
    # T1/T2 disabled by empty field (not the same as '0')
    if t1 == '' and t2 != '':
        att = PD * exp(-TE/T2);
    if t1 != '' and t2 == '':
        att = PD * (1-exp(-(TR-TE)/T1));
    if t1 == '' and t2 == '':
        att = PD;
    if t1 != '' and t2 != '': # this is the normal case
         att = PD * exp(-TE/T2) * (1-exp(-(TR-TE)/T1));       
    s = "ATT = %.4f" % att;
    # show result 
    ATT_tkVar.set(s);
    #print "Output: T1=%g T2=%g PD=%g TE=%g TR=%g ATT=%g" % (T1, T2, PD, TE, TR, att); # debug

def FocusT1(event): T1_tkEntry.focus(); T1_tkEntry.icursor(110); T1_tkEntry.select_clear()
def FocusT2(event): T2_tkEntry.focus(); T2_tkEntry.icursor(110); T2_tkEntry.select_clear()
def FocusPD(event): PD_tkEntry.focus(); PD_tkEntry.icursor(110); PD_tkEntry.select_clear()
        
def float_(input): # empty string aware float conversion
    if isinstance(input,str):     # is input a string
       if input == '': return 0.; # on empty return 0.
    return float(input);          # else do a normal float conversion
        
def validateTE (TE):
    TE = int(TE);               # convert to int
    TR = int(TR_tkVar.get());   # get TR
    if TR<TE:                   # TR<TE is wrong py MR pysics 
        TR_tkVar.set(TE);       # correct TR in GUI
        TR=TE;                  # correct local TR
    T1 = T1_tkVar.get();        # get T1 needed for update
    T2 = T2_tkVar.get();        # get T2 needed for update
    PD = PD_tkVar.get();        # get PD needed for update
    Update(T1, T2, PD, TE, TR); # update
        
def validateTR (TR):
    TR = int(TR);               # convert to int
    TE = int(TE_tkVar.get());   # get TE
    if TR<TE:                   # TR<TE is wrong py MR pysics
        TE_tkVar.set(TR);       # correct TE in GUI
        TE=TR;                  # correct local TE
    T1 = T1_tkVar.get();        # get T1 needed for update
    T2 = T2_tkVar.get();        # get T2 needed for update
    PD = PD_tkVar.get();        # get PD needed for update
    Update(T1, T2, PD, TE, TR); # update
  
def validateT1 (action, index, t_new, t_prior, t_mod, v_set, v_trig, wID):
    T2 = T2_tkVar.get();                 # get T2 needed for update
    PD = PD_tkVar.get();                 # get PD needed for update
    TE = TE_tkVar.get();                 # get TE needed for update
    TR = TR_tkVar.get();                 # get TR needed for update
    if t_new == '':                      # accept empty tkEntry
        if action != "-1":               # not on initialize (Entry may be not yet defined)
            T1_tkEntry['bg'] = 'yellow'; # set yellow to indicate this condition
    else:
        try: T1 = float(t_new);          # convert to float
        except ValueError: return False; # reject on conversion fail
        if T1 < 0: return False;         # reject <0
        if T1 > 999999: return False;    # reject >999999
        if T1 < float_(T2) and T2 != '': # T1<T2 is wrong by MR physics
            T1 =  '{0:g}'.format(T1)     # convert to string without trailing 0
            T2 = T1                      # correct local T2
            T2_tkVar.set(T1);            # correct T2 in GUI
        if action != "-1":               # not on initialize (Entry may be not yet defined)
            T1_tkEntry['bg'] = 'white';  # reset to white
    Update(t_new, T2, PD, TE, TR);       # update
    return True;                         # OK
    
def validateT2 (action, index, t_new, t_prior, t_mod, v_set, v_trig, wID):
    T1 = T1_tkVar.get();                 # get T1 needed for update
    PD = PD_tkVar.get();                 # get PD needed for update
    TE = TE_tkVar.get();                 # get TE needed for update
    TR = TR_tkVar.get();                 # get TR needed for update
    if t_new == '':                      # accept empty tkEntry
        if action != "-1":               # not on initialize (Entry may be not yet defined)
            T2_tkEntry['bg'] = 'yellow'; # set yellow to indicate this condition
    else:
        try: T2 = float(t_new);          # convert to float
        except ValueError: return False; # reject on conversion fail
        if T2 < 0: return False;         # reject <0
        if T2 > 999999: return False;    # reject >999999
        if T2 > float_(T1) and T1 != '': # T2>T1 is wrong by MR physics
            T2 = '{0:g}'.format(T2)      # convert to string without trailing 0
            T1 = T2                      # correct local T1
            T1_tkVar.set(T2);            # correct T1 in GUI
        if action != "-1":               # not on initialize (Entry may be not yet defined)
            T2_tkEntry['bg'] = 'white';  # reset to white
    Update(T1, t_new, PD, TE, TR);       # update
    return True;                         # OK

def validatePD (action, index, t_new, t_prior, t_mod, v_set, v_trig, wID):
    T1 = T1_tkVar.get();                 # get T1 needed for update
    T2 = T2_tkVar.get();                 # get T2 needed for update
    TE = TE_tkVar.get();                 # get TE needed for update
    TR = TR_tkVar.get();                 # get TR needed for update
    if t_new == '':                      # tkEntry is empty
        if action != "-1":               # not on initialize (Entry may be not yet defined)
            PD_tkEntry['bg'] = 'yellow'; # set yellow to indicate this condition
    else:
        try: PD = float(t_new);          # convert to float
        except ValueError: return False; # reject on conversion fail
        if PD < 0.: return False;        # reject <0.
        if PD > 1.: return False;        # reject >1.
        if action != "-1":               # not on initialize (Entry may be not yet defined)
            PD_tkEntry['bg'] = 'white';  # reset to white
    Update(T1, T2, t_new, TE, TR);       # update
    return True;                         # OK
        
def WM_reset ():
    T1_tkVar.set(T1_WM_def);
    T2_tkVar.set(T2_WM_def);
    PD_tkVar.set(PD_WM_def);
    reset();
    
def GM_reset ():
    T1_tkVar.set(T1_GM_def);
    T2_tkVar.set(T2_GM_def);
    PD_tkVar.set(PD_GM_def);
    reset();
    
def CSF_reset ():
    T1_tkVar.set(T1_CSF_def);
    T2_tkVar.set(T2_CSF_def);
    PD_tkVar.set(PD_CSF_def);
    reset();
    
def reset():    
    FocusT1(0); # default start
    T1_tkEntry['bg'] = 'white';
    T2_tkEntry['bg'] = 'white';
    PD_tkEntry['bg'] = 'white';
    T1_tkEntry.configure(validate='key'); # re-enable after error
    T2_tkEntry.configure(validate='key'); # re-enable after error
    PD_tkEntry.configure(validate='key'); # re-enable after error 


    
# ========================= MAIN PROGRAM STARTS HERE =========================

root = tk.Tk()
root.resizable(width=False, height=False)
Program_name = os.path.basename(sys.argv[0]); 
root.title(Program_name[:Program_name.find('.')]);
# variable Definition & Initialization
T1_tkVar  = tk.StringVar(); T1_tkVar.set(T1_WM_def);
T2_tkVar  = tk.StringVar(); T2_tkVar.set(T2_WM_def); 
PD_tkVar  = tk.StringVar(); PD_tkVar.set(PD_WM_def);
TE_tkVar  = tk.IntVar();    TE_tkVar.set(TE_def);
TR_tkVar  = tk.IntVar();    TR_tkVar.set(TR_def);
ATT_tkVar = tk.IntVar();
# tk.Scale sider for TE 
TE_tkScale = tk.Scale(root, command=validateTE, variable=TE_tkVar, 
    from_=0, to=300, resolution=1, 
    length=500, tickinterval=20, 
    showvalue='yes', orient='horizontal');
TE_tkLabel = tk.Label(root, text='TE ');
# tk.Scale sider for TR
TR_tkScale = tk.Scale(root, command=validateTR, variable=TR_tkVar, 
    from_=0, to=6000, resolution=1, 
    length=500, tickinterval=500, 
    showvalue='yes', orient='horizontal');
TR_tkLabel = tk.Label(root, text='TR ');
# tk.Label Names for Entry
T1_tkLabel = tk.Label(root, text='T1 '); 
T2_tkLabel = tk.Label(root, text='T2 '); 
PD_tkLabel = tk.Label(root, text='PD ');
# tk.Entry for T1, T2, PD
# validation parameters
#   %d = Type of action (1=insert, 0=delete, -1 for others)
#   %i = index of char string to be inserted/deleted, or -1
#   %P = value of the entry if the edit is allowed
#   %s = value of entry prior to editing
#   %S = the text string being inserted or deleted, if any
#   %v = the type of validation that is currently set
#   %V = the type of validation that triggered the callback
#       (key, focusin, focusout, forced)
#   %W = the tk name of the widget
#        find with nametowidget(W)
vcmd=(root.register(validateT1), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
T1_tkEntry = tk.Entry(root, textvariable=T1_tkVar, validate="key", validatecommand=vcmd);
vcmd=(root.register(validateT2), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
T2_tkEntry = tk.Entry(root, textvariable=T2_tkVar, validate="key", validatecommand=vcmd);
vcmd=(root.register(validatePD), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
PD_tkEntry = tk.Entry(root, textvariable=PD_tkVar, validate="key", validatecommand=vcmd);
# bind arrow keys on Entry(s)
T1_tkEntry.bind('<Down>', FocusT2);
T2_tkEntry.bind('<Down>', FocusPD);
T2_tkEntry.bind('<Up>',   FocusT1);
PD_tkEntry.bind('<Up>',   FocusT2);
FocusT1(0) # default start
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
TE_tkScale.grid (row=3, column=1, columnspan=4, sticky=tk.W);#TE_Scale
TR_tkLabel.grid(row=4, column=0, sticky=tk.W);               #TR_Label 
TR_tkScale.grid (row=4, column=1, columnspan=4, sticky=tk.W);#TR_Scale
# Result
empty = tk.Label(root, text=''); # to create an empty line for spacing
empty.grid    (row=5, column=0, columnspan=5, sticky=tk.W);  #empty  
ATT_tkLabel.grid(row=6, column=1, columnspan=4, sticky=tk.W);#ATT_Label


root.mainloop()