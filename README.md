# NANDO 
NANDO（Nanbyo Disease Ontology）は，「指定難病」制度対象の疾患と「小児慢性特定疾病」制度対象の疾患について，国内においてオーソライズされた資料を元に，疾患概念と疾患同士の関係性を厳密に体系化したものである．また，国際的な疾患オントロジー<a href="https://github.com/monarch-initiative/mondo">MONDO</a>へのクロスリファレンスを含む．

## 取得
- http://nanbyodata.jp/ontology/nando.ttl
- http://nanbyodata.jp/ontology/nando.rdf

## 参照
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
| クラス数 | `2,347` | `1,023` | `1,323` |
| 英語表記を含むクラス数 | `2,284` | `991` | `1,292` |
| 疾患定義を含むクラス数 | `1,189` | `333` | `856` |
| MONDOへのクロスリファレンスを含むクラス数 | `1,382` | `698` | `684` |

## ライセンス
<a href="https://creativecommons.org/licenses/by/4.0/deed.ja">CC-BY 4.0</a> | <a href="http://dbcls.rois.ac.jp">DBCLS</a>

## コンタクト
新しい用語のリクエストやクラスの修正依頼，オントロジーに関する問題点・疑問点の報告には，本リポジトリの <a href="https://github.com/aidrd/nando/issues">Issue tracker</a> をご利用ください．

## 出典
- 「概要、診断基準等」（厚生労働省）（https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000084783.html) <br>（2020年7月14日に利用）
- 「臨床調査個人票」（厚生労働省）（https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000084783.html) <br>（2020年7月14日に利用）

## 謝辞
- 本オントロジーの構築に際して<a href="https://ddrare.nibiohn.go.jp/">DDrare</a>および<a href="https://metadb.riken.jp/metadb/ontology/RDVJ">RDVJ</a>を参照した．
- 本オントロジーの構築に<a href="http://biohackathon.org/">BioHackathon</a>の成果を利用した．
