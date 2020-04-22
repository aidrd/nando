# NANDO

## 1. setting (Mac，Linuxで検証済み)
- `$ brew install raptor`
- `$ pipenv install`
- `$ pipenv shell`
- `$ ./setting.sh`

## 2. convert
1. TTL作成
    - `$ python -m converter`
1. RDF化
    - `$ rapper -i turtle -o rdfxml-abbrev results/nando.ttl > results/nando.rdf`
1. HTML化
    - `$ xsltproc --output results/nando.html data/owl2xhtml.xsl results/nando.rdf`
