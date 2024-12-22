from concurrent.futures import ThreadPoolExecutor
from netaddr import IPAddress,IPNetwork
from random import choice
import requests
from utility import download_or_read,send_or_write, report

class Varifier:
    def __init__(self, proxy_file: str, judges_file: str, exclude_file = "", output_path = "./temp", verbose=False,threads=100):
        self.version = "2.0.0"
        self.proxy_list = []
        self.judge_list = []
        self.exclude_range = []
        self.checked_proxies = []
        self.output_path = output_path
        self.num_threads = threads
        self.verbose = verbose

        report("Loaded proxitechtor version " + self.version, "MAIN")
        report("Loading exclude list.","MAIN")
        self.load_excludes(exclude_file)
        report("Loading judge list.","MAIN")
        self.load_judges(judges_file)
        report("Loading proxy list.","MAIN")
        self.load_proxies(proxy_file)

    def load_proxies(self,proxy_file: str):
        source_list = []
        source_list = download_or_read(proxy_file)
        if self.verbose:
            report(f"Loaded {len(source_list)} proxy sources.","SYSTEM")
        for source in source_list:
            try:
                url,method = source.split(",",1)
            except Exception as e:
                if self.verbose:
                    report(f"Unexpected source value. Error: {e}","ERROR")
                continue
            loaded_list = []
            loaded_list = download_or_read(url)
            for proxy in loaded_list:
                if self.check_address(proxy):
                    if self.varify_address(proxy):
                        proxy_addr = method + "://" + proxy
                        if not proxy_addr in self.proxy_list:
                            self.proxy_list.append(proxy_addr)
            if self.verbose:
                report(f"Loaded {len(loaded_list)} raw proxies from \"{source}\".","SYSTEM")
        report(f"Loaded {len(self.proxy_list)} raw proxies.","MAIN")

    def load_judges(self,judge_file: str):
        source_list = []
        source_list = download_or_read(judge_file)
        if self.verbose:
            report(f"Loaded {len(source_list)} judge sources.","SYSTEM")
        for source in source_list:
            try:
                response = requests.request("GET",source,timeout=5)
                if "REMOTE_ADDR" in response.text:
                    self.judge_list.append(source)
                else:
                    if self.verbose:
                        report(f"Unexpected response from the judge: \"{source}\".","ERROR")
            except Exception as e:
                report(f"ERROR: Unable to connect \"{source}\".","ERROR")
        report(f"Loaded {len(self.judge_list)} judges.","MAIN")

    def load_excludes(self,exclude_file: str):
        source_list = []
        source_list = download_or_read(exclude_file)
        if self.verbose:
            report(f"Loaded {len(source_list)} exclude sources.","SYSTEM")
        for source in source_list:
            if source.startswith("http"):
                loaded_list = []
                loaded_list = download_or_read(source)
                self.exclude_range += [range for range in loaded_list if self.check_address(range)]
            elif self.check_address(source):
                self.exclude_range.append(source)
            else:
                if self.verbose:
                    report(f"Unexpected data for exclude range: \"{source}\"","ERROR")
        report(f"Loaded {len(self.exclude_range)} forbiden subnets.","MAIN")

    def sort_check(self,proxy):
        pass

    def three_ray_chack(self,proxy):
        pass

    def basic_check(self,proxy):
        if self.varify_address(proxy):
            try:
                judge = choice(self.judge_list)
                response = requests.request("GET",judge,proxies={"http":proxy,"https":proxy},timeout=10)
                if response.status_code == 200:
                    if "REMOTE_ADDR" in response.text:
                        if self.verbose:
                            report(f"\"{proxy}\": SUCCSSES.","SYSTEM")
                        self.checked_proxies.append(proxy)
                    else:
                        if self.verbose:
                            report(f"\"{proxy}\": FAILED. Response code: {response.status_code}","SYSTEM")
            except requests.Timeout:
                if self.verbose:
                    report(f"\"{proxy}\": FAILED. Timeout.","SYSTEM")
            except requests.ConnectionError as e:
                if ("time out" in str(e)):
                    if self.verbose:
                        report(f"\"{proxy}\": FAILED. Timeout.","SYSTEM")
                else:
                    if self.verbose:
                        report(f"\"{proxy}\": FAILED. Connection error: {e}","SYSTEM")
            except Exception as e:
                if self.verbose:
                    report(f"\"{proxy}\": FAILED. Error: {e}","SYSTEM")

    def check_proxies(self):
        report("Starting to check proxies.","MAIN")
        chunk_size = 12500
        chunks = []
        for i in range(0, len(self.proxy_list), chunk_size):
            chunks.append(self.proxy_list[i:i + chunk_size])
        for chunk in chunks:
            last_size = len(self.checked_proxies)
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                executor.map(self.basic_check,chunk)
            report(f"{len(self.checked_proxies)-last_size} proxies checked seccessfuly.","MAIN")
        report(f"At all {len(self.checked_proxies)} proxies were checked seccessfuly.","MAIN")
        send_or_write(self.output_path,self.checked_proxies)
    
    def check_address(self,address: str):
        allowed_symbols = "sockhtp:/1234567890."
        if len(address) > 8 and len(address) < 30:
            if not any(symbol not in allowed_symbols for symbol in address):
                return True
        if self.verbose:
            report(f"Unexpected symbols in proxy address: \"{address}\"","ERROR")
        return False

    def varify_address(self, address: str):
        if "/" in address:
            addr = address.split(":")[1][2:]
        else:
            addr = address.split(":")[0]
            for subnet in self.exclude_range:
                if IPAddress(addr) in IPNetwork(subnet):
                    if self.verbose:
                        report(f"Proxy \"{addr}\" in forbiden subnet: \"{subnet}\"","ERROR")
                    return False
        return True
