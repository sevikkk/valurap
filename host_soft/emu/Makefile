export::
	([ -d tmp ] && rm -rf tmp || echo ok )&& mkdir -p tmp && cd tmp && unzip ../motion3.wxmx
	python ./cleanup.py tmp/content.xml export/content.xml
	cp tmp/mimetype export
	cp tmp/format.txt export
	rm -r tmp

import::
	cd export && rm -f ../motion3_imp.wxmx && zip ../motion3_imp.wxmx format.txt mimetype content.xml
