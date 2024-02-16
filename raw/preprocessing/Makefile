download:
	git clone https://github.com/lexibank/seifartecheverriboran cldf-data/seifartecheverriboran
	git clone https://github.com/lexibank/lexibank-analysed --branch v1.0 cldf-data/lexibank-analysed
	git clone https://github.com/concepticon/concepticon-data cldf-data/concepticon-data
	git clone https://github.com/lexibank/crossandean cldf-data/crossandean
	cldf createdb cldf-data/lexibank-analysed/cldf/wordlist-metadata.json cldf-data/lexibank-analysed/lexibank.sqlite3
	cldf createdb cldf-data/seifartecheverriboran/cldf/cldf-metadata.json cldf-data/seifartecheverriboran/seifartecheverriboran.sqlite3
	cldf createdb cldf-data/crossandean/cldf/cldf-metadata.json cldf-data/crossandean/crossandean.sqlite3