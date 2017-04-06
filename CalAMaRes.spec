# -*- mode: python -*-
a = Analysis(['CalAMaRes.pyw'],
             excludes=[ 'win32pdh','win32pipe',
                        'select', 'pydoc', 'pickle', '_hashlib', '_ssl',
                        'setuptools','pyexpat'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
             
def addMCR():
    import os
    import fnmatch
    extraDatas = []
    source='MCRv717'
    for root, dirnames, filenames in os.walk(source):
        for filename in fnmatch.filter(filenames, '*'):    
            extraDatas.append((os.path.join(root, filename), os.path.join(root, filename), 'DATA'))
    return extraDatas             
             
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break             
a.datas = [x for x in a.datas if not ('mpl-data\\fonts' in os.path.dirname(x[1]))]                     
a.datas = [x for x in a.datas if not ('mpl-data\fonts' in os.path.dirname(x[1]))]                     
a.datas = [x for x in a.datas if not ('mpl-data\\sample_data' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('mpl-data\sample_data' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tk8.5\msgs' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tk8.5\images' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tk8.5\demos' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.5\opt0.4' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.5\http1.0' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.5\encoding' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.5\msgs' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.5\tzdata' in os.path.dirname(x[1]))]            
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='CalAMaRes.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False, icon='CalAMaRes.ico')          

