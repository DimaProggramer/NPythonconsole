import os
import socket
import requests
import platform
import random
import time
import sys
import select
import zipfile
from shutil import rmtree
from pathlib import Path
from configforn import *

def print_colored(text, color):
    print(f"{color}{text}{RESET}")

def set_prompt():
    current_directory = os.getcwd()
    if show_path:
        current_directory = current_directory.replace("/storage/emulated/0/", ".../")
        current_directory = current_directory.replace("\\", "/")
        return f"{current_directory} n:>"
    else:
        return "n:>"

def create_directories():
    if os.name == 'nt':
        dirs_to_create = ["C:\\conpyt", "C:\\conpyt\\home", "C:\\conpyt\\src"]
    else:
        dirs_to_create = ["/storage/emulated/0/conpyt", "/storage/emulated/0/conpyt/home", "/storage/emulated/0/conpyt/src"]
    
    for directory in dirs_to_create:
        if not Path(directory).exists():
            try:
                os.makedirs(directory)
                print(f"Directory {directory} created")
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")

create_directories()

def ensure_in_conpyt():
    allowed_dir = Path("/storage/emulated/0/conpyt").resolve()
    current_dir = Path.cwd().resolve()
    if not str(current_dir).startswith(str(allowed_dir)):
        os.chdir(allowed_dir)
        print_colored("Access denied. Returned to /storage/emulated/0/conpyt", RED)

def search_github(query):
    url = f"https://api.github.com/search/repositories?q={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["total_count"] == 0:
                print_colored("No results found.", YELLOW)
                return
            for item in data["items"][:5]:
                repo_name = item["name"]
                repo_url = item["html_url"]
                readme_url = f"{repo_url}/blob/master/README.md"
                print_colored(f"{repo_name} - {repo_url}, README: {readme_url}", WHITE)
        else:
            print_colored(f"Error: {response.status_code}", RED)
    except Exception as e:
        print_colored(str(e), RED)

def search_pypi(query):
    url = f"https://pypi.org/pypi/{query}/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            info = data.get("info", {})
            name = info.get("name", "N/A")
            summary = info.get("summary", "N/A")
            package_url = info.get("package_url", "N/A")
            print_colored(f"Package: {name}\nSummary: {summary}\nURL: {package_url}", WHITE)
        else:
            print_colored("Package not found.", YELLOW)
    except Exception as e:
        print_colored(str(e), RED)

def search(args):
    if len(args) < 3:
        print_colored("Usage: search <git/pypi> <query>", RED)
        return
    
    platform = args[1]
    query = " ".join(args[2:])
    if platform == "git":
        search_github(query)
    elif platform == "pypi":
        search_pypi(query)
    else:
        print_colored("Unknown platform. Use 'google', 'github', or 'pypi'.", RED)

def change_directory(args):
    try:
        target_dir = args[1]
        os.chdir(target_dir)
        print_colored(f"Directory changed to {os.getcwd()}", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def make_directory(args):
    try:
        target_dir = args[1]
        Path(target_dir).mkdir()
        print_colored(f"Directory {target_dir} created", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def remove_file(args):
    try:
        target_file = args[1]
        Path(target_file).unlink()
        print_colored(f"File {target_file} removed", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def list_files(args):
    try:
        files = Path.cwd().iterdir()
        for file in files:
            if file.is_dir():
                print_colored(file.name, PURPLE)
            else:
                print_colored(file.name, GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def remove_directory(args):
    try:
        target_dir = args[1]
        rmtree(target_dir)
        print_colored(f"Directory {target_dir} removed", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def rename_file(args):
    try:
        old_name = args[1]
        new_name = args[2]
        Path(old_name).rename(new_name)
        print_colored(f"Renamed {old_name} to {new_name}", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def clear_screen(args):
    try:
        os.system("cls" if platform.system() == "Windows" else "clear")
    except Exception as e:
        print_colored(str(e), RED)

def show_ip(args):
    try:
        ip = socket.gethostbyname(socket.gethostname())
        print_colored(ip, YELLOW)
    except Exception as e:
        print_colored(str(e), RED)

def show_time(args):
    try:
        current_time = time.ctime()
        print_colored(current_time, MAGENTA)
    except Exception as e:
        print_colored(str(e), RED)

def make_request(args):
    try:
        url = args[1]
        response = requests.get(url)
        print_colored(response.text, WHITE)
    except Exception as e:
        print_colored(str(e), RED)

def matrix(args):
    try:
        print_colored("Entering 'Matrix' mode. Press Ctrl+C or type 'leave' to exit.", GREEN)
        time.sleep(1)
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                user_input = sys.stdin.read(1)
                if user_input.lower().strip() == "leave":
                    break
            line = ''.join(random.choices("01", k=80))
            print_colored(line, GREEN)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print_colored("Exiting 'Matrix' mode.", GREEN)

def show_help(args):
    help_text = (
        "Command list:\n"
        "exit - exit\n"
        "cd <dir> - change directory\n"
        "mkdir <dir> - create directory\n"
        "rm <file> - remove file\n"
        "ls - list files\n"
        "rmdir <dir> - remove directory\n"
        "info - developer information\n"
        "pwd - show current directory\n"
        "matrix - matrix (CTRL+C to exit)\n"
        "rn <old> <new> - rename\n"
        "ipconfig - show IP\n"
        "time - current time\n"
        "req <url> - make GET request\n"
        "system - system information\n"
        "dpi <url> - (download package from internet) download package\n"
        "search <git/pypi> <query> - perform search\n"
        "show <file> - show file content\n"
        "cls or clear - clear terminal\n"
        "zip <file> - zip file\n"
        "unzip <file> - unzip file\n"
        "meow - meow\n"
    )
    print_colored(help_text, WHITE)

def show_system_info(args):
    processor_info = platform.processor() or "Platform does not provide access to the processor"
    print_colored(logo, colorc)
    print_colored(f"OS: {platform.system()} {platform.release()} ({platform.version()})", MAGENTA)
    print_colored(f"Hostname: {platform.node()}", MAGENTA)
    print_colored(f"Processor: {processor_info}", MAGENTA)
    print_colored(f"Python Version: {platform.python_version()}", MAGENTA)

def download_package(args):
    try:
        url = args[1]
        response = requests.get(url)
        filename = url.split("/")[-1]
        with open(filename, "wb") as f:
            f.write(response.content)
        print_colored(f"Package downloaded from {url}", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def show_file(args):
    if len(args) < 2:
        print_colored("Usage: show <filename>", RED)
        return
    filename = args[1]
    try:
        with open(filename, "r") as f:
            content = f.read()
            print_colored(content, WHITE)
    except Exception as e:
        print_colored(str(e), RED)

def git_clone(args):
    try:
        url = args[1]
        if not url.startswith("https://github.com"):
            print_colored("Only GitHub repositories are supported.", RED)
            return
        repo_name = url.split("/")[-1]
        zip_url = f"{url}/archive/master.zip"
        response = requests.get(zip_url)
        filename = f"{repo_name}.zip"
        with open(filename, "wb") as f:
            f.write(response.content)
        print_colored(f"Repository cloned from {url} and saved as {filename}", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def zip_file(args):
    try:
        file_name = args[1]
        zip_file_name = f'{file_name}.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zipf:
            zipf.write(file_name)
        print_colored(f"{file_name} zipped successfully as {zip_file_name}.", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def touch(args):
    try:
        filename = args[1]
        Path(filename).touch()
        print_colored(f"File {filename} created", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def movedir(args):
    try:
        source = args[1]
        destination = args[2]
        Path(source).rename(destination)
        print_colored(f"Directory {source} moved to {destination}", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def unzip_file(args):
    try:
        file_name = args[1]
        with zipfile.ZipFile(f'{file_name}', 'r') as zipf:
            file_count = len(zipf.filelist)
            for i, file in enumerate(zipf.filelist):
                print_colored(f"Extracting {i+1}/{file_count} files: {file.filename}", CYAN)
                zipf.extract(file)
        print_colored(f"{file_name} unzipped successfully.", GREEN)
    except Exception as e:
        print_colored(str(e), RED)

def pwd(args):
    try:
        current_dir = Path.cwd()
        print_colored(str(current_dir), CYAN)
    except Exception as e:
        print_colored(str(e), RED)

def info(args):
    print("Console", end=" ")
    time.sleep(0.7)
    print_colored("N:>", GREEN)
    print("(or simply N)")
    time.sleep(0.7)
    print_colored("Developed by DimaProggramer", BLUE)
    time.sleep(0.7)
    print_colored("Social networks:", BLUE)
    time.sleep(0.1)
    print_colored("tg @hellobiden", CYAN)
    time.sleep(0.1)
    print_colored("github: github.com/DimaProggramer", WHITE)
    print("For questions, contact", end=" ")
    time.sleep(0.1)
    print_colored("Telegram: @hellobiden", BLUE)

def meow(args):
    print_colored(cat, PINK)

COMMANDS = {
    "cd": change_directory,
    "mkdir": make_directory,
    "rm": remove_file,
    "ls": list_files,
    "rmdir": remove_directory,
    "zip": zip_file,
    "unzip": unzip_file,
    "rn": rename_file,
    "clear": clear_screen,
    "cls": clear_screen,
    "ipconfig": show_ip,
    "time": show_time,
    "req": make_request,
    "help": show_help,
    "system": show_system_info,
    "git": git_clone,
    "dpi": download_package,
    "search": search,
    "show": show_file,
    "touch": touch,
    "pwd": pwd,
    "meow": meow,
    "matrix": matrix,
    "info": info,
}
def console():
    if os.name == 'nt':
        os.chdir(r"C:\conpyt")
    else:
        os.chdir("/storage/emulated/0/")

    while True:
        command = input(f"{GREEN}{set_prompt()} {RESET}")
        if command == "exit":
            break

        args = command.split(" ")
        cmd = args[0]

        if cmd in COMMANDS:
            COMMANDS[cmd](args)
        else:
            print_colored(f"unknown command {command}", RED)

        ensure_in_conpyt()

if __name__ == "__main__":
    print_colored("Welcome!", MAGENTA)
    console()
