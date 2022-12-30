from re import findall as re_findall
from threading import Thread, Event
from time import time
from math import ceil
from html import escape
from psutil import virtual_memory, cpu_percent, disk_usage

from bot import download_dict, download_dict_lock, botStartTime, DOWNLOAD_DIR, user_data, config_dict
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

COUNT = 0
PAGE_NO = 1
PAGES = 0

class MirrorStatus:
    STATUS_CLONING = "Clone"
    STATUS_CHECKING = "CheckUp"

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = Event()
        thread = Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time() + self.interval
        while not self.stopEvent.wait(nextTime - time()):
            self.action()
            nextTime = time() + self.interval

    def cancel(self):
        self.stopEvent.set()

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def getDownloadByGid(gid):
    with download_dict_lock:
        for dl in list(download_dict.values()):
            if dl.gid() == gid:
                return dl
    return None

def getAllDownload(req_status: str):
    with download_dict_lock:
        for dl in list(download_dict.values()):
            status = dl.status()
            if req_status in ['all', status]:
                return dl
    return None

def get_progress_bar_string(status):
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    p_str = '■' * cFull
    p_str += '□' * (12 - cFull)
    return f"[{p_str}]"

def get_readable_message():
    with download_dict_lock:
        msg = ""
        if STATUS_LIMIT := config_dict['STATUS_LIMIT']:
            tasks = len(download_dict)
            globals()['PAGES'] = ceil(tasks/STATUS_LIMIT)
            if PAGE_NO > PAGES and PAGES != 0:
                globals()['COUNT'] -= STATUS_LIMIT
                globals()['PAGE_NO'] -= 1
        for index, download in enumerate(list(download_dict.values())[COUNT:], start=1):
            msg += f"<b><a href='{download.message.link}'>{download.status()}</a>: </b>"
            msg += f"<code>{escape(str(download.name()))}</code>"
            msg += f"\n{get_progress_bar_string(download)} {download.progress()}"
            msg += f"\n<b>Processed:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
            msg += f"\n<b>Speed:</b> {download.speed()} | <b>ETA:</b> {download.eta()}"
            msg += f"\n<code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            msg += "\n\n"
            if index == STATUS_LIMIT:
                break
        if len(msg) == 0:
            return None, None
            
        dl_speed = 0
        up_speed = 0
        
        bmsg = f"<b>CPU:</b> {cpu_percent()}% | <b>FREE:</b> {get_readable_file_size(disk_usage(DOWNLOAD_DIR).free)}"
        bmsg += f"\n<b>RAM:</b> {virtual_memory().percent}% | <b>UPTIME:</b> {get_readable_time(time() - botStartTime)}"
        bmsg += f"\n<b>DL:</b> {get_readable_file_size(dl_speed)}/s | <b>UL:</b> {get_readable_file_size(up_speed)}/s"
        if STATUS_LIMIT and tasks > STATUS_LIMIT:
            msg += f"<b>Page:</b> {PAGE_NO}/{PAGES} | <b>Tasks:</b> {tasks}\n"
            buttons = ButtonMaker()
            buttons.sbutton("<<", "status pre")
            buttons.sbutton(">>", "status nex")
            buttons.sbutton("♻️", "status ref")
            button = buttons.build_menu(3)
            return msg + bmsg, button
        return msg + bmsg, None

def turn(data):
    STATUS_LIMIT = config_dict['STATUS_LIMIT']
    try:
        global COUNT, PAGE_NO
        with download_dict_lock:
            if data[1] == "nex":
                if PAGE_NO == PAGES:
                    COUNT = 0
                    PAGE_NO = 1
                else:
                    COUNT += STATUS_LIMIT
                    PAGE_NO += 1
            elif data[1] == "pre":
                if PAGE_NO == 1:
                    COUNT = STATUS_LIMIT * (PAGES - 1)
                    PAGE_NO = PAGES
                else:
                    COUNT -= STATUS_LIMIT
                    PAGE_NO -= 1
        return True
    except:
        return False

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def is_url(url: str):
    url = re_findall(URL_REGEX, url)
    return bool(url)

def is_gdrive_link(url: str):
    return "drive.google.com" in url

def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper

def update_user_ldata(id_, key, value):
    if id_ in user_data:
        user_data[id_][key] = value
    else:
        user_data[id_] = {key: value}
