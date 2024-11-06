import csv
from glob import glob


final_data = [[
    "Doculect", "Concept", "Form", "Notes"
]]

data = list(sorted(glob("prepared_data/*.tsv")))

replacements = {
    "Resígaro": "Resigaro",
    "Witoto Mi̵ni̵ca": "WitotoMinica",
    "Witoto Murui" : "WitotoMurui",
    "Witoto Ni̵pode": "WitotoNipode"
}

# Load manually digitized data
def add_wl(language):
    """Adds data from languages in folder."""
    if "Iquito.tsv" in language:
        return

    if "lexibank.tsv" in language:
        return

    if "Ticuna.tsv" in language:
        return
    
    with open(language, mode='r', encoding="utf8") as f:
        wl = csv.reader(f, delimiter="\t")
        header = next(wl)
        if "Spanish" in header:
            for entry in wl:
                if entry[2] != "":
                    final_data.append(entry[:-1])
        elif "Gloss" in header:
            for entry in wl:
                if entry[2] != "":
                    final_data.append(entry[:-1])
        else:
            for entry in wl:
                if entry[2] != "":
                    final_data.append(entry)


# Load Iquito data
with open("prepared_data/Iquito.tsv", mode='r', encoding="utf8") as file:
    d = csv.reader(file, delimiter="\t")
    next(d)
    for lines in d:
        final_data.append([
            "Iquito",
            lines[2],  # Gloss
            lines[3],  # Form
            lines[5]   # Note --> SENSE in dictionary
        ])

# Load Ticuna data
with open("prepared_data/Ticuna.tsv", mode='r', encoding="utf8") as file:
    d = csv.reader(file, delimiter="\t")
    next(d)
    for lines in d:
        final_data.append([
            "Ticuna",
            lines[2], # Gloss
            lines[3],  # Form
            lines[5]   # Note --> SENSE in dictionary
        ])

# Load Lexibank data
with open("prepared_data/lexibank.tsv", mode='r', encoding="utf8") as file:
    d = csv.reader(file, delimiter="\t")
    next(d)
    for lines in d:
        doculect = lines[0]
        if doculect in replacements:
            doculect = replacements[doculect]
        final_data.append([
            doculect,
            lines[1],  # Gloss
            lines[2],  # Form
            ""         # Note
        ])


# Check that everything is alright
for lang in data:
    add_wl(lang)

with open("raw.tsv", "w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(final_data)
