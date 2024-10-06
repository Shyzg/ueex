from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
import asyncio, json, os, sys

class UE:
    def __init__(self) -> None:
        self.faker = Faker()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'zejlgz.com',
            'Origin': 'https://ueex-mining-be9.pages.dev',
            'Pragma': 'no-cache',
            'Referer': 'https://ueex-mining-be9.pages.dev/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': FakeUserAgent().random
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_timestamp(self, message):
        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{message}",
            flush=True
        )

    async def generate_token(self, query: str):
        url = 'https://zejlgz.com/api/login/tg'
        data = json.dumps({'init_data':query,'referrer':'yqw2x9'})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                    response.raise_for_status()
                    generate_token = await response.json()
                    token = generate_token['data']['token']['token']
                    display_name = generate_token['data']['user']['display_name'] or self.faker.name()
                    return (token, display_name)
        except (Exception, ClientResponseError) as e:
            self.print_timestamp(
                f"{Fore.YELLOW + Style.BRIGHT}[ Failed To Process {query} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}"
            )
            return None

    async def generate_tokens(self, queries):
        tasks = [self.generate_token(query) for query in queries]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

    async def assets_user(self, token: str):
        url = 'https://zejlgz.com/api/user/assets'
        data = json.dumps({'token':token})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                    response.raise_for_status()
                    return await response.json()
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Assets: {str(e)} ]{Style.RESET_ALL}")
            return None
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Assets: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def info_scene(self, token: str):
        url = 'https://zejlgz.com/api/scene/info'
        data = json.dumps({'token':token})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                    response.raise_for_status()
                    scene_info = await response.json()
                    if scene_info['code'] == 0 or scene_info['data'] is not None:
                        for data_entry in scene_info['data']:
                            if data_entry['eggs'] is not None:
                                for eggs in data_entry['eggs']:
                                    await self.reward_egg_scene(token=token, egg_uid=eggs['uid'])
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Info Scene: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Info Scene: {str(e)} ]{Style.RESET_ALL}")

    async def reward_egg_scene(self, token: str, egg_uid: str):
        url = 'https://zejlgz.com/api/scene/egg/reward'
        data = json.dumps({'token':token,'egg_uid':egg_uid})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                    response.raise_for_status()
                    reward_egg_scene = await response.json()
                    if reward_egg_scene['code'] == 0 or reward_egg_scene['data'] is not None:
                        if reward_egg_scene['data']['a_type'] == 'ue':
                            return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Reward 🪙 {reward_egg_scene['data']['amount']} ]{Style.RESET_ALL}")
                        elif reward_egg_scene['data']['a_type'] == 'usdt':
                            return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Reward 💵 {reward_egg_scene['data']['amount']} ]{Style.RESET_ALL}")
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Reward Egg Scene: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Reward Egg Scene: {str(e)} ]{Style.RESET_ALL}")

    async def list_invite(self, token: str):
        url = 'https://zejlgz.com/api/invite/list'
        data = json.dumps({'token':token,'start_id':'','size':20})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                    response.raise_for_status()
                    list_invite = await response.json()
                    for list in list_invite['data']:
                        if list['flag'] == 0:
                            await self.reward_invite(token=token, invite_id=list['id'], user_display_name=list['user_display_name'])
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Reward Egg Scene: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Reward Egg Scene: {str(e)} ]{Style.RESET_ALL}")

    async def reward_invite(self, token: str, invite_id: str, user_display_name: str):
        url = 'https://zejlgz.com/api/invite/reward'
        data = json.dumps({'token':token,'invite_id':invite_id})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                    response.raise_for_status()
                    reward_invite = await response.json()
                    if 'data' in reward_invite:
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {reward_invite['data']['diamond']} 💎 From {user_display_name} ]{Style.RESET_ALL}")
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Reward Egg Scene: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Reward Egg Scene: {str(e)} ]{Style.RESET_ALL}")

    async def main(self):
        while True:
            try:
                queries = [line.strip() for line in open('queries.txt', 'r').readlines()]
                tokens = await self.generate_tokens(queries=queries)
                for (token, display_name) in tokens:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Home ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {display_name} ]{Style.RESET_ALL}"
                    )
                    assets_user = await self.assets_user(token=token)
                    if assets_user is not None:
                        self.print_timestamp(
                            f"{Fore.BLUE + Style.BRIGHT}[ 💎 {assets_user['data']['diamond']['amount'] if 'diamond' in assets_user['data'] else 0} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ 🪙 {assets_user['data']['ue']['amount'] if 'ue' in assets_user['data'] else 0} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}[ 💵 {assets_user['data']['usdt']['amount'] if 'usdt' in assets_user['data'] else 0} ]{Style.RESET_ALL}"
                        )
                    await self.info_scene(token=token)
                    await self.list_invite(token=token)

                sleep_timestamp = (datetime.now().astimezone() + timedelta(seconds=20*60)).strftime('%x %X %Z')
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {sleep_timestamp} ]{Style.RESET_ALL}")

                await asyncio.sleep(20*60)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        init(autoreset=True)
        ue = UE()
        asyncio.run(ue.main())
    except Exception as e:
        ue.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)