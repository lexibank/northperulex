import csv
import sqlite3
import tqdm


LB_QUERY = """
SELECT
    ROW_NUMBER() OVER(),
	l.cldf_name,
	p.concepticon_gloss,
	f.cldf_form
FROM
	languagetable as l,
	parametertable as p,
	formtable as f
WHERE
	f.cldf_languagereference = l.cldf_id
		AND
	f.cldf_parameterreference = p.cldf_id
		AND
	p.core_concept like "%Swadesh-1952-200%"
        AND
    l.cldf_glottocode IN ("arab1268", "cand1248", "muni1258", "taus1253", "waor1240", "agua1253")
;
"""

ATTACH_LB = """ATTACH 'cldf-data/lexibank-analysed/lexibank.sqlite3' AS lb;"""
SEB_QUERY = """
SELECT
    ROW_NUMBER() OVER(),
	l.cldf_name,
	p.concepticon_gloss,
	f.cldf_form
FROM
	languagetable as l,
	parametertable as p,
	formtable as f
INNER JOIN
    (
        SELECT
            f_1.cldf_id
        FROM
            formtable as f_1,
            parametertable as p_1,
            lb.parametertable as p_2
        WHERE
            f_1.cldf_parameterReference = p_1.cldf_id
                AND
            p_1.concepticon_gloss = p_2.cldf_name
                AND
            p_2.core_concept like "%Swadesh-1952-200%"
    ) as c
ON
    c.cldf_id = f.cldf_id
WHERE
	f.cldf_languageReference = l.cldf_id
		AND
	f.cldf_parameterReference = p.cldf_id
;
"""


def get_db(path):
    con = sqlite3.connect(path)
    return con.cursor()


output_data = [[
    'Doculect',
    'Concept',
    'Form'
]]

db = get_db('cldf-data/lexibank-analysed/lexibank.sqlite3')
db.execute(LB_QUERY)

for idx, doculect, gloss, form in tqdm.tqdm(db.fetchall()):
    print(idx, doculect, gloss, form)
    output_data.append([
        doculect, gloss, form
    ])

db = get_db('cldf-data/seifartecheverriboran/seifartecheverriboran.sqlite3')
db.execute(ATTACH_LB)
db.execute(SEB_QUERY)

for idx, doculect, gloss, form in tqdm.tqdm(db.fetchall()):
    print(idx, doculect, gloss, form)
    output_data.append([
        doculect, gloss, form
    ])

with open('imported/lexibank.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(output_data)