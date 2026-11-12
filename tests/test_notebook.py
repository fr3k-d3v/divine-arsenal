"""Synthetic-only notebook lifecycle, migrations, import and authority boundaries."""
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from divine import notebook, store
from divine.server import app


@pytest.fixture(autouse=True)
def private(tmp_path, monkeypatch):
    monkeypatch.setenv('DIVINE_DATA_DIR', str(tmp_path/'private'))


def transcription(**changes):
    return {'kind':'transcription','title':'Original synthetic exercise','text':'שלום\n[unclear]',
            'coordinates': {'source_id':'sloane-3188','edition':'Synthetic exercise, not manuscript text',
                            'page':'Synthetic page','line':'1–2','region':[0,0,10,20]},
            'attribution':'Test author','rights':'Project-original synthetic input',**changes}


def save(document, revision=0):
    return notebook.Save(expected_revision=revision, document=document)


def test_revision_history_unicode_conflicts_and_deletion():
    item=notebook.save(save(transcription()))
    new=notebook.save(save(transcription(text='Revised original'),1),item['id'])
    assert new['revision']==2 and new['history'][0]['document']['text']=='שלום\n[unclear]'
    with pytest.raises(notebook.Conflict): notebook.save(save(transcription(text='Lost edit'),1),item['id'])
    with pytest.raises(notebook.Conflict): notebook.delete(item['id'],1)
    with pytest.raises(notebook.Conflict): notebook.save(save({'kind':'journal','title':'x','text':'x'},2),item['id'])
    assert notebook.get(item['id'])['revision']==2
    assert notebook.delete(item['id'],2)
    assert notebook.get(item['id']) is None and notebook.listing()==[]


def test_migration_preserves_profiles_and_is_idempotent():
    profile=store.create_profile({'alias':'synthetic'})
    assert notebook.listing()==notebook.listing()==[]
    assert store.get_profile(profile['id'])==profile
    with store._connect() as db:
        assert db.execute('SELECT version FROM notebook_migrations').fetchall()[0][0]==1
    assert (store.private_root()/'profiles.sqlite3').stat().st_mode & 0o777 == 0o600


def test_concurrent_edits_only_one_wins():
    item=notebook.save(save(transcription()))
    def edit(n):
        try:
            notebook.save(save(transcription(text=str(n)),1),item['id']); return 'saved'
        except notebook.Conflict: return 'conflict'
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(edit,[1,2]))==['conflict','saved']


def test_export_import_revisions_are_private_new_ids_and_no_profiles():
    store.create_profile({'alias':'PRIVATE PROFILE NEVER EXPORTED'})
    item=notebook.save(save(transcription()))
    notebook.save(save(transcription(text='second'),1),item['id'])
    bundle=notebook.export_bundle()
    assert 'PRIVATE PROFILE' not in bundle.model_dump_json()
    imported=notebook.import_bundle(bundle)
    assert imported != [item['id']]
    restored=notebook.get(imported[0])
    assert restored['revision']==2 and restored['history'][0]['document']['text']=='שלום\n[unclear]'
    assert notebook.listing('journal')==[]
    assert len(notebook.listing('transcription'))==2


@pytest.mark.parametrize('changes',[
    {'coordinates':{'source_id':'fake','edition':'x','page':'x'}},
    {'coordinates':{'source_id':'sloane-3188','edition':'x','page':'x','region':[-1,0,2,3]}},
    {'coordinates':{'source_id':'sloane-3188','edition':'x','page':'x','canvas':'file:///etc/passwd'}},
    {'state':'published'}, {'state':'machine draft'}, {'confidence':float('nan')},
    {'authority':'AUTO'}, {'text':'x'*100001}, {'rights':''}])
def test_invalid_documents_fail_closed(changes):
    with pytest.raises(ValidationError): save(transcription(**changes))


def test_import_validation_and_no_partial_write():
    valid={'format':'divine-private-notebook','version':1,'items':[{'revisions':[transcription()]}]}
    for key,value in [('version',2),('path','../../global'),('profiles',[])]:
        bad={**valid,key:value}
        with pytest.raises(ValidationError): notebook.Bundle.model_validate(bad)
    bad=json.loads(json.dumps(valid)); bad['items'].append({'revisions':[{'kind':'journal','title':'x','text':'x','execute':'evil'}]})
    with pytest.raises(ValidationError): notebook.Bundle.model_validate(bad)
    assert notebook.listing()==[]
    mixed={'revisions':[transcription(),{'kind':'journal','title':'x','text':'x'}]}
    with pytest.raises(ValidationError): notebook.ImportItem.model_validate(mixed)


def relationship(**changes):
    return {'kind':'relationship','title':'Synthetic comparison, no historical assertion',
            'subject':'sloane-3188','object':'sloane-3189','predicate':'resembles','evidence':'HYPOTHESIS',
            'citation':transcription()['coordinates'],'attribution':'Synthetic test',
            'date_range':'UNKNOWN','note':'Fixture only',**changes}


def test_graph_inspectable_citation_filters_and_no_invented_edges():
    assert notebook.graph()['edges']==[]
    item=notebook.save(save(relationship()))
    graph=notebook.graph('synthetic','HYPOTHESIS')
    assert len(graph['nodes'])==27
    assert graph['edges'][0]['citation']['source_id']=='sloane-3188'
    assert graph['edges'][0]['id']==item['id']
    assert notebook.graph(evidence='VERIFIED FACT')['edges']==[]
    for changes in [{'object':'fake'},{'object':'sloane-3188'},{'evidence':'VERIFIED FACT'}]:
        with pytest.raises(ValidationError): save(relationship(**changes))


def test_api_private_lifecycle_and_security():
    with TestClient(app) as c:
        r=c.post('/api/notebook',json={'expected_revision':0,'document':transcription()})
        assert r.status_code==201
        item=r.json(); path='/api/notebook/'+item['id']
        assert c.get(path).json()['revision']==1
        assert c.put(path,json={'expected_revision':0,'document':transcription()}).status_code==409
        assert c.get('/api/notebook/export').headers['cache-control']=='no-store'
        assert c.post('/api/notebook/import',json=c.get('/api/notebook/export').json()).status_code==200
        assert c.delete(path+'?expected_revision=1').json()['deleted']
        assert c.get(path).status_code==404
        assert c.get('/api/notebook/invalid').status_code==422
        assert c.get('/api/notebook',headers={'Origin':'https://evil.example'}).status_code==403
        assert c.get('/api/geo/search?q=Brisbane').status_code==403
        assert c.get('/api/health').json()['local_only'] is True
        assert c.get('/api/notebook/graph').status_code==200


def test_manifest_archive_roundtrip_and_invalid_import():
    from pathlib import Path
    raw=json.loads(Path('tests/fixtures/iiif-synthetic.json').read_text())
    item=notebook.save(save({'kind':'manifest','title':'Synthetic manifest','manifest':raw}))
    assert notebook.get(item['id'])['document']['manifest']==raw
    raw['items'][0]['width']=0
    with pytest.raises(ValidationError): save({'kind':'manifest','title':'Invalid','manifest':raw})


def test_tei_profile_lossless_roundtrip_and_rejects_active_or_inconsistent_xml():
    from divine import tei
    document=notebook.Transcription.model_validate(transcription(text='שלום <unclear> & original\nnext line'))
    xml=tei.encode(document)
    assert tei.decode(xml)==document
    for bad in ['<!DOCTYPE x [<!ENTITY a SYSTEM "file:///etc/passwd">]>'+xml,
                xml.replace('<body>', '<body onclick="bad">'),
                xml.replace('<ab>', '<ab>tampered'), '<TEI/>', '<?xml-stylesheet href="https://evil.example"?>'+xml]:
        with pytest.raises(ValueError): tei.decode(bad)
    with TestClient(app) as c:
        item=c.post('/api/notebook',json={'expected_revision':0,'document':document.model_dump()}).json()
        exported=c.get('/api/notebook/'+item['id']+'/tei')
        assert exported.status_code==200 and 'sandbox' in exported.headers['content-security-policy']
        result=c.post('/api/transcriptions/tei/validate',json={'xml':exported.text})
        assert result.json()['document']==document.model_dump(mode='json')
        assert result.json()['persisted'] is False
        assert c.post('/api/transcriptions/tei/validate',json={'xml':'<!DOCTYPE evil><TEI/>'}).status_code==422


def test_size_limit_rolls_back_and_backups_stay_importable():
    document={'kind':'journal','title':'Synthetic capacity test','text':'א'*100000}
    item=notebook.save(save(document))
    for rev in range(1,4): notebook.save(save(document,rev),item['id'])
    with pytest.raises(ValueError,match='backup limit'): notebook.save(save(document,4),item['id'])
    assert notebook.get(item['id'])['revision']==4
    bundle=notebook.export_bundle()
    assert len(bundle.model_dump_json().encode('utf-8'))<1048576
    with pytest.raises(ValueError,match='backup limit'): notebook.import_bundle(bundle)
    assert len(notebook.listing())==1


@pytest.mark.parametrize('bad',['\ud800','\x00','\x01','\ufffe','\uffff'])
def test_invalid_unicode_scalars_and_xml_controls_rejected(bad):
    with pytest.raises(ValidationError): save(transcription(text=bad))


def test_all_or_nothing_import_document_count_cap():
    item=notebook.ImportItem(revisions=[notebook.Journal(kind='journal',title='Synthetic',text='x')])
    notebook.import_bundle(notebook.Bundle(format='divine-private-notebook',version=1,items=[item]*100))
    with pytest.raises(ValueError,match='100-document'): notebook.import_bundle(notebook.Bundle(format='divine-private-notebook',version=1,items=[item]))
    assert len(notebook.listing())==100
