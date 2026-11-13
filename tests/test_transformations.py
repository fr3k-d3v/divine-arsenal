import pytest
from fastapi.testclient import TestClient
from divine import language
from divine.server import app


def test_extraction_preserves_combining_clusters_and_original_spans():
    text='שָׁלוֹם עולם'
    expected={'first-letter-v1':'שָׁע','last-letter-v1':'םם','middle-left-v1':'לו'}
    for algorithm,result in expected.items():
        data=language.transform(text,algorithm)
        assert data['output']==result and data['authority']=='NONE'
        assert data['input']==text
        for item in data['trace']:
            assert text[item['input_start']:item['input_end_exclusive']]==item['text']
    assert language.transform('אב גד','middle-left-v1')['output']=='אג'
    assert language.transform('אב־גד','last-letter-v1')['output']=='בד'


def test_permutations_explicit_logical_order_and_rotation():
    assert language.transform('שָׁלוֹם','reverse-letters-v1')['output']=='םוֹלשָׁ'
    assert language.transform('אב גד','rotate-letters-v1',1)['output']=='בגדא'
    assert language.transform('אב גד','rotate-letters-v1',-1)['output']=='דאבג'
    assert language.transform('א','rotate-letters-v1',2000)['output']=='א'


@pytest.mark.parametrize('text,algorithm,offset',[('ָא','first-letter-v1',0),('אב ָג','last-letter-v1',0),
    ('a','first-letter-v1',0),('א\u202e','first-letter-v1',0),('א','unknown',0),
    ('א','first-letter-v1',1),('א','rotate-letters-v1',2001),('א','rotate-letters-v1',True),
    ('','first-letter-v1',0)])
def test_invalid_transformations(text,algorithm,offset):
    with pytest.raises(ValueError): language.transform(text,algorithm,offset)


def test_rectangular_grid_trace_and_rotation_identity():
    original=[['א','ב','ג'],['ד','ה','ו']]
    assert language.transform_grid(original,'transpose-v1')['cells']==[['א','ד'],['ב','ה'],['ג','ו']]
    assert language.transform_grid(original,'reverse-columns-v1')['cells']==[['ג','ב','א'],['ו','ה','ד']]
    assert language.transform_grid(original,'reverse-rows-v1')['cells']==list(reversed(original))
    current=original
    for i in range(4):
        data=language.transform_grid(current,'rotate-clockwise-v1')
        for row,trace in zip(data['cells'],data['input_coordinates']):
            assert row==[current[r][c] for r,c in trace]
        current=data['cells']
    assert current==original
    assert len(language.transform_grid([['x']*49 for _ in range(49)],'transpose-v1')['cells'])==49


@pytest.mark.parametrize('cells,operation', [([], 'transpose-v1'),([['a'],['b','c']], 'transpose-v1'),
    ([['a']]*50,'transpose-v1'),([['\u202e']],'transpose-v1'),([['']], 'transpose-v1'),
    ([['a'*17]],'transpose-v1'),([['a']],'unknown'),([[None]],'transpose-v1')])
def test_invalid_grids(cells,operation):
    with pytest.raises(ValueError): language.transform_grid(cells,operation)


def test_transform_api_trace_and_untrusted_input():
    with TestClient(app) as c:
        result=c.post('/api/language/transform',json={'text':'אב גד','algorithm':'first-letter-v1'})
        assert result.json()['output']=='אג'
        assert c.post('/api/language/transform',json={'text':'a','algorithm':'first-letter-v1'}).status_code==422
        assert c.post('/api/language/grid',json={'cells':[['x','y']],'operation':'transpose-v1'}).json()['cells']==[['x'],['y']]
        assert c.post('/api/language/grid',json={'cells':[[]],'operation':'transpose-v1'}).status_code==422


def test_edition_specific_verse_coordinate_structure_not_equivalence():
    from divine import psalter
    result=psalter.verse_reference(113,'lxx-index','Synthetic example edition',0,3)
    assert result['work_candidates']==['psalm-114','psalm-115']
    assert result['coordinate']=={'chapter':113,'system':'LXX','verse_start':0,'verse_end':3}
    assert result['text'] is None and result['evidence']=='UNKNOWN'
    for number,edition,text,start,end in [(151,'mt-index','x',1,1),(1,'fake','x',1,1),
        (1,'mt-index','',1,1),(1,'mt-index','x',-1,1),(1,'mt-index','x',2,1),
        (1,'mt-index','x',True,2),(1,'mt-index','a\n',1,1)]:
        with pytest.raises(ValueError): psalter.verse_reference(number,edition,text,start,end)
    with TestClient(app) as c:
        data=c.get('/api/psalter/113/reference',params={'index_edition':'lxx-index','text_edition':'Synthetic edition','verse_start':1})
        assert data.status_code==200 and data.json()['coordinate']['verse_end']==1
        assert c.get('/api/psalter/1/reference?verse_start=1').status_code==422
