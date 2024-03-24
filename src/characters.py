import json


def get_all_characters() -> list[str]:
    with open("./src/characters.json") as f:
        characters = json.load(f)

    characters = characters["Characters"]

    characters = [
        c["name"]
        for c in characters
        if c["name"] != "random"
        and c["name"] != "pokémon trainer"
        and c["name"] != "pyra / mythra"
        and c["name"] != "steve / alex"
    ]

    characters.append("pyra")
    characters.append("mythra")
    characters.append("squirtle")
    characters.append("ivysaur")
    characters.append("charizard")
    characters.append("steve")

    return characters


def get_characters_url(character: str) -> str:
    if character == "squirtle":
        return "pt_squirtle"
    elif character == "ivysaur":
        return "pt_ivysaur"
    elif character == "charizard":
        return "pt_charizard"

    return character.replace(" ", "_").replace(".", "").replace("&", "and")
