"""Install a built wheel into an isolated /tmp venv using existing dependencies.

No downloads, profile data, providers or global installs. Run via project Python.
"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

wheel = Path(sys.argv[1]).resolve()
site = next(p for p in sys.path if p.endswith('site-packages'))
with tempfile.TemporaryDirectory(prefix='divine-installed-') as temporary:
    root = Path(temporary)
    subprocess.run(['uv', 'venv', '--offline', '--python', sys.executable, str(root/'venv')], check=True)
    python = str(root/'venv/bin/python')
    subprocess.run(['uv', 'pip', 'install', '--offline', '--no-deps', '--python', python, str(wheel)], check=True)
    script = '''
import json,sys
from pathlib import Path
sys.path.append(sys.argv[1])
from divine import server,notebook
assert '/divine-installed-' in server.__file__,server.__file__
from fastapi.testclient import TestClient
with TestClient(server.app) as client:
    assert client.get('/api/health').status_code==200
    assert client.get('/api/health').json()['local_only']
    assert len(client.get('/api/sources').json())==27
    assert len(client.get('/api/psalter').json()['psalms'])==150
    assert client.get('/api/notebook').json()==[]
    result=client.post('/api/notebook',json={'expected_revision':0,'document':{'kind':'journal','title':'Synthetic installed-wheel check','text':'Original test'}})
    assert result.status_code==201,result.text
    assert client.delete('/api/notebook/'+result.json()['id']+'?expected_revision=1').json()['deleted']
    assert 'Private research notebook' in client.get('/').text
print('Installed wheel: imports, packaged UI/data, health, notebook lifecycle verified')
'''
    env = {**os.environ, 'DIVINE_DATA_DIR': str(root/'private')}
    subprocess.run([python, '-I', '-c', script, site], cwd=root, env=env, check=True)
