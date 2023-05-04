# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

'''
This method returns the full history of jumps for the 
last 3 months, does not return the results of jumps 
and how much is left before the guarantor.
'''

import asyncio
from honkaistarrail import starrail

'''
To get the link automatically, just don't pass the link parameter.
'''

async def get_jump_history():
    async with starrail.Jump(banner = 1,lang = "en", reg = "os") as hist:
        async for key in hist.get_history():
            for info in key:
                print(f'[{info.type}] Name: {info.name} ({info.rank}*) - {info.time.strftime("%d.%m.%Y %H:%M:%S")}')


asyncio.run(get_jump_history())
