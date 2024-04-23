# NANDO 
NANDO（Nanbyo Disease Ontology）は，「指定難病」制度対象の疾患と「小児慢性特定疾病」制度対象の疾患について，国内においてオーソライズされた資料を元に，疾患概念と疾患同士の関係性を厳密に体系化したものである．また，国際的な疾患オントロジー<a href="https://github.com/monarch-initiative/mondo">MONDO</a>へのクロスリファレンスを含む．

The Nanbyo Disease Ontology (NANDO) is a structured resource that organizes vocabulary related to rare diseases, the relationships between these diseases, and their connections with other disease resources. Includes cross-references to the international disease ontology, MONDO<a href="https://github.com/monarch-initiative/mondo">MONDO</a>.

## 取得/Down loads
- http://nanbyodata.jp/ontology/nando.ttl
- http://nanbyodata.jp/ontology/nando.rdf

## 参照/References
- http://nanbyodata.jp/ontology/nando
- http://bioportal.bioontology.org/ontologies/NANDO

## 作成
#### 1. 設定 (Macで検証済み)
- `$ brew install raptor`
- `$ pipenv install`
- `$ pipenv shell`
- `$ ./setting.sh`

#### 2. ファイル作成
1. TTL
    - `$ python -m converter`
1. RDF
    - `$ rapper -i turtle -o rdfxml-abbrev results/nando.ttl > results/nando.rdf`
1. HTML
    - `$ xsltproc --output results/nando.html data/owl2xhtml.xsl results/nando.rdf`

## 統計情報
|| 全疾患 | 指定難病 | 小児慢性特定疾病 |
| --- | ---: | ---: | ---: |
| クラス数 | `2,777` | `1,099` | `1,676` |
| MONDOへのクロスリファレンスを含むクラス数 | `2154` | `892` | `1262` |

## ライセンス
<a href="https://creativecommons.org/licenses/by/4.0/deed.ja">CC-BY 4.0</a> | <a href="http://dbcls.rois.ac.jp">DBCLS</a>

## コンタクト
新しい用語のリクエストやクラスの修正依頼，オントロジーに関する問題点・疑問点の報告には，本リポジトリの <a href="https://github.com/aidrd/nando/issues">Issue tracker</a> をご利用ください．

## 出典
- 「概要、診断基準等」（厚生労働省）（https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000084783.html) <br>（2020年7月14日に利用）
- 「臨床調査個人票」（厚生労働省）（https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000084783.html) <br>（2020年7月14日に利用）
- 小児慢性特定疾病情報センター「概要」（https://www.shouman.jp/disease/search/group/) <br>（2020年7月14日に利用）
- 小児慢性特定疾病情報センター「意見書」（https://www.shouman.jp/disease/search/group/) <br>（2020年7月14日に利用）

- Sources
- Ministry of Health, Labour and Welfare, "Overview, Diagnostic Criteria, etc." (Accessed July 14, 2020)
- Ministry of Health, Labour and Welfare, "Clinical Survey Individual Sheet" (Accessed July 14, 2020)
- Center for Chronic Pediatric Diseases, "Overview" (Accessed July 14, 2020)
- Center for Chronic Pediatric Diseases, "Opinion Paper" (Accessed July 14, 2020)


## 謝辞
- 本オントロジーの構築に際して<a href="https://ddrare.nibiohn.go.jp/">DDrare</a>および<a href="https://metadb.riken.jp/metadb/ontology/RDVJ">RDVJ</a>を参照した．
- 本オントロジーの構築に<a href="http://biohackathon.org/">BioHackathon</a>の成果を利用した．

- Acknowledgements
The construction of this ontology was informed by references to DDrare and RDVJ. The results from the BioHackathon were also utilized in building this ontology.

