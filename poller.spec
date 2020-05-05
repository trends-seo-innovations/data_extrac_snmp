
# -*- mode: python -*-
 
hiddenimports = ['pysnmp.smi.exval','pysnmp.cache']
a = Analysis(['poller.py'],
             pathex=['D://SEO Projects//see_backend//dist//poller'],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None,
)
x = Tree('C:/Users/jlalmenanza/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/pysnmp/smi/mibs',prefix='pysnmp/smi/mibs',excludes='.py')
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          x,
          name='poller',
          debug=False,
          strip=None,
          upx=True,
          console=True )