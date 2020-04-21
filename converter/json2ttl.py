"""
main.pyでMondoと紐付けたnanbyo2mondo, shoman2mondoを使ってttlファイルを作成
$ python json2ttl.py results/nanbyo2mondo_v4.json results/shoman2mondo_v4.json results/nando.ttl
"""
import json
from pathlib import Path
from typing import Dict, Union, List

from pynando.nando import Nando
from pynando.data import find
from .config import Config

NANBYOCLASS2NANDO = {}
NANBYO2NANDO = {}
SHOMANCLASS2NANDO = {}
SHOMAN2NANDO = {}

OBSOLETE_CLASS_ID = '0000002'


def zero_pad(_id: Union[str, int], head: str, digit: int=7):
    """
    通し番号をゼロ埋め
    難病疾患分類, 難病, 小慢疾患分類, 小慢ごとに1桁目の数字を区分
    e.g. 難病疾患分類は0000001から始まり、難病は1000001から始まる
    :param _id:
    :param head:
    :param digit:
    :return:
    """
    if type(_id) == int:
        _id = str(_id)
    return head + _id.zfill(digit - 2)


def x_to_nando(mapper: Dict, x_id: int):
    """
    各オントロジーのidからNandoの通し番号に変換
    :param mapper:
    :param x_id:
    :return:
    """
    return mapper[x_id]


def nando_to_x(mapper: Dict, nando_id: int):
    """
    Nandoの通し番号から各オントロジーのidに変換
    :param mapper:
    :param nando_id:
    :return:
    """
    return {v: k for k, v in mapper.items()}[nando_id]


def lines_to_doc(lines: List[str]):
    """
    エンティティに関する複数業の情報をまとめる
    :param lines:
    :return:
    """
    doc = '\n'.join(lines)
    doc = doc[:-1] + '.'
    return doc


def top_concept_to_ttl():
    """
    難病（最上位概念）のttl化
    :return:
    """
    _id = 1
    head = '00'
    doc_list = []

    id_zero_padded = zero_pad(_id, head)
    lines = [
        '### 難病',
        ':{}'.format(id_zero_padded),
        ' ' * 4 + 'rdf:type owl:Class ;',
        ' ' * 4 + 'rdfs:subClassOf mondo:MONDO_0000001 ;',
        ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
        ' ' * 4 + 'rdfs:label "難病"@ja ;',
    ]
    doc = lines_to_doc(lines)
    doc_list.append(doc)
    _id += 1

    id_zero_padded = zero_pad(_id, head)
    lines = [
        '### obsolete class',
        ':{}'.format(id_zero_padded),
        ' ' * 4 + 'rdf:type owl:Class ;',
        ' ' * 4 + 'rdfs:subClassOf owl:Thing ;',
        ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
        ' ' * 4 + 'rdfs:label "obsolete class"@en ;',
        ' ' * 4 + 'efo:definition "NANDO number no more in use."@en ;',
    ]
    doc = lines_to_doc(lines)
    doc_list.append(doc)

    return '\n\n'.join(doc_list)


def nanbyo_top_concept_to_ttl():
    """
    指定難病のttl化
    :return:
    """
    _id = 1
    head = '10'
    doc_list = []

    id_zero_padded = zero_pad(_id, head)
    parent_id = '0000001'
    lines = [
        '### 指定難病',
        ':{}'.format(id_zero_padded),
        ' ' * 4 + 'rdf:type owl:Class ;',
        ' ' * 4 + 'rdfs:subClassOf :{} ;'.format(parent_id),
        ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
        ' ' * 4 + 'rdfs:label "指定難病"@ja ;',
    ]
    doc = lines_to_doc(lines)
    doc_list.append(doc)
    return '\n\n'.join(doc_list)


def nanbyo_class_to_ttl(fp: Path):
    """
    指定難病 分類のttl化
    :param fp:
    :return:
    """
    global NANBYOCLASS2NANDO
    _id = 1
    head = '11'
    doc_list = []

    parent_id = '1000001'
    with fp.open() as f:
        nando_class_nodes = json.load(f)
    for nando_class_node in nando_class_nodes:
        id_zero_padded = zero_pad(_id, head)
        name_ja = nando_class_node['name_ja']
        name_en = nando_class_node['name_en']
        NANBYOCLASS2NANDO[nando_class_node['id']] = id_zero_padded
        lines = [
            '### {}'.format(name_ja),
            ':{}'.format(id_zero_padded),
            ' ' * 4 + 'rdf:type owl:Class ;',
            ' ' * 4 + 'rdfs:subClassOf :{} ;'.format(parent_id),
            ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
            ' ' * 4 + 'rdfs:label "{}"@ja ;'.format(name_ja),
        ]
        if nando_class_node['name_en']:
            lines += [' ' * 4 + 'oboinowl:hasExactSynonym "{}"@en ;'.format(name_en)]
        doc = lines_to_doc(lines)
        doc_list.append(doc)
        _id += 1
    return '\n\n'.join(doc_list)


def nanbyo_to_ttl(target: str, data_dir: Path):
    """
    指定難病 疾患のttl化
    :param fp:
    :return:
    """
    global NANBYO2NANDO
    _id = 1
    head = '12'
    doc_list = []

    for nando_node in Nando(target, data_dir):
        if nando_node.id == '0':
            continue

        id_zero_padded = zero_pad(_id, head)
        NANBYO2NANDO[nando_node.id] = id_zero_padded

        # parent_id
        if '-' not in nando_node.id:
            parent_id = x_to_nando(NANBYOCLASS2NANDO, nando_node.class_id)
        else:
            parent_id = NANBYO2NANDO[nando_node.id.rsplit('-', 1)[0]]
        # obsolete
        if nando_node.obsolete:
            parent_id = OBSOLETE_CLASS_ID

        # exact_synonym
        exact_synonym_list = []
        for synonym in nando_node.synonyms_ja:
            if not synonym:
                continue
            exact_synonym_list.append('"{}"@ja ,'.format(synonym))
        for synonym in [nando_node.name_en] + nando_node.synonyms_en:
            if not synonym:
                continue
            exact_synonym_list.append('"{}"@en ,'.format(synonym))
        
        exact_synonym = ('\n' + ' ' * 29).join(exact_synonym_list)
        exact_synonym = exact_synonym[:-2]

        # description
        description = nando_node.description

        # see_also
        see_also_list = []
        for see_also in nando_node.see_also:
            see_also_list.append('<{}> ,'.format(see_also))
        see_also = ('\n' + ' ' * 17).join(see_also_list)
        see_also = see_also[:-2]

        # mondo
        mondo_list = []
        for mondo in nando_node.mondo_nodes:
            mondo_list.append('mondo:{} ,'.format(mondo.id))
        mondo = ('\n' + ' ' * 53).join(mondo_list)
        mondo = mondo[:-2]

        lines = [
            '### 指定難病 {}'.format(nando_node.id),
            ':{}'.format(id_zero_padded),
            ' ' * 4 + 'rdf:type owl:Class ;',
            ' ' * 4 + 'rdfs:subClassOf :{} ;'.format(parent_id),
            ' ' * 4 + 'rdfs:label "{}"@ja ;'.format(nando_node.name_ja),
            ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
            ' ' * 4 + ':has_notification_number "{}"^^xsd:string ;'.format(nando_node.notification_no),
        ]
        if nando_node.is_defined_by:
            lines += [' ' * 4 + 'rdfs:isDefinedBy <{}> ;'.format(nando_node.is_defined_by)]
        if exact_synonym:
            lines += [' ' * 4 + 'oboinowl:hasExactSynonym {} ;'.format(exact_synonym)]
        if description:
            lines += [' ' * 4 + 'efo: definition "{}"@ja ;'.format(description)]
        if see_also:
            lines += [' ' * 4 + 'rdfs:seeAlso {} ;'.format(see_also)]
        if mondo:
            lines += [' ' * 4 + '<http://www.w3.org/2004/02/skos/core#exactMatch> {} ;'.format(mondo)]

        doc = lines_to_doc(lines)
        doc_list.append(doc)
        _id += 1

    return '\n\n'.join(doc_list)


def shoman_top_concept_to_ttl():
    """
    小児慢性特定疾病のttl化
    :return:
    """
    _id = 1
    head = '20'
    doc_list = []

    id_zero_padded = zero_pad(_id, head)
    parent_id = '0000001'
    lines = [
        '### 小児慢性特定疾病',
        ':{}'.format(id_zero_padded),
        ' ' * 4 + 'rdf:type owl:Class ;',
        ' ' * 4 + 'rdfs:subClassOf :{} ;'.format(parent_id),
        ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
        ' ' * 4 + 'rdfs:label "小児慢性特定疾病"@ja ;',
    ]
    doc = lines_to_doc(lines)
    doc_list.append(doc)
    return '\n\n'.join(doc_list)


def shoman_class_to_ttl(fp: Path):
    """
    小児慢性特定疾病 分類のttl化
    :param fp:
    :return:
    """
    global SHOMANCLASS2NANDO
    _id = 1
    head = '21'
    doc_list = []

    # 疾患分類個別クラス
    with fp.open() as f:
        nando_class_nodes = json.load(f)
    for nando_class_node in nando_class_nodes:
        nando_class_id = nando_class_node['id']
        name_ja = nando_class_node['name_ja']
        name_en = nando_class_node['name_en']
        id_zero_padded = zero_pad(_id, head)
        SHOMANCLASS2NANDO[nando_class_id] = id_zero_padded

        # parent_id
        if '-' not in nando_class_id:
            parent_id = '2000001'
        else:
            parent_id = '{}'.format(SHOMANCLASS2NANDO[nando_class_id.rsplit('-', 1)[0]])


        lines = [
            '### {}'.format(name_ja),
            ':{}'.format(id_zero_padded),
            ' ' * 4 + 'rdf:type owl:Class ;',
            ' ' * 4 + 'rdfs:subClassOf :{} ;'.format(parent_id),
            ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
            ' ' * 4 + 'rdfs:label "{}"@ja ;'.format(name_ja),
        ]
        if name_en:
            lines += [' ' * 4 + 'oboinowl:hasExactSynonym "{}"@en ;'.format(name_en)]
        doc = lines_to_doc(lines)
        doc_list.append(doc)
        _id += 1
    return '\n\n'.join(doc_list)


def shoman_to_ttl(target: str, data_dir: Path):
    """
    小慢疾患クラスのttl化
    nanbyo_to_ttl()とほとんど同じだが固有の処理が入るかもしれないので関数を分けておく
    :param fp:
    :return:
    """
    global SHOMAN2NANDO
    _id = 1
    head = '22'
    doc_list = []

    for nando_node in Nando(target, data_dir):
        if nando_node.id == '0':
            continue

        id_zero_padded = zero_pad(_id, head)
        SHOMAN2NANDO[nando_node.id] = id_zero_padded

        # parent_id
        if '-' not in nando_node.id:
            parent_id = x_to_nando(SHOMANCLASS2NANDO, nando_node.class_id)
        else:
            parent_id = '{}'.format(SHOMAN2NANDO[nando_node.id.rsplit('-', 1)[0]])
        # obsolete
        if nando_node.obsolete:
            parent_id = OBSOLETE_CLASS_ID

        # exact_synonym
        exact_synonym_list = []
        for synonym in nando_node.synonyms_ja:
            if not synonym:
                continue
            exact_synonym_list.append('"{}"@ja ,'.format(synonym))
        for synonym in [nando_node.name_en] + nando_node.synonyms_en:
            if not synonym:
                continue
            exact_synonym_list.append('"{}"@en ,'.format(synonym))
        exact_synonym = ('\n' + ' ' * 29).join(exact_synonym_list)
        exact_synonym = exact_synonym[:-2]

        # description
        description = nando_node.description

        # see_also
        see_also_list = []
        for see_also in nando_node.see_also:
            see_also_list.append('<{}> ,'.format(see_also))
        see_also = ('\n' + ' ' * 17).join(see_also_list)
        see_also = see_also[:-2]

        # mondo
        mondo_list = []
        for mondo in nando_node.mondo_nodes:
            mondo_list.append('mondo:{} ,'.format(mondo.id))
        mondo = ('\n' + ' ' * 53).join(mondo_list)
        mondo = mondo[:-2]

        lines = [
            '### 小児慢性特定疾病 {}'.format(nando_node.id),
            ':{}'.format(id_zero_padded),
            ' ' * 4 + 'rdf:type owl:Class ;',
            ' ' * 4 + 'rdfs:subClassOf :{} ;'.format(parent_id),
            ' ' * 4 + 'rdfs:label "{}"@ja ;'.format(nando_node.name_ja),
            ' ' * 4 + 'terms:identifier "{}"^^xsd:string ;'.format(id_zero_padded),
            ' ' * 4 + ':has_notification_number "{}"^^xsd:string ;'.format(nando_node.notification_no),
        ]
        if nando_node.is_defined_by:
            lines += [' ' * 4 + 'rdfs:isDefinedBy <{}> ;'.format(nando_node.is_defined_by)]
        if exact_synonym:
            lines += [' ' * 4 + 'oboinowl:hasExactSynonym {} ;'.format(exact_synonym)]
        if description:
            lines += [' ' * 4 + 'efo: definition "{}"@ja ;'.format(description)]
        if see_also:
            lines += [' ' * 4 + 'rdfs:seeAlso {} ;'.format(see_also)]
        if mondo:
            lines += [' ' * 4 + '<http://www.w3.org/2004/02/skos/core#exactMatch> {} ;'.format(mondo)]

        doc = lines_to_doc(lines)
        doc_list.append(doc)
        _id += 1
    return '\n\n'.join(doc_list)


def main():
    doc_list = []
    config = Config()
    data_dir = config.DATA_DIR
    fp_nanbyo_class = find('nanbyo_class', data_dir)
    fp_shoman_class = find('shoman_class', data_dir)

    # 前半部分は手書きのファイルを読み込み
    with Path(config.NANDO_FRONT_PATH).open() as f:
        front = f.read()
    doc_list.append(front)

    # 難病（最上位概念）
    doc_list.append(top_concept_to_ttl())

    # 指定難病
    doc_list.append(nanbyo_top_concept_to_ttl())
    # 指定難病 分類
    doc_list.append(nanbyo_class_to_ttl(fp_nanbyo_class))
    # 指定難病 疾患
    doc_list.append(nanbyo_to_ttl('nanbyo', data_dir))

    # 小児特定慢性疾
    doc_list.append(shoman_top_concept_to_ttl())
    # 小児特定慢性疾病 分類
    doc_list.append(shoman_class_to_ttl(fp_shoman_class))
    # 小児特定慢性疾病 疾患
    doc_list.append(shoman_to_ttl('shoman', data_dir))

    doc = '\n\n'.join(doc_list)

    output_file_path = config.RESULTS_DIR / 'nando.ttl'
    with Path(output_file_path).open(mode='w') as f:
        f.write(doc)
