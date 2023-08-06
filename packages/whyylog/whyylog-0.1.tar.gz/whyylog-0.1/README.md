# ylog

This is an library to print color-coded log messages to the terminal. It prints in the following format.

`TIME [LOG TYPE] (file names) > (path of the call|line no): Message.`

## Log Levels

Print or Save to a log file.
| Log Level | Log Type      | Print Color | Background Color |
| ---------:| ------------- | ----------- | ---------------- |
|         0 | Emergency     | Black       | Red              |
|         1 | Alert         | Black       | Yellow           |
|         2 | Critical      | Black       | Magenta          |
|         3 | Error         | Red         | No Color         |
|         4 | Warning       | Yellow      | No Color         |
|         5 | Notice        | White       | Blue             |
|         6 | Informational | White       | No Color         |
|         7 | Debug         | Cyan        | No Color         |
|         8 | None          | NA          | NA               |

## Usage

### Code

```python
from ylog import Log

log = Log(loglevel=8)

log.emergency('Test emergency Print by importing')
log.alert('Test alert Print by importing')
log.critical('Test crtical Print by importing')
log.error('Test error Print by importing')
log.warning('Test warning Print by importing')
log.notice('Test notice Print by importing')
log.debug('Test Debug Print by importing')
log.info('Test info Print by importing')
```

### Output

![Output](images/output.png)
