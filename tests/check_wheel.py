"""Verify built wheel resources without fetching/installing dependencies.

Run using the project venv: python tests/check_wheel.py /path/to/built.whl
Imports the extracted wheel ahead of the editable checkout.
"""
import sys
import tempfile
import zipfile
from pathlib import Path

wheel = Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory(prefix='divine-wheel-') as target:
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
        assert 'divine/web/index.html' in names
        assert 'divine/data/catalogue.json' in names
        assert not any(n.startswith(('private/', 'profiles/', '.env')) for n in names)
        archive.extractall(target)
    sys.path.insert(0, target)
    from divine import server, catalogue
    assert str(server.__file__).startswith(target)
    assert Path(server.index().path).is_file()
    assert len(catalogue.catalogue().sources) == 27
    from fastapi.testclient import TestClient
    with TestClient(server.app) as client:
        assert client.get('/').status_code == 200
        assert len(client.get('/api/sources').json()) == 27
    print('Wheel import, packaged UI, catalogue and HTTP resources verified')
