# CLDF dataset derived from Ugarte et al.'s "NorthPeruLex - A Lexical Dataset of Small Language Families and Isolates from Northern Peru (forthcoming).

## How to cite

If you use these data please cite
- the original source
  > Ugarte, Carlos and Blum, Frederic and Ingunza, Adriano and Gonzales, Rosa and Peña, Jaime. Forthcoming. NorthPeruLex - A Lexical Dataset of Small Language Families and Isolates from Northern Peru.
- the derived dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


This dataset brings together lexical data from isolates and small language families from northern Peru to investigate their historic relations.

This dataset is licensed under a CC-BY-4.0 license


Conceptlists in Concepticon:
- [Swadesh-1952-200](https://concepticon.clld.org/contributions/Swadesh-1952-200)
## Notes

# Accessing the data
## Installing dependencies

The first step to access all the contents of the dataset is to clone the repository and install all the necessary requirements.

```
git clone https://github.com/lexibank/northperulex.git
cd northperulex
pip install -e .
```
This includes all packages used for the conversion to CLDF (Cross-Linguistic Data Formats: [https://cldf.clld.org](https://cldf.clld.org)). 
The NorthPeruLex dataset can also be downloaded directly as a ZIP file directly from this Github repository or from Zenodo ([10.5281/zenodo.13269802](10.5281/zenodo.13269802)).
If the user wishes to perform the CLDF conversion, they can run the following command:

```
cldfbench lexibank.makecldf lexibank_northperulex.py --concepticon-version=v3.4.0 --glottolog-version=v5.2.1 --clts-version=v2.3.0
```
This command uses the cldfbench package ([https://pypi.org/project/cldfbench/](https://pypi.org/project/cldfbench/)) with the pylexibank plug-in ([https://pypi.org/project/pylexibank/](https://pypi.org/project/pylexibank/)) to automatically convert the data to CLDF using the raw data at the `raw` folder and the latest version
(at the time of the publication of this dataset) of the references catalogs: Concepticon ([https://concepticon.clld.org/](https://concepticon.clld.org/)), for concept glosses; Glottolog ([https://glottolog.org/](https://glottolog.org/)), for language names; and CLTS ([https://clts.clld.org/](https://clts.clld.org/)), for the phonetic transcriptions.

The converted data is located in the `cldf` folder.
All data in the dataset is stored in tabular (CSV) files. Therefore, it can be read on various platforms and environments and manually inspected.

## Create the wordlist
We provided the user with a `\analysis\Makefile` file that creates a wordlist on a TSV file that can be used to manually inspect the data with the help
of EDICTOR web tool ([https://edictor.org/](https://edictor.org/)).
To produce the file, please run the following commands:

```
cd analysis
pip install -r requirements.txt
make wordlist
```


## Statistics


![Glottolog: 100%](https://img.shields.io/badge/Glottolog-100%25-brightgreen.svg "Glottolog: 100%")
![Concepticon: 100%](https://img.shields.io/badge/Concepticon-100%25-brightgreen.svg "Concepticon: 100%")
![Source: 100%](https://img.shields.io/badge/Source-100%25-brightgreen.svg "Source: 100%")
![BIPA: 100%](https://img.shields.io/badge/BIPA-100%25-brightgreen.svg "BIPA: 100%")
![CLTS SoundClass: 100%](https://img.shields.io/badge/CLTS%20SoundClass-100%25-brightgreen.svg "CLTS SoundClass: 100%")

- **Varieties:** 35 (linked to 35 different Glottocodes)
- **Concepts:** 200 (linked to 200 different Concepticon concept sets)
- **Lexemes:** 4,986
- **Sources:** 21
- **Synonymy:** 1.12
- **Cognacy:** 4,986 cognates in 3,660 cognate sets (2,905 singletons)
- **Cognate Diversity:** 0.72
- **Invalid lexemes:** 0
- **Tokens:** 29,552
- **Segments:** 178 (0 BIPA errors, 0 CLTS sound class errors, 178 CLTS modified)
- **Inventory size (avg):** 29.83

# Contributors

Name | GitHub user   | Description                                     | Role
--- |---------------|-------------------------------------------------| ---
Carlos Ugarte | @CMUgarte     | Data collector, CLDF conversion and annotation  | Author, Editor
Frederic Blum | @FredericBlum | CLDF conversion and annotation | Author, Editor
Adriano Ingunza | @BadBatched   | Data collector and annotation                   | Author
Rosa Gonzales | @rosalgm      | Data collector and annotation                   | Author
Jaime Peña | @JaimePenat   | Data collector and annotation                   | Author




## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [Wordlist](https://github.com/cldf/cldf/tree/master/modules/Wordlist) at [cldf/cldf-metadata.json](cldf/cldf-metadata.json)