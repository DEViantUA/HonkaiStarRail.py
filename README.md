<p align="center">
  <img src="https://raw.githubusercontent.com/DEViantUA/HonkaiStarRail.py/main/Readme/HSR-BANNER.png" />
</p>

# Asynchronous module for working with API Honkai: Star Rail

At the moment it only supports counting guarantors and getting a jumps 

### Installation: 
```
pip install honkaistarrail
```
PyPi: [OPEN](https://pypi.org/project/honkaistarrail/)

You can also see other usage examples here: [OPEN](https://github.com/DEViantUA/starrail.py/tree/main/Examples)

Instructions for getting a link to the history of jumps: [OPEN](https://github.com/DEViantUA/starrail.py/blob/main/Instruction.md)

### ID Banned:
``1`` - Event Banner
``2`` - Light Cone
``3`` - Standart Banner


### Launc:

```py
# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

'''
This method returns the full history of jumps for the 
last 3 months, does not return the results of jumps 
and how much is left before the guarantor.
'''

import asyncio
from honkaistarrail import starrail

async def get_jump_history():
    link = ""
    async with starrail.Jump(link,3,"en") as hist:
        async for key in hist.get_history():
            for info in key:
                print(f'[{info.type}] Name: {info.name} ({info.rank}*) - {info.time.strftime("%d.%m.%Y %H:%M:%S")}')


asyncio.run(get_jump_history())
```


#In developing:

1. Automatic receipt of a link to the journal.
2. Return of images in jumps.
3. Automatic code redemption.
4. Automatic collection of daily marks on HoYoLab.
