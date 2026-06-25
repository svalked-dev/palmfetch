#!/usr/bin/env python3
import os
import platform
from datetime import datetime
import psutil

class SystemFetcher:
    def __init__(self):
        self.ascii_art = self._load_ascii()
    
    def _load_ascii(self):
        try:
            with open("ascii.txt", 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""
    
    def get_info(self):
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            days = uptime.days
            hours = uptime.seconds // 3600
        except:
            days, hours = 0, 0
        
        return {
            'user': os.environ.get('USER', 'user'),
            'host': platform.node(),
            'os': f"{platform.system()} {platform.release()}",
            'uptime': f"{days}d {hours}h" if days else f"{hours}h",
            'cpu': platform.processor() or "Unknown",
            'memory': self._get_memory_info(),
            'shell': os.environ.get('SHELL', '/bin/bash').split('/')[-1],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    
    def _get_memory_info(self):
        try:
            mem = psutil.virtual_memory()
            return f"{mem.total // (1024**2)}MB ({mem.available // (1024**2)}MB free)"
        except:
            return "N/A"
    
    def show(self):
        info = self.get_info()
        print("\033c", end="")
        
        if self.ascii_art:
            print(self.ascii_art)
            print()
        
        print(f"  {info['user']}@{info['host']}")
        print("  " + "="*40)
        print(f"  OS:      {info['os']}")
        print(f"  Uptime:  {info['uptime']}")
        print(f"  CPU:     {info['cpu']}")
        print(f"  Memory:  {info['memory']}")
        print(f"  Shell:   {info['shell']}")
        print(f"  Date:    {info['date']}")
        print()

def main():
    fetcher = SystemFetcher()
    fetcher.show()

if __name__ == "__main__":
    main()
