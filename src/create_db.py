import aiosqlite


async def setup_ufd(filepath: str = "./db/ultimateframedata.db") -> None:
    """Sets up the UFD database with the required tables.
    Only really needed for first-time setup.
    """
    async with aiosqlite.connect(filepath) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS moves(
                character TEXT,
                move_name TEXT,
                move_name_smash TEXT,
                frame_startup TEXT,
                frame_active TEXT,
                frame_endlag TEXT,
                frame_onshield TEXT,
                frame_shieldlag TEXT,
                frame_shieldstun TEXT,
                frame_total TEXT,
                autocancels TEXT,
                actionable_before_landing TEXT,
                damage TEXT,
                hitbox_gif TEXT,
                notes TEXT)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS stats(
                character TEXT,
                image TEXT,
                weight TEXT,
                gravity TEXT,
                walk_speed TEXT,
                run_speed TEXT,
                initial_dash TEXT,
                air_speed TEXT,
                total_air_acceleration TEXT,
                sh_fh_shff_fhff_frames TEXT,
                fall_speed_fast_fall_speed TEXT,
                oos1 TEXT,
                oos2 TEXT,
                oos3 TEXT,
                shield_grab TEXT,
                shield_drop TEXT,
                jump_squat TEXT)"""
        )
