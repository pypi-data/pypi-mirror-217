'''
    Copy right 2023.
'''

import sys
import argparse
import os
import platform
from urllib.parse import urlencode
from . import http
import zipfile
import tempfile
import shutil
from tqdm import tqdm
import json
import re
import time
from threading import Thread

verbose = False


def get_python_link_name(pydll_path, os_name):
    if os_name == "linux":
        for so in os.listdir(pydll_path):
            if so.startswith("libpython") and not so.endswith(".so") and so.find(".so") != -1:
                basename = os.path.basename(so[3:so.find(".so")])
                full_path = os.path.join(pydll_path, so)
                return basename, full_path
    return None, None

def format_size(size):

    units = ["Byte", "KB", "MB", "GB", "PB"]
    for i, unit in enumerate(units):
        ref = 1024 ** (i + 1)
        if size < ref:
            div = 1024 ** i
            if i == 0:
                return f"{size} {unit}"
            else:
                return f"{size / div:.2f} {unit}"
    return f"{size} Bytes"

class ChangeCWD:
    def __init__(self, dir):
        self.dir = os.path.abspath(dir)
        self.old = os.path.abspath(os.getcwd())
    
    def __enter__(self):
        os.chdir(self.dir)
        if verbose:
            print(f"Enter {self.dir}")

    def __exit__(self, *args, **kwargs):
        os.chdir(self.old)
        if verbose:
            print(f"Leave {self.dir}, Enter {self.old}")


class Cmd:
    def __init__(self, actions):
        self.parser    = argparse.ArgumentParser()
        self.subparser = self.parser.add_subparsers(dest="cmd")
        self.actions   = actions

    def add_cmd(self, name : str, help : str = None)->argparse._ActionsContainer:
        return self.subparser.add_parser(name, help=help)

    def help(self):
        self.parser.print_help()

    def hello(self):
        print(
            "You can use 'wemp --help' to show the more message."
        )

    def run(self, args, remargs):
        args = self.parser.parse_args(args)
        if args.cmd is None:
            self.hello()
            return False

        return self.actions.private_run_cmd(args, remargs)


class Config:
    def __init__(self):
        self.SERVER      = "https://zifuture.com"
        self.CACHE_ROOT  = os.path.expanduser('~/.cache/wemp')
        self.CACHE_FILE  = os.path.join(self.CACHE_ROOT, "config.json")
        self.OS_NAME     = platform.system().lower()
        self.PY_VERSION  = ".".join(sys.version.split(".")[:2])
        self.EMP_ROOT   = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
        self.CWD         = os.path.abspath(os.path.curdir)
        self.PYLIB_DIR   = os.path.join(sys.exec_prefix, "lib")
        self.PYLIB_NAME, self.PYLIB_PATH = get_python_link_name(self.PYLIB_DIR, self.OS_NAME)

        self.config       = {}
        if not os.path.exists(self.CACHE_FILE):
            os.makedirs(self.CACHE_ROOT, exist_ok=True)
        else:
            try:
                self.config = json.load(open(self.CACHE_FILE))
                if not isinstance(self.config, dict):
                    self.config = {}
                else:
                    self.SERVER = self.config.get("Server", self.SERVER)
            except Exception as e:
                print(f"Failed to load config file: {self.CACHE_FILE}")

        user_name = self.config.get("UserName", None)
        if user_name is None:
            while True:
                user_name = input(f"Please input your UserName: ")
                if not user_name.encode("utf-8").isalnum():
                    print(f"An invalid username is entered. Only [a-zA-Z0-9] can be passed.")
                else:
                    break

            self.config["UserName"] = user_name
            json.dump(self.config, open(self.CACHE_FILE, "w"))

        os.environ["WEMP_SERVER"] = self.SERVER

    def get_cfg(self, name):
        return self.config.get(name, None)
    
    def set_cfg(self, name, value):
        self.config[name] = value
        json.dump(self.config, open(self.CACHE_FILE, "w"))

    def __repr__(self):
        sb  = ["Config:"]
        dic = self.get_dict()
        for key in dic:
            val = dic[key]
            sb.append(f"   {key} = {val}")
        return "\n".join(sb)


def pid_is_live(pid):
    try:
        os.kill(pid, 0)
        return True
    except:
        return False

class Actions:
    def __init__(self, cfg):
        self.cfg : Config = cfg

    def private_run_cmd(self, args, remargs):
        
        cmd = args.cmd
        if not hasattr(self, cmd):
            return False

        del args.__dict__["cmd"]
        self.remargs = remargs
        return getattr(self, cmd)(args)

    def watch(self, args : argparse.Namespace):
        
        file = args.file
        pid  = args.pid
        wait_file = args.wait_file
        noprint = args.noprint

        if args.token is None:
            token = self.cfg.get_cfg("UserName")
        else:
            token = args.token

        if pid is not None:
            if not pid_is_live(pid):
                print(f"This pid[{pid}] is not live")
                return False

        if wait_file:
            i = 0
            while not os.path.isfile(file):
                i += 1

                if i == 1:
                    print(f"Wait file: {file}")

                time.sleep(1)
            
            print(f"Found watch file: {file}")
        
        if not os.path.isfile(file):
            print(f"Is not a file: {file}")
            return False
        
        file_size = os.path.getsize(file)
        print(f"Start watching for: {file}, [{file_size} bytes]")
        print(f"You can use [{token}] to view this.")
        system_run = True

        def cycle_heart(token, pid):
            nonlocal system_run
            heart_url = f"{self.cfg.SERVER}/api/public/watcher/heart"
            while system_run:
                if pid is not None:
                    if not pid_is_live(pid):
                        http.update(update_url, token, f"Pid is shutdown\n\nlast_message is: \n{last_message}")
                        break

                http.heart(heart_url, token)
                time.sleep(5)

            system_run = False

        heart_thread = Thread(target=cycle_heart, args=(token, pid))
        heart_thread.start()

        update_url = f"{self.cfg.SERVER}/api/public/watcher/update"
        last_message = None
        with open(file, "r") as f:

            if file_size > 2048:
                f.seek(file_size - 2048, os.SEEK_SET)

            while system_run:
                last_line = None
                while True:
                    line = f.readline()
                    if line:
                        last_line = line
                    else:
                        break
                
                if last_line:
                    last_line = last_line.strip().replace("\n", "").replace("\r", "")
                    if last_line:
                        if not noprint:
                            print(f"Send: {last_line}")
                            
                        last_message = last_line
                        http.update(update_url, token, last_line)

                time.sleep(1)

        heart_thread.join()
        return True
        
class Application:
    def __init__(self):
        self.cfg     = Config()
        self.actions = Actions(self.cfg)

    def run_with_command(self, args=None)->bool:
        
        if args is not None and isinstance(args, str):
            args = args.split(" ")
        elif args is None:
            args = sys.argv[1:]
        
        remargs = []
        if len(args) > 1 and args[0] == "run":
            run_name = args[1]
            remargs  = args[2:]
            args = ["run", run_name]

        cmd = Cmd(self.actions)
        c = cmd.add_cmd("watch", "Get data from server")
        c.add_argument("file", type=str, help="repo name")
        c.add_argument("--token", type=str, help="token")
        c.add_argument("--pid", type=int, help="watch program")
        c.add_argument("--wait-file", action="store_true", help="wait file")
        c.add_argument("--noprint", action="store_true", help="wait file")

        c = cmd.add_cmd("config", "Config")
        c.add_argument("name", type=str, help="key")
        c.add_argument("value", type=str, help="value")
        return cmd.run(args, remargs)
    
watch_thread = None

def watch(file, token):

    cfg     = Config()
    actions = Actions(cfg)

    global watch_thread
    def watch_fn(token):
        actions.watch(argparse.Namespace(file=file, token=token, pid=None, wait_file=True, noprint=True))

    watch_thread = Thread(target=watch_fn, args=(token,), daemon=True).start()

def stop_watch():

    global watch_thread
    if watch_thread is not None:
        watch_thread.join()
    
    watch_thread = None