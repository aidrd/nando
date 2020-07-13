"""
jsonファイルをttlファイル
"""
import json


def json_to_ttl(json_list):
    prefixes = '''@prefix : <http://nanbyodata.jp/ontology/nanbyo#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix mondo: <http://purl.obolibrary.org/obo/> .
@prefix oboinowl: <http://www.geneontology.org/formats/oboInOwl#> .
@prefix terms: <http://purl.org/dc/terms/> .
@prefix efo: <http://www.ebi.ac.uk/efo/> .
# @base <http://nanbyodata.jp/ontology/nanbyo.owl> .
'''
    
    ontology_property = '''
#################################################################
#    Ontology Property
#################################################################
<http://nanbyodata.jp/ontology/nanbyo.owl#>
    rdf:type owl:Ontology ;
    owl:versionIRI <http://nanbyodata.jp/version0.1> ;
    owl:versionInfo "0.1"^^xsd:string ;
    <http://purl.org/dc/elements/1.1/creator> "Kota Ninomiya"^^xsd:string ,
                                              "Ryota Yamada"^^xsd:string ,
                                              "Orion Buske"^^xsd:string ,
                                              "Toshiaki Katayama"^^xsd:string ,
                                              "Shuichi Kawashima"^^xsd:string ,
                                              "Yasunori Yamamoto"^^xsd:string ,
                                              "Hiroshi Masuya"^^xsd:string ,
                                              "Soichi Ogishima"^^xsd:string ,
                                              "Toyofumi Fujiwara"^^xsd:string ;
    <http://purl.org/dc/terms/license> <https://creativecommons.org/licenses/by/4.0/> ;
    <http://purl.org/dc/terms/created> "2019-10-29T16:00:00"^^xsd:dateTime ;
    <http://purl.org/dc/terms/modified> "2019-10-29T16:00:00"^^xsd:dateTime .
'''
    
    annotation_properties = '''
#################################################################
#    Annotation Properties
#################################################################
:classifiedWith
    rdf:type owl:ObjectProperty ;
    rdfs:label "classified with"@en .

:has_notification_number
    rdf:type owl:ObjectProperty ;
    rdfs:label "has notification number"@en .
'''
    
    object_properties = '''
#################################################################
#    Object Properties
#################################################################

### 疾患分類
:0000001
    rdf:type owl:Class ;
    terms:identifier "0000001"^^xsd:string ;
    rdfs:label "難病疾患分類"@ja .

### 疾患分類 1
:0000002
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000002"^^xsd:string ;
    rdfs:label "神経・筋疾患"@ja .

### 疾患分類 2
:0000003
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000003"^^xsd:string ;
    rdfs:label "代謝系疾患"@ja .

### 疾患分類 3
:0000004
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000004"^^xsd:string ;
    rdfs:label "皮膚・結合組織疾患"@ja .

### 疾患分類 4
:0000005
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000005"^^xsd:string ;
    rdfs:label "免疫系疾患"@ja .

### 疾患分類 5
:0000006
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000006"^^xsd:string ;
    rdfs:label "循環器系疾患"@ja .

### 疾患分類 6
:0000007
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000007"^^xsd:string ;
    rdfs:label "血液系疾患"@ja .

### 疾患分類 7
:0000008
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000008"^^xsd:string ;
    rdfs:label "腎・泌尿器系疾患"@ja .

### 疾患分類 8
:0000009
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000009"^^xsd:string ;
    rdfs:label "骨・関節系疾患"@ja .

### 疾患分類 9
:0000010
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000010"^^xsd:string ;
    rdfs:label "内分泌系疾患"@ja .

### 疾患分類 10
:0000011
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000011"^^xsd:string ;
    rdfs:label "呼吸器系疾患"@ja .

### 疾患分類 11
:0000012
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000012"^^xsd:string ;
    rdfs:label "視覚系疾患"@ja .

### 疾患分類 12
:0000013
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000013"^^xsd:string ;
    rdfs:label "聴覚・平衡機能系疾患"@ja .

### 疾患分類 13
:0000014
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000014"^^xsd:string ;
    rdfs:label "消化器系疾患"@ja .

### 疾患分類 14
:0000015
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000015"^^xsd:string ;
    rdfs:label "染色体または遺伝子に変化を伴う症候群"@ja .

### 疾患分類 15
:0000016
    rdf:type owl:Class ;
    rdfs:subClassOf :0000001 ;
    terms:identifier "0000016"^^xsd:string ;
    rdfs:label "耳鼻科系疾患"@ja .

'''
    object_properties += _make_entity_chunk(json_list)
    ttl_text = '{}\n{}\n{}\n{}'.format(prefixes, ontology_property, annotation_properties, object_properties)

    return ttl_text


def _make_entity_chunk(json_list):
    chunk = ''
    for i, entity in enumerate(json_list):
        id = entity['id']
        if id == '0':
            continue
        name_ja = entity['name_ja']
        synonyms_ja = entity['synonyms_ja']
        name_en = entity['name_en']
        synonyms_en = entity['synonyms_en']
        mondo_ids = ', '.join([mn['id'] for mn in entity['mondo_nodes']]).replace(':', '_')
        url = entity['url']
        class_id = entity['class_id']
        class_id = '{:07}'.format(int(class_id)+1)
        
        comment = '### 指定難病{}'.format(id)
        nanbyo_id = ':{:07}'.format(i+16)
        # 3階層であることを前提
        if len(id.split('-')) == 1:
            top_class = nanbyo_id
            sub_class_of = 'mondo:MONDO_0000001'
        elif len(id.split('-')) == 2:
            middle_class = nanbyo_id
            sub_class_of = top_class
        elif len(id.split('-')) == 3:
            sub_class_of = middle_class
        
        labels, synonyms = _get_labels_and_synonyms(name_ja, name_en, synonyms_ja, synonyms_en)
        
        if mondo_ids:
            mondo_ids = ', '.join(['mondo:{}'.format(m_id) for m_id in mondo_ids.split(', ')])
            #mondo_ids = '<http://www.w3.org/2004/02/skos/core#exactMatch> {mondo_ids}'.format(mondo_ids=mondo_ids)
            mondo_ids = 'skos:closeMatch {mondo_ids}'.format(mondo_ids=mondo_ids)
        
        block = _get_block(comment, nanbyo_id, sub_class_of, labels, synonyms, id, class_id, url, mondo_ids)
        chunk += block

    return chunk


def _get_labels_and_synonyms(name_ja, name_en, synonyms_ja, synonyms_en):
    name_ja = [name_ja]
    name_en = [name_en]
    labels = '\n    '.join(['rdfs:label "{}"@ja ;'.format(n) for n in name_ja if n] + ['rdfs:label "{}"@en ;'.format(n) for n in name_en if n])[:-2]
    if ['"{}"@ja ,'.format(s) for s in synonyms_ja] + ['"{}"@en ,'.format(s) for s in synonyms_en]:
        #synonyms = 'oboinowl:hasExactSynonym ' + '\n                            '.join(['"{}"@ja ,'.format(s) for s in synonyms_ja] + ['"{}"@en ,'.format(s) for s in synonyms_en])
        synonyms = 'terms:altLabel ' + '\n                 '.join(['"{}"@ja ,'.format(s) for s in synonyms_ja] + ['"{}"@en ,'.format(s) for s in synonyms_en])
        synonyms = synonyms[:-2]
    else:
        synonyms = []

    return labels, synonyms


def _get_block(comment, nanbyo_id, sub_class_of, labels, synonyms, id, class_id, url, mondo_ids):
    sections = [
        'rdf:type owl:Class',
        'rdfs:subClassOf {sub_class_of}'.format(sub_class_of=sub_class_of),
        labels,
        synonyms,
        'terms:identifier "{nanbyo_id_num}"^^xsd:string'.format(nanbyo_id_num=nanbyo_id[1:]),
        ':has_notification_number "{id}"^^xsd:string'.format(id=id.split('-')[0]),
        ':classifiedWith :{class_id}'.format(class_id=class_id),
        'rdfs:isDefinedBy <{url}>'.format(url=url),
        'rdfs:seeAlso "xxxxxxxxxxxxxxxx"',
        mondo_ids
        ]
    
    sections = [s for s in sections if s]
    block = '{}\n{}\n    '.format(comment, nanbyo_id) +' ;\n    '.join(sections) + ' .\n\n'

    return block


if __name__ == '__main__':
    json_path = 'results/nanbyo2mondo_v4.json'
    with open(json_path) as f:
        json_list = json.load(f)
    ttl_text = json_to_ttl(json_list)
    with open('result.ttl', mode='w') as f:
        f.write(ttl_text)
