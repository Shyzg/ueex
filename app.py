from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
from requests import (
    JSONDecodeError,
    RequestException,
    Session
)
from time import sleep
import json
import os
import sys

class UE:
    def __init__(self) -> None:
        self.session = Session()
        self.faker = Faker()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
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

    def tg(self, queries: str):
        url = 'https://zejlgz.com/api/login/tg'
        tokens = []
        for query in queries:
            data = json.dumps({'init_data':query,'referrer':'gl5mq7'})
            headers = {
                **self.headers,
                'Content-Length': str(len(data))
            }
            try:
                response = self.session.post(url=url, headers=headers, data=data)
                response.raise_for_status()
                data = response.json()
                token = data['data']['token']['token']
                display_name = data['data']['user']['display_name'] or self.faker.name()
                tokens.append((token, display_name))
            except (Exception, JSONDecodeError, RequestException) as e:
                self.print_timestamp(
                    f"{Fore.YELLOW + Style.BRIGHT}[ Failed To Process {query} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}"
                )
                continue
        return tokens

    def assets_user(self, token: str, display_name: str):
        url = 'https://zejlgz.com/api/user/assets'
        data = json.dumps({'token':token})
        headers = {
            **self.headers,
            'Content-Length': str(len(data))
        }
        try:
            response = self.session.post(url=url, headers=headers, data=data)
            response.raise_for_status()
            assets = response.json()
            return self.print_timestamp(
                f"{Fore.CYAN + Style.BRIGHT}[ {display_name} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}[ 💎 {assets['data']['diamond']['amount'] if 'diamond' in assets['data'] else 0} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}[ 🪙 {assets['data']['ue']['amount'] if 'ue' in assets['data'] else 0} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT}[ 💵 {assets['data']['usdt']['amount'] if 'usdt' in assets['data'] else 0} ]{Style.RESET_ALL}"
            )
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Assets: {str(e.response.reason)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Assets: {str(e)} ]{Style.RESET_ALL}")

    def info_scene(self, token: str, display_name: str):
        url = 'https://zejlgz.com/api/scene/info'
        data = json.dumps({'token':token})
        headers = {
            **self.headers,
            'Content-Length': str(len(data))
        }
        try:
            response = self.session.post(url=url, headers=headers, data=data)
            response.raise_for_status()
            scene_info = response.json()
            if scene_info['code'] == 0 or scene_info['data'] is not None:
                for data_entry in scene_info['data']:
                    if data_entry['eggs'] is not None:
                        for eggs in data_entry['eggs']:
                            self.reward_egg_scene(token=token, egg_uid=eggs['uid'], display_name=display_name)
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Info Scene: {str(e.response.reason)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Info Scene: {str(e)} ]{Style.RESET_ALL}")

    def reward_egg_scene(self, token: str, egg_uid: str, display_name: str):
        url = 'https://zejlgz.com/api/scene/egg/reward'
        data = json.dumps({'token':token,'egg_uid':egg_uid})
        headers = {
            **self.headers,
            'Content-Length': str(len(data))
        }
        try:
            response = self.session.post(url=url, headers=headers, data=data)
            response.raise_for_status()
            scene_egg_reward = response.json()
            if scene_egg_reward['code'] == 0 or scene_egg_reward['data'] is not None:
                if scene_egg_reward['data']['a_type'] == 'ue':
                    return self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {display_name} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}[ Reward 🪙 {scene_egg_reward['data']['amount']} ]{Style.RESET_ALL}"
                    )
                elif scene_egg_reward['data']['a_type'] == 'usdt':
                    return self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {display_name} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Reward 💵 {scene_egg_reward['data']['amount']} ]{Style.RESET_ALL}"
                    )
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Reward Egg: {str(e.response.reason)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Reward Egg: {str(e)} ]{Style.RESET_ALL}")

    def main(self):
        while True:
            try:
                queries = [line.strip() for line in open('queries.txt', 'r').readlines()]
                tokens = self.tg(queries=queries)
                for (token, display_name) in tokens:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Home ]{Style.RESET_ALL}")
                    self.assets_user(token=token, display_name=display_name)
                    self.info_scene(token=token, display_name=display_name)

                sleep_timestamp = (datetime.now().astimezone() + timedelta(seconds=20*60)).strftime('%x %X %Z')
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {sleep_timestamp} ]{Style.RESET_ALL}")

                sleep(20*60)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        init(autoreset=True)
        ue = UE()
        ue.main()
    except Exception as e:
        ue.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)