import requests
import aiosqlite
from bs4 import BeautifulSoup

import src.characters


async def populate_moves(characters: list[str]) -> None:
    async with aiosqlite.connect("./db/ultimateframedata.db") as db:
        for character in characters:
            character_url = src.characters.get_characters_url(character)

            r = requests.get(f"https://ultimateframedata.com/{character_url}.php")

            soup = BeautifulSoup(r.text, "html.parser")

            moves = [x for x in soup.find_all("div", {"class": "movecontainer"})]

            special_names = []

            for move in moves:

                movename = move.find("div", {"class": "movename"})
                startup = move.find("div", {"class": "startup"})
                totalframes = move.find("div", {"class": "totalframes"})
                landinglag = move.find("div", {"class": "landinglag"})
                notes = move.find("div", {"class": "notes"})
                basedamage = move.find("div", {"class": "basedamage"})
                shieldlag = move.find("div", {"class": "shieldlag"})
                shieldstun = move.find("div", {"class": "shieldstun"})
                advantage = move.find("div", {"class": "advantage"})
                activeframes = move.find("div", {"class": "activeframes"})
                endlag = move.find("div", {"class": "endlag"})
                autocancels = move.find("div", {"class": "hopsautocancel"})
                actionable_before_landing = move.find(
                    "div", {"class": "hopsactionable"}
                )
                hitbox = move.find("div", {"class": "hitbox"})

                if movename:
                    movename = movename.text.replace("\n", "").replace("\t", "")

                movename_smash = None

                if movename and "(" in movename:
                    movename_smash = movename.split("(")[1].replace(")", "")
                    movename = movename.split(" (")[0]

                    special_names.append([movename_smash, movename])

                for special in special_names:
                    if special[0] in movename:
                        movename_smash = movename
                        movename = special[1]

                print(f"Movename: {movename}, Movename Smash: {movename_smash}")

                if startup:
                    startup = (
                        startup.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if totalframes:
                    totalframes = (
                        totalframes.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if landinglag:
                    landinglag = (
                        landinglag.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if notes:
                    notes = (
                        notes.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if basedamage:
                    basedamage = (
                        basedamage.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if shieldlag:
                    shieldlag = (
                        shieldlag.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if shieldstun:
                    shieldstun = (
                        shieldstun.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if advantage:
                    advantage = (
                        advantage.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if activeframes:
                    activeframes = (
                        activeframes.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if endlag:
                    endlag = (
                        endlag.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if autocancels:
                    autocancels = (
                        autocancels.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if actionable_before_landing:
                    actionable_before_landing = (
                        actionable_before_landing.text.replace("\n", "")
                        .replace("\t", "")
                        .replace("**", "--")
                    )

                if hitbox:
                    if hitbox.find("img"):
                        hitbox = f"https://ultimateframedata.com/{hitbox.find('img')['data-src']}"
                    else:
                        hitbox = None

                if movename != "Stats":
                    await db.execute(
                        """INSERT INTO moves VALUES (
                        :character,
                        :move_name,
                        :move_name_smash,
                        :frame_startup,
                        :frame_active,
                        :frame_endlag,
                        :frame_onshield,
                        :frame_shieldlag,
                        :frame_shieldstun,
                        :frame_total,
                        :autocancels,
                        :actionable_before_landing,
                        :damage,
                        :hitbox_gif,
                        :notes)""",
                        {
                            "character": character,
                            "move_name": movename,
                            "move_name_smash": movename_smash,
                            "frame_startup": startup,
                            "frame_active": activeframes,
                            "frame_endlag": endlag,
                            "frame_onshield": advantage,
                            "frame_shieldlag": shieldlag,
                            "frame_shieldstun": shieldstun,
                            "frame_total": totalframes,
                            "autocancels": autocancels,
                            "actionable_before_landing": actionable_before_landing,
                            "damage": basedamage,
                            "hitbox_gif": hitbox,
                            "notes": notes,
                        },
                    )

                    print(f"Inserted {movename} for {character}")

        await db.commit()
