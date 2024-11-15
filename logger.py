"""Logger module
   ~~~~~~~~~~~~~
   Owner: @bobkinn_

   Copyright 2024 BoBkiNN
   
   Permission is hereby granted to use, modify, and distribute this file, with or without modification, provided 
   that the following conditions are met:
   
   1. Redistributions of this file or substantial portions of it must retain the above copyright notice, this list of conditions, and the following acknowledgment:
    
      "Original author: BoBkiNN."

   2. This file or any substantial portion of it may not be used to misrepresent or detract from the original author's contribution.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT SHALL THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
   DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import traceback
from datetime import datetime
from enum import Enum
from typing import Union, Any

import colorama
import pytz
from rich import print as rprint


class LogLevel(str, Enum):
    WARN = "WARN"
    ERROR = "ERROR"
    INFO = "INFO"
    DEBUG = "DEBUG"

LEVEL_COLOR = \
{
    "WARN": "yellow",
    "ERROR": "red",
    "INFO": "green",
    "DEBUG": "magenta"
}

class LogEvent:
    def __init__(self, level: LogLevel, text: str, exception: Exception | None) -> None:
        self.level = level
        self.text = text
        self.exception = exception
    
    @staticmethod
    def create(level: LogLevel, *objs):
        exc: Exception | None = None
        ls: list[str] = []
        for v in objs:
            if level is not LogLevel.INFO and isinstance(v, Exception) and exc is None:
                exc = v
            else:
                ls.append(str(v))
        return LogEvent(level, " ".join(ls), exc)

class Logger:
    def __init__(
            self,
            console: bool = True,
            file: bool = False,
            colored: bool = True,
            debug: bool = False,
            timezone: pytz.BaseTzInfo = pytz.timezone("UTC"),
            date_format: str = '%d.%m.%Y %H:%M:%S',
            directory: str = f"{os.getcwd()}{os.sep}logs",
    ):
        self.do_console = console
        self.do_file = file
        self.enable_debug = debug
        self.is_colored = colored
        self.tz = timezone
        self.df = date_format
        self.dir = directory
 
        if os.name == "nt" and colored:
            colorama.init(autoreset=True)
 
    def _format_time(self) -> str:
        dt = datetime.now(self.tz)
        return dt.strftime(self.df)
    
    def _format_exc(self, ex: Union[Exception, tuple[type[BaseException], BaseException, Any]]):
        if isinstance(ex, tuple) and len(ex) == 3:
            te = traceback.TracebackException.from_exception(ex[1])
        else:
            te = traceback.TracebackException.from_exception(ex)
        return ''.join(te.format()).strip("\n")
 
    def _log(self, event: LogEvent):
        if event.level == LogLevel.DEBUG and not self.enable_debug:
            return
        nowstr = self._format_time()
        lval = event.level.name
        cval = LEVEL_COLOR[lval]
        exc_text = None
        if event.exception:
            exc_text = "\n"+self._format_exc(event.exception)
        final_text = f"[{nowstr} {lval}]: {event.text}"
        final_text_nocolored = final_text
        if self.do_console:
            if self.is_colored:
                final_text = fr"[bold {cval}]\[{nowstr} {lval}]: {event.text}"
                if exc_text:
                    final_text += exc_text
                final_text += "[/]"
            rprint(final_text)
        if exc_text:
            final_text_nocolored += exc_text
        if self.do_file:
            self._write_to_file(final_text_nocolored)
 
    def _write_to_file(self, text: str):
        path_latest = f"{self.dir}{os.sep}latest.log"
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
 
        if not os.path.exists(path_latest):
            with open(path_latest, "w") as fl:
                fl.close()
        else:
            latest_mod = os.path.getmtime(path_latest)
            latest_mod_date = datetime.fromtimestamp(
                latest_mod, tz=self.tz).date()
            now_date = datetime.now(self.tz).date()
 
            latest_size = os.stat(path_latest).st_size // 1024 // 1024
            if latest_mod_date.day != now_date.day or latest_size > 10:
                file_number = 1
                while True:
                    filename = f"{latest_mod_date.day}_{latest_mod_date.month}_{latest_mod_date.year}-{file_number}.log"
                    try:
                        os.rename(path_latest, f"{self.dir}{os.sep}{filename}")
                    except FileExistsError:
                        file_number += 1
                    else:
                        break
 
        if not os.path.exists(path_latest):
            with open(path_latest, "w") as fl:
                fl.close()
 
        with open(path_latest, "a", encoding="utf-8") as fl:
            print(text, file=fl)
 
    def info(self, *objs):
        return self._log(LogEvent.create(LogLevel.INFO, *objs))
 
    def warn(self, *objs):
        return self._log(LogEvent.create(LogLevel.WARN, *objs))
 
    def error(self, *objs):
        return self._log(LogEvent.create(LogLevel.ERROR, *objs))
    
    def debug(self, *objs):
        return self._log(LogEvent.create(LogLevel.DEBUG, *objs))



if __name__ == "__main__":
    def bar():
        raise ValueError("meow")
    def foo():
        bar()
    l = Logger(debug=True)
    l.debug("Created logger")
    l.info("Hello world!")
    l.warn("Warn")
    l.error("Error!")
    try:
        foo()
    except Exception as e:
        l.error("Foo", e)
        l.warn(e)
        l.info(e)
