import asyncio
import src.create_db
import src.populate_stats
import src.characters
import src.populate_moves


async def main():
    character_list = src.characters.get_all_characters()

    await src.create_db.setup_ufd()
    await src.populate_stats.populate_stats(character_list)
    await src.populate_moves.populate_moves(character_list)


if __name__ == "__main__":
    asyncio.run(main())
