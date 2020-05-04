# NANDO (Nanbyo Disease Ontology)
本オントロジー は，「指定難病」制度対象の333疾患と「小児慢性特定疾病」制度対象の762疾患について，国内においてオーソライズされた資料を元に，疾患概念と疾患同士の関係性を厳密に体系化したものである．国際的な疾患オントロジー<a href="https://github.com/monarch-initiative/mondo">MONDO</a>へのクロスリファレンスを含む．

## 取得
- http://nanbyodata.jp/ontology/nando.ttl
- http://nanbyodata.jp/ontology/nando.rdf

## 参照
- http://nanbyodata.jp/ontology/nando
- http://bioportal.bioontology.org/ontologies/NANDO

## 作成
#### 1. setting (Mac，Linuxで検証済み)
- `$ brew install raptor`
- `$ pipenv install`
- `$ pipenv shell`
- `$ ./setting.sh`

#### 2. convert
1. TTL作成
    - `$ python -m converter`
1. RDF化
    - `$ rapper -i turtle -o rdfxml-abbrev results/nando.ttl > results/nando.rdf`
1. HTML化
    - `$ xsltproc --output results/nando.html data/owl2xhtml.xsl results/nando.rdf`

## 統計情報
| --- | --- |
| 全疾患 | 2,348件 |
| 指定難病 | 1,023件 |
| 小児慢性特定疾病 | 1,323件 |
| MONDOへのクロスリファレンスを含む疾患 | 1,372件 |
| 英語表記を含む疾患 | 2,288件 |
| 疾患定義を含む疾患 | 1,190件 |


