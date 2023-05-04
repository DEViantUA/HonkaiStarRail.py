import aiohttp,urllib.parse, subprocess
from .modal import URLParams,JumpRecord,JumpRecordGacha,ImageGacha
from .calculator import get_result
from .src.data.gacha import gacha_data
from datetime import datetime, timezone

_API = "https://api-os-takumi.mihoyo.com/common/gacha_record/api/getGachaLog"
_EVENT = "dbebc8d9fbb0d4ffa067423482ce505bc5ea"
_LIGHT_CONE = "ceef3b655e094f3f603c57e581c98dad09b3"
_STANDART = "ad9815cdf2308104c377aac42c7f0cdd8d"
_ALLOWED_LANGUAGES = ["chs","cht","de","en","es","fr","id","it","jp","kr","pt","ru","th","vi","tr"]
_ALLOWED_BANNERS = ["1","2","3"]

_LINK_DATA_IMAGE = "https://starrailstation.com/assets/{keys}.webp"


def examination(lang,banner):
    if lang not in _ALLOWED_LANGUAGES:
        raise ValueError(f"Invalid value for 'lang'. Allowed values are {_ALLOWED_LANGUAGES}")
    if str(banner) not in _ALLOWED_BANNERS:
        raise ValueError(f"Invalid value for 'banner'. Allowed values are 1,2,3")


class Jump:
    def __init__(self, link = "", banner = 1, lang = "en",limit = 0,reg = "os") -> None:

        examination(lang,banner)
        self.link = link
        if self.link == "":
            self.get_auto_link(reg=reg)
        self.limit = limit
        self.lang = lang
        self.banner = str(banner)
        data = self.set_parameters()

        if data.authkey == None:
            raise ValueError(f"Check if the link is correct")
            
        if data.lang != self.lang:
            data.lang = self.lang
        
        if self.banner == "1":
            #EVENT
            data.gacha_id = _EVENT
            data.default_gacha_type = 11
        elif self.banner == "2":
            #LIGHT CONE
            data.gacha_id = _LIGHT_CONE
            data.default_gacha_type = 12
        else:
            #STANDART
            data.gacha_id = _STANDART
            data.default_gacha_type = 1
        self.params = {
            "authkey_ver": data.authkey_ver,
            "gacha_id": data.gacha_id,
            "timestamp": int(datetime.now(timezone.utc).astimezone(timezone.utc).replace(tzinfo=timezone.utc).timestamp()),
            "region": data.region,
            "default_gacha_type": data.default_gacha_type ,
            "lang": data.lang,
            "authkey": urllib.parse.unquote(data.authkey),
            "game_biz": data.game_biz,
            "plat_type": "pc",
            "page": 1,
            "size": 20,
            "gacha_type": data.default_gacha_type,
            "end_id": 0
        }


        self.history = []
        self.response = None

    def get_auto_link(self, reg = "os"):
        if reg.lower() == "os":
            cmd = ['powershell', '-Command', 'Invoke-Expression (New-Object Net.WebClient).DownloadString("https://gist.githubusercontent.com/DEViantUA/d5b77400c5d710e4260474afa5011d17/raw/bd8c200f7906fb005d4d11097a8f95e4feb8823f/HonkaiStarRailJump.ps1")'] 
        elif reg.lower() == "cn":
            cmd = ['powershell', '-Command', 'Invoke-Expression (New-Object Net.WebClient).DownloadString("https://gist.githubusercontent.com/DEViantUA/19d224c9c13e6f6b1cc62a12fc0e8a9d/raw/9dcd08b8033d9e60921e216c7219354e863e13b5/HonkaiStarRailJump_CN.ps1")'] 
        else:
            raise ValueError('The reg parameter takes values: os or cn')
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.link = next(filter(None, map(str.strip, reversed(result.stdout.splitlines()))))
        elif result.returncode == 1:
            raise ValueError('Try changing reg to ch or os')
        elif result.returncode == 2:
            raise ValueError(f'Open "More" in Honkai Star Rail - Jumps')
        elif result.returncode == 3:
            raise ValueError(f'The file path is missing, try changing the reg option to os or cn')
        else:
            raise ValueError('Unknown error')
    
    async def get_images(self, itmes_id):
        items = gacha_data.items.get(str(itmes_id), None)
        if items == None:
            raise ValueError('Information not found in the database, try updating the module version.')
        
        
        keys_image_mini = items.get("icon","a30bc8cb7d4bed2a72c52b43949ac07e010f3ba1c5f6fe05c70d7f31feb234f1")
        keys_image_full = items.get("splashIcon","a30bc8cb7d4bed2a72c52b43949ac07e010f3ba1c5f6fe05c70d7f31feb234f1")
        
        return ImageGacha(icon = _LINK_DATA_IMAGE.format(keys = keys_image_mini), full =  _LINK_DATA_IMAGE.format(keys = keys_image_full))



    def set_parameters(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.link).query)
        params = {k: v[0] for k, v in params.items()}

        params_obj = URLParams(**params)

        return params_obj

    async def send_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(_API, params=self.params) as response:
                if response.status == 200:
                    self.response = await response.json()
                    self.history.append(self.response)
                else:
                    print(f"Request error: {response.status}\n\nCheck if the history link is correct.")
                    self.response = None

    async def get_history(self,gacha = False):
        limite = 0
        while True:
            if self.limit != 0:
                self.limit += 1
                if self.limit <= limite:
                    break
            await self.send_request()
            if self.response is not None:   
                data_length = len(self.response.get('data', {}).get('list', []))

                if data_length == 0:
                    break
                self.params['end_id'] = self.response.get('data', {}).get('list', [])[-1].get('id')
                self.params['page'] += 1
            else:
                break

            if gacha:
                yield [JumpRecordGacha(dropped = 0, uid = r["uid"],time= datetime.fromisoformat(r['time']), name=r['name'], type=r['item_type'], rank=r['rank_type'], count=r['count'], id = r["item_id"]) for r in self.response['data']['list']] 
            else:
                yield [JumpRecord(uid = r["uid"],time= datetime.fromisoformat(r['time']), name=r['name'], type=r['item_type'], rank=r['rank_type'], count=r['count'], id = r["item_id"]) for r in self.response['data']['list']] 

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    
    async def get_gacha(self):
        items = []
        async for key in self.get_history(gacha=True):
            items.extend(key)
        return await get_result(items)

