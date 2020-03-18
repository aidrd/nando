#!/bin/sh

echo 'download mondo.obo'
wget -O data/mondo.obo http://purl.obolibrary.org/obo/mondo.obo
echo 'download faldo.ttl'
wget -O data/faldo.ttl https://raw.githubusercontent.com/OBF/FALDO/master/faldo.ttl
echo 'download owl2xhtml.xsl'
wget -O data/owl2xhtml.xsl https://raw.githubusercontent.com/OBF/FALDO/master/owl2xhtml.xsl
