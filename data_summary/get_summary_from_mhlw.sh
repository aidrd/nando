
# make output directories
today=`date "+%Y%m%d"`
outdir="./mhlw_${today}"
outdir_docx="./mhlw_${today}/docx"
mkdir -p $outdir_docx

# download html files from mhlw
wget https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000062437.html -O ${outdir}/1_110.html
wget https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000079293.html -O ${outdir}/111_306.html
wget https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000085261.html -O ${outdir}/307_330.html
wget https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000197628.html -O ${outdir}/331.html
wget https://www.mhlw.go.jp/stf/newpage_05467.html -O ${outdir}/332_333.html

# retrieve urls from html files
grep "概要、診断基準等" ${outdir}/1_110.html | perl -nle 'print "https://www.mhlw.go.jp".$1 if (/(\/file[^"]*)/)' > ${outdir}/1_110.url
grep "概要、診断基準等" ${outdir}/111_306.html | perl -nle 'print "https://www.mhlw.go.jp".$1 if (/(\/file[^"]*)/)' > ${outdir}/111_306.url
grep "概要、診断基準等" ${outdir}/307_330.html | perl -nle 'print "https://www.mhlw.go.jp".$1 if (/(\/file[^"]*)/)' > ${outdir}/307_330.url
grep "概要、診断基準等" ${outdir}/331.html | perl -nle 'print "https://www.mhlw.go.jp".$1 if (/(\/file[^"]*)/)' > ${outdir}/331.url
grep "概要、診断基準等" ${outdir}/332_333.html | perl -nle 'print "https://www.mhlw.go.jp".$1 if (/(\/content[^"]*)/)' > ${outdir}/332_333.url

# retrieve a public notification of each nanbyo from a html file
grep "xl66" ${outdir}/1_110.html |grep "42pt" | perl -nle 'print $1 if (/56\"\>([\d]*)/)' > ${outdir}/1_110.num
grep "39pt" ${outdir}/111_306.html |grep 52 |egrep "(xl71|xl67)" | perl -nle 'print $1 if (/52\"\>([\d]*)/)' > ${outdir}/111_306.num
grep "41pt" ${outdir}/307_330.html |grep 54 |egrep "(xl69|xl70)" | perl -nle 'print $1 if (/54\"\>([\d]*)/)' > ${outdir}/307_330.num
grep "xl69" ${outdir}/331.html |grep "41pt" | perl -nle 'print $1 if (/54\"\>([\d]*)/)' > ${outdir}/331.num
grep "0px" ${outdir}/332_333.html |grep "55px" |grep -v "strong" | perl -nle 'print $1 if (/55px\;\"\>([\d]*)/)' > ${outdir}/332_333.num

# merge a public notification and a url of each nanbyo
paste ${outdir}/1_110.num ${outdir}/1_110.url |sort -n > ${outdir}/1_110.num.url.tsv
paste ${outdir}/111_306.num ${outdir}/111_306.url |sort -n > ${outdir}/111_306.num.url.tsv
paste ${outdir}/307_330.num ${outdir}/307_330.url |sort -n > ${outdir}/307_330.num.url.tsv
paste ${outdir}/331.num ${outdir}/331.url |sort -n > ${outdir}/331.num.url.tsv
paste ${outdir}/332_333.num ${outdir}/332_333.url |sort -n > ${outdir}/332_333.num.url.tsv

# merge all tsv files
cat ${outdir}/1_110.num.url.tsv ${outdir}/111_306.num.url.tsv ${outdir}/307_330.num.url.tsv ${outdir}/331.num.url.tsv ${outdir}/332_333.num.url.tsv > ${outdir}/1_333.num.url.tsv

# download a doc or docx file of each nanbyo from mhlw
cut -f2 ${outdir}/1_333.num.url.tsv |while read line; do echo $line; wget $line -P ${outdir_docx}; done

# convert doc to docx
## using libreoffice (soffice) to convert *.doc to *.docx
### https://blog.katsubemakito.net/centos/install_libreoffice_with_yum
### https://stackoverflow.com/questions/52277264/convert-doc-to-docx-using-soffice-not-working
for i in ${outdir_docx}/*.doc; do echo $i; soffice --headless --convert-to docx --outdir ${outdir_docx} $i; done

# correspondence of a public notification and a docx file name with converting *.doc to *.docx
sed -e 's/https\:\/\/www\.mhlw\.go\.jp\/file\/06\-Seisakujouhou\-10900000\-Kenkoukyoku\///g' ${outdir}/1_333.num.url.tsv |sed -e 's/https\:\/\/www\.mhlw\.go\.jp\/content\/10900000\///g' |sed -e 's/doc$/docx/g' > ${outdir}/1_333.num.docx.tsv

# output summary
## $ python --version
## Python 3.6.8
## $ pip list
## Package     Version
## ----------- -------
## lxml        4.5.0  
## pip         20.0.2 
## python-docx 0.8.10 
## setuptools  46.0.0 
## wheel       0.34.2 
cat ${outdir}/1_333.num.docx.tsv |while read line; do export IFS=$'\t'; set -- ${line}; echo -ne "$1\t$2\t"; python ./retrieve_txt_from_mhlw_docx.py ${outdir_docx}/$2; echo ""; done > ${outdir}/1_333.num.summary.tsv
