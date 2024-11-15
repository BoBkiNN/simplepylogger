## Simple python logger module for copy-paste

### Usage:
- Copy `logger.py` file to your project
- Import it using `from logger import Logger`
- Instantiate it using `logger = Logger()`
- Use logging functions on instance

### Dependencies:
- `colorama` to enable colors support on windows
- `rich` to display colored text
- `pytz` for timezone settings

### Supported features:
- Change datetime format
- Change datetime timzone
- Write in file, splitting by days and file size
- Enable/Disable colored output in console
- Display exception tracebacks

### Example:
```py
l = Logger(debug=True) # you can enable debug and set other params using constructor
l.debug("Created logger") # debug message will appear only if debug settings is True
l.info("Hello world!") # info message
l.warn("Warn") # warning message
l.error("Error!") # error message
try:
    foo()
except Exception as e:
    l.error("Foo", e) # print exception traceback on error
```