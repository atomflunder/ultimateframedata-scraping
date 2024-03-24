import requests
import aiosqlite
from bs4 import BeautifulSoup
import src.characters


async def populate_stats(characters: list[str]) -> None:
    async with aiosqlite.connect("./db/ultimateframedata.db") as db:
        for character in characters:
            character_url = src.characters.get_characters_url(character)

            r = requests.get(f"https://ultimateframedata.com/{character_url}.php")

            soup = BeautifulSoup(r.text, "html.parser")

            moves = [x for x in soup.find_all("div", {"class": "movecontainer"})]

            for move in moves:
                movename = move.find("div", {"class": "movename"})

                if movename:
                    movename = movename.text.replace("\n", "").replace("\t", "")

                if movename != "Stats":
                    continue

                oos1 = move.find_all("div", {"class": "oos1"})
                oos2 = move.find_all("div", {"class": "oos2"})
                oos3 = move.find_all("div", {"class": "oos3"})

                oos1 = "\n".join([x.text for x in oos1])
                oos2 = "\n".join([x.text for x in oos2])
                oos3 = "\n".join([x.text for x in oos3])

                other_children = move.findChildren("div", recursive=False)

                stats = {
                    "weight": other_children[1].text,
                    "gravity": other_children[2].text,
                    "walk_speed": other_children[3].text,
                    "run_speed": other_children[4].text,
                    "initial_dash": other_children[5].text,
                    "air_speed": other_children[6].text,
                    "total_air_acceleration": other_children[7].text,
                    "sh_fh_shff_fhff_frames": other_children[8].text,
                    "fall_speed_fast_fall_speed": other_children[9].text,
                    "oos1": oos1,
                    "oos2": oos2,
                    "oos3": oos3,
                    "shield_grab": other_children[13].text,
                    "shield_drop": other_children[14].text,
                    "jump_squat": other_children[15].text,
                    "image": f"https://ultimateframedata.com/characterart/dark/{character_url}.webp",
                }

                await db.execute(
                    """INSERT INTO stats VALUES(
                        :character,
                        :image,
                        :weight,
                        :gravity,
                        :walk_speed,
                        :run_speed,
                        :initial_dash,
                        :air_speed,
                        :total_air_acceleration,
                        :sh_fh_shff_fhff_frames,
                        :fall_speed_fast_fall_speed,
                        :oos1,
                        :oos2,
                        :oos3,
                        :shield_grab,
                        :shield_drop,
                        :jump_squat)""",
                    {
                        "character": character,
                        **stats,
                    },
                )

            print(f"Stats for {character} populated")

        await db.commit()
