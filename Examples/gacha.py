# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import asyncio
from starrail import starrail

async def get_jump_gacha():
    link = ""
    async with starrail.Jump(link,1,"en") as hist:
        result = await hist.get_gacha()
        print(f"Total jump: {result.total}")

        print(f"Total {result.total_type_one[0].name}: {result.total_type_one[0].count}")
        print(f"Total {result.total_type_one[1].name}: {result.total_type_one[1].count}")

        print(f"Total rank '4': {result.total_rank_four}")
        print(f"Total rank'5': {result.total_rank_five}")
        print(f"Next '4' reset in: {result.next_four_garant} jump")
        print(f"Next '5' reset in: {result.next_five_garant} jump")
        for info in result.history:
            print()
            print(f'[{info.type}] Name: {info.name} ({info.rank}*) - {info.dropped}')
            
asyncio.run(get_jump_gacha())
