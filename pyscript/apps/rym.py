import aiohttp

class RYM:
    def __init__(self):
        self.cred = pyscript.app_config
        self.session = aiohttp.ClientSession()
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.7,he;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://rym-pro.com/',
                'Content-Type': 'application/json',
                'x-app-id': '3a869241-d476-40f6-a923-d789d63db11d',
                'Origin': 'https://rym-pro.com',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'TE': 'trailers',
                }
        self.do_auth()

    async def do_auth(self):
        log.info("Trying to login")
        self.token = None
        async with self.session.post('https://api.city-mind.com/consumer/login', headers=self.headers, json=self.cred) as r:
            self.token = r.json()["token"]
            self.headers["x-access-token"] = self.token
            log.info("Logged in successfully")

    async def do_get_readings(self):
        url = "https://api-ctm.city-mind.com"
        path = "consumption/last-read"

        async with self.session.get(f"{url}/{path}", headers=self.headers) as r:
            return r.json()[0]['read']

    def read_meter(self):
        readings = 0

        try:
            readings = self.do_get_readings()
        except Exception as e:
            log.info(f"Failed getting readings - trying a new token ({e})")
            self.do_auth(cred)
            readings = self.do_get_readings()


        log.info(f"Reading: {readings}")
        state.set(f"sensor.rym", value = float(readings))

rym = RYM()

@time_trigger("period(now() + 0min, 1hour)")
def timer_rym():
    rym.read_meter()

@service
def service_rym(action=None, id=None):
    """yaml
name: Read meter status
description: Read water meter from Read-Your-Meter-Pro.
"""
    rym.read_meter()

