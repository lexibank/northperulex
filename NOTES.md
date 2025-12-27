### Accessing the data
#### Installing dependencies

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

#### Create the wordlist
We provided the user with a `analysis\Makefile` file that creates a wordlist on a TSV file that can be used to manually inspect the data with the help
of EDICTOR web tool ([https://edictor.org/](https://edictor.org/)).
To produce the file, please run the following commands:

```
cd analysis
pip install -r requirements.txt
make wordlist
```

In addition to yielding the word list file (`npl_data.tsv`), the Makefile
also runs a script that performs the multiple sequence alignment and an 
automatic recognition of sound correspondence patterns. To do so, please
type the following:

```shell
make analysis
```
The result of both processes are stored in the files `npl_msaligned` 
and `npl_patterns.tsv`.