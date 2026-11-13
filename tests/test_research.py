import json
from pathlib import Path
from xml.etree import ElementTree as ET
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from divine import catalogue, psalter, language, manuscripts, diagrams, astro, agents
from divine.server import app


def test_catalogue_schema_and_conservative_evidence():
    cat = catalogue.catalogue()
    assert len(cat.sources) == 27
    assert json.loads(Path('divine/data/catalogue.schema.json').read_text()) == catalogue.schema()
    assert all(s.rights.text.startswith('UNKNOWN') and s.accessed is None for s in cat.sources)
    assert catalogue.search_sources('3188')[0]['id'] == 'sloane-3188'
    assert catalogue.search_sources('3189')[0]['evidence'] == 'HYPOTHESIS'
    assert catalogue.search_sources(evidence='UNKNOWN')
    assert catalogue.search_sources('not-a-source') == []
    assert catalogue.search_sources(medium='manuscript', date='1583')


def test_catalogue_rejects_duplicates_and_unsafe_urls():
    cat = catalogue.catalogue().model_dump()
    cat['sources'].append(cat['sources'][0])
    with pytest.raises(ValidationError, match='Duplicate'):
        catalogue.Catalogue.model_validate(cat)
    for url in ('javascript:alert(1)', 'http://example.org', 'https://u:p@example.org'):
        source = catalogue.catalogue().sources[0].model_dump()
        source['source_url'] = url
        with pytest.raises(ValidationError):
            catalogue.Source.model_validate(source)


@pytest.mark.parametrize('mt,lxx', [(1,[1]),(8,[8]),(9,[9]),(10,[9]),(11,[10]),
    (113,[112]),(114,[113]),(115,[113]),(116,[114,115]),(117,[116]),
    (146,[145]),(147,[146,147]),(148,[148]),(150,[150])])
def test_psalm_reference_vectors(mt,lxx):
    assert psalter.mt_to_lxx(mt) == lxx


def test_all_150_works_and_inverse_coordinates():
    data = psalter.index()
    assert len(data['psalms']) == 150
    assert [sum(a <= n <= b for n in range(1,151)) for a,b in psalter.BOOKS] == [41,31,17,17,44]
    assert len({p['works'][0]['id'] for p in data['psalms']}) == 150
    for n in range(1,151):
        for lxx in psalter.mt_to_lxx(n):
            assert n in [w['mt_chapter'] for w in psalter.psalm(lxx,'lxx-index')['works']]
        assert psalter.psalm(n)['text'] is None
    assert len(psalter.psalm(9,'lxx-index')['works']) == 2
    assert len(psalter.psalm(113,'lxx-index')['works']) == 2
    for n in (0,151,-1):
        with pytest.raises(ValueError): psalter.psalm(n)
    with pytest.raises(ValueError): psalter.psalm(1,'fake')


def test_hebrew_named_scheme_vectors_and_preserved_marks():
    assert language.calculate('שלום','hebrew-standard-v1')['total'] == 376
    assert language.calculate('שלום','hebrew-ordinal-v1')['total'] == 52
    text = 'שָׁלוֹם ךםןףץ'
    result = language.calculate(text,'hebrew-standard-v1')
    assert result['input'] == text
    assert ''.join(t['character'] for t in result['trace']) == text
    assert result['total'] == 376 + 20+40+50+80+90
    assert result['authority'] == 'NONE'


@pytest.mark.parametrize('text,scheme', [('abc','hebrew-standard-v1'),('א\u202e','hebrew-standard-v1'),
    ('123','hebrew-standard-v1'),('א'*2001,'hebrew-standard-v1'),('','hebrew-standard-v1'),
    ('א','unknown'),('ָ','hebrew-standard-v1')])
def test_language_abuse(text,scheme):
    with pytest.raises(ValueError): language.calculate(text,scheme)


def fixture_manifest():
    return json.loads(Path('tests/fixtures/iiif-synthetic.json').read_text())


def test_iiif_subset_and_no_network(monkeypatch):
    import urllib.request
    monkeypatch.setattr(urllib.request,'urlopen',lambda *a,**kw: pytest.fail('No import fetches allowed'))
    result = manuscripts.parse_manifest(fixture_manifest())
    assert len(result['pages']) == 2
    assert result['pages'][1]['label'] == 'Synthetic page 2'
    assert result['rights'] == 'https://creativecommons.org/publicdomain/zero/1.0/'


@pytest.mark.parametrize('url',['file:///etc/passwd','http://127.0.0.1/x','https://evil.example/image.png',
    'https://tile.loc.gov.evil.example/x','https://u:p@tile.loc.gov/x','https://tile.loc.gov:444/x'])
def test_manifest_rejects_untrusted_images(url):
    raw = fixture_manifest()
    raw['items'][0]['items'][0]['items'][0]['body']['id'] = url
    with pytest.raises(ValueError): manuscripts.parse_manifest(raw)


def test_manifest_rejects_duplicate_pages_bad_targets_dimensions():
    for transform in [lambda r:r['items'].append(r['items'][0]),
        lambda r:r['items'][0].update(width=0),
        lambda r:r['items'][0]['items'][0]['items'][0].update(target='https://example.org/wrong')]:
        raw = fixture_manifest(); transform(raw)
        with pytest.raises(ValueError): manuscripts.parse_manifest(raw)


@pytest.mark.parametrize('planet,n,total',[('Saturn',3,15),('Sun',6,111),('Moon',9,369)])
def test_svg_geometry_and_provenance(planet,n,total):
    svg = diagrams.square_svg(planet)
    assert svg == diagrams.square_svg(planet)
    root = ET.fromstring(svg); ns={'s':'http://www.w3.org/2000/svg'}
    assert 'RECONSTRUCTION' in root.find('s:title',ns).text
    meta = json.loads(root.find('s:metadata',ns).text)
    assert meta['constant'] == total and meta['historical_source'] is None
    assert len(root.findall('.//s:line',ns)) == 2*(n+1)
    assert len(root.findall(".//s:g[@id='numbers']/s:text",ns)) == n*n
    assert not ET.fromstring(diagrams.square_svg(planet,False)).findall(".//s:g[@id='numbers']/s:text",ns)
    assert '<script' not in svg and 'href=' not in svg


def test_api_research_end_to_end(tmp_path,monkeypatch):
    monkeypatch.setenv('DIVINE_DATA_DIR',str(tmp_path/'private'))
    with TestClient(app) as c:
        rows = c.get('/api/sources').json()
        assert len(rows) == 27
        assert c.get('/api/sources/schema').json()['title'] == 'Catalogue'
        for row in rows:
            assert c.get('/api/sources/'+row['id']).json() == row
        assert c.get('/api/sources/missing').status_code == 404
        assert c.post('/api/sources/validate',json=catalogue.catalogue().model_dump()).json()['persisted'] is False
        assert c.get('/api/psalter').status_code == 200
        for n in range(1,151):
            r=c.get('/api/psalter/'+str(n)); assert r.status_code==200
            assert r.json()['coordinate']['chapter']==n
        assert c.get('/api/psalter/151').status_code == 422
        assert c.get('/api/psalter/1?edition=forged').status_code == 422
        assert c.post('/api/language/calculate',json={'text':'שלום','scheme':'hebrew-standard-v1'}).json()['total']==376
        assert c.post('/api/manuscripts/validate',json=fixture_manifest()).status_code==200
        assert c.post('/api/manuscripts/validate',json={'type':'Manifest'}).status_code==422
        assert c.get('/api/diagrams/Saturn.svg').headers['content-type'].startswith('image/svg+xml')
        assert c.get('/api/diagrams/invalid.svg').status_code==404


def test_local_api_threat_boundaries():
    with TestClient(app) as c:
        assert c.get('/api/sources',headers={'Host':'evil.example'}).status_code==400
        assert c.get('/api/sources',headers={'Origin':'https://evil.example'}).status_code==403
        assert c.get('/api/sources',headers={'Sec-Fetch-Site':'cross-site'}).status_code==403
        assert c.post('/api/manuscripts/validate',content='{}').status_code==415
        assert c.post('/api/manuscripts/validate',content='x'*1_048_577,headers={'Content-Type':'application/json'}).status_code==413
        assert c.get('/').headers['x-content-type-options']=='nosniff'
        assert c.get('/api/sources').headers['cache-control']=='no-store'
    with TestClient(app,client=('192.0.2.1',123)) as c:
        assert c.get('/api/sources').status_code==403


def test_birth_offset_and_bad_fold_rejected():
    for value,fold in [('12:00+10:00',None),('12:00',2)]:
        with pytest.raises(ValueError): astro.parse_local_birth('2000-01-01',value,'UTC',fold)


def test_workspace_rejects_traversal_and_symlink(tmp_path,monkeypatch):
    monkeypatch.setenv('DIVINE_DATA_DIR',str(tmp_path/'private'))
    with pytest.raises(ValueError): agents.compile_workspace({'id':'../../escape','goals':''})
    workspace=tmp_path/'private'/'workspaces'; workspace.mkdir(parents=True)
    outside=tmp_path/'outside'; outside.mkdir()
    workspace.joinpath('00000000-0000-0000-0000-000000000000').symlink_to(outside,target_is_directory=True)
    with pytest.raises(ValueError): agents.compile_workspace({'id':'00000000-0000-0000-0000-000000000000','goals':''})
    assert not list(outside.iterdir())


def test_original_tei_provenance_chain():
    ns={'t':'http://www.tei-c.org/ns/1.0'}
    tree=ET.parse('tests/fixtures/original-transcription.tei.xml')
    phrase=tree.find('.//t:seg',ns).text
    assert phrase=='Source before symbol.' and len(phrase.split())==3
    chain=json.loads(Path('divine/data/provenance-example.json').read_text())
    ids={e['id'] for e in chain['entities']}
    assert all(e.get('derived_from') in ids for e in chain['entities'][1:])
    assert chain['entities'][2]['text']==phrase
    assert tree.find('.//t:pb',ns).attrib['facs']=='#synthetic-page'
    assert tree.find('.//t:availability',ns) is not None


def test_nested_workspace_symlink_never_creates_external_dirs(tmp_path,monkeypatch):
    monkeypatch.setenv('DIVINE_DATA_DIR',str(tmp_path/'private'))
    root=tmp_path/'private';root.mkdir()
    outside=tmp_path/'outside';outside.mkdir()
    (root/'.agents').symlink_to(outside,target_is_directory=True)
    with pytest.raises(ValueError): agents._write(root/'.agents'/'skills'/'test.txt','not written')
    assert not list(outside.iterdir())


def test_invalid_square_and_calculation_metadata():
    from divine.traditions import verify_magic
    assert not verify_magic([])
    assert not verify_magic([[1]])
    result=astro.natal_chart('2000-01-01',None,'UTC')
    assert result['label']=='CALCULATION'
    assert result['engine']['version']


def test_api_docs_are_offline_and_provenance_resolves():
    with TestClient(app) as c:
        result=c.get('/api/docs')
        assert result.status_code==200
        assert '<script' not in result.text and 'cdn.' not in result.text
        assert '/openapi.json' in result.text
        assert '/api/psalter/{number}' in c.get('/openapi.json').json()['paths']
        assert c.get('/api/provenance/example').json()['evidence']=='RECONSTRUCTION'
        assert c.delete('/api/profiles/not-a-uuid').status_code==404


def test_iiif_context_multilingual_services_and_region_requests():
    raw=fixture_manifest()
    raw['@context']=['https://example.org/extra','http://iiif.io/api/presentation/3/context.json']
    raw['label']={'he':['כתב יד'],'fr':['Exercice']}
    body=raw['items'][0]['items'][0]['items'][0]['body']
    body['service']=[{'id':'https://iiif.io/synthetic/service','type':'ImageService3','profile':'level1'}]
    parsed=manuscripts.parse_manifest(raw)
    assert parsed['label']=='כתב יד'
    assert parsed['pages'][0]['image_service']=='https://iiif.io/synthetic/service'
    assert manuscripts.region_request(raw,0,(0,0,100,100),100)=='https://iiif.io/synthetic/service/0,0,100,100/100,/0/default.jpg'
    for page,region,width in [(2,(0,0,1,1),1),(0,(-1,0,10,10),1),(0,(0,0,0,1),1),
                              (0,(0,0,99999,99999),1),(0,(0,0,10,10),11)]:
        with pytest.raises(ValueError): manuscripts.region_request(raw,page,region,width)
    body['service'][0]['id']='https://iiif.io/../escape'
    with pytest.raises(ValueError): manuscripts.parse_manifest(raw)


@pytest.mark.parametrize('change',[
    lambda r:r.update(label={'en':['x'],'he':[42]}),
    lambda r:r['items'][0].update(items=None),
    lambda r:r['items'][0]['items'][0].update(items=[None]),
    lambda r:r['items'][0]['items'][0]['items'][0]['body'].update(service=[None]),
])
def test_iiif_malformed_structure_api_returns_422(change):
    raw=fixture_manifest();change(raw)
    with TestClient(app) as c:
        assert c.post('/api/manuscripts/validate',json=raw).status_code==422


def test_image_region_uses_image_pixels_not_canvas_units():
    raw=fixture_manifest()
    assert raw['items'][0]['width']==600
    assert manuscripts.region_request(raw,0,(600,800,600,800),600).endswith('/600,800,600,800/600,/0/default.jpg')
    del raw['items'][0]['items'][0]['items'][0]['body']['width']
    with pytest.raises(ValueError,match='pixel dimensions'): manuscripts.parse_manifest(raw)


def test_image_request_api_local_only_no_fetch(monkeypatch):
    import urllib.request
    monkeypatch.setattr(urllib.request,'urlopen',lambda *a,**kw: pytest.fail('No network allowed'))
    monkeypatch.delenv('DIVINE_ALLOW_NETWORK',raising=False)
    with TestClient(app) as c:
        payload={'manifest':fixture_manifest(),'page':0,'region':[600,800,100,100],'width':100}
        result=c.post('/api/manuscripts/image-request',json=payload)
        assert result.status_code==200 and result.json()['retrieved'] is False
        payload['page']=1
        assert c.post('/api/manuscripts/image-request',json=payload).status_code==422
        assert "img-src 'self' blob:;" in c.get('/').headers['content-security-policy']
