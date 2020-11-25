import pandas as pd
import re

congress = pd.read_pickle('Data/Interim/congress_cleaned.pkl')

special_characters = ",._´&’%':€$£!?#"
character_set = {
    "characters": "abcdefghijklmnopqrstuvwxyz0123456789" + special_characters,
    "space": " ",
}
alphabet = "".join(character_set.values())


regex_links = re.compile("http\S+")
regex_whitespace = re.compile("[\s|-]+")
regex_unknown = re.compile(f"[^{alphabet}]+")

regex_html_tags = {
    "&amp": "and",
    "&lt": "<",
    "&gt": ">",
    "&quot": '"',
    "&apos": "'",
}

## Replace unicode charetars
for pattern_string, char in regex_html_tags.items():
    congress["text"] = congress["text"].str.replace(pattern_string, char)

congress["text"] = (congress["text"]
    .str.lower()
    .str.replace(regex_links, "")
    .str.replace(regex_whitespace, character_set["space"])
    .str.replace(regex_unknown, '')
    .str.strip()
)
congress.to_pickle('Data/Processed/congress_cleaned_processed.pkl')
