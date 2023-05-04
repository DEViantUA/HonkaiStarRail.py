import asyncio
from honkaistarrail import starrail

'''
This example shows how to get an image using get_images()
'''

async def get_image_history():
    async with starrail.Jump(banner = 3,lang = "en", reg = "os") as hist:
        result = await hist.get_history()
        for info in result.history:
            image = await hist.get_images(info.id))
            print(f"Icon: {image.icon}\nFullL: {image.full}")
            
            
asyncio.run(get_image_history())
