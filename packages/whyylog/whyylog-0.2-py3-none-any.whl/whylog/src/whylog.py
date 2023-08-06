from colorama import Fore, init
import datetime as dt
import os, sys
import inspect

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class Log:
    def __init__(self, loglevel=6, tofile=False, showline=False, log_filename='mylog.log') -> None:
        """Print or Save to a log file.
        
        | Log Level | Log Type      | Print Color | Background Color |
        | ---------:| ------------- | ----------- | ---------------- |
        |         0 | Emergency     | Black       | Red              |
        |         1 | Alert         | Black       | Yellow           |
        |         2 | Critical      | Black       | Magenta          |
        |         3 | Error         | Red         | No Color         |
        |         4 | Warning       | Yellow      | No Color         |
        |         5 | Notice        | White       | Blue             |
        |         6 | Informational | Green       | No Color         |
        |         7 | Debug         | Cyan        | No Color         |
        |         8 | None          | NA          | NA               |
 
        
        Parameters
        ----------
        loglevel     : int, optional > log level 0-7, by default 7
        log_filename : str, optional > if you want to change the log file name, by default 'mopy.log'
        """
        self.loglevel = loglevel
        self.tofile = tofile
        self.logfile = log_filename
        self.showline = showline
        self.color_lookup = {
            'emergency' : {'color' : '\033[30;41m' , 'loglevel' : 0},
            'alert'     : {'color' : '\033[30;43m' , 'loglevel' : 1},
            'critical'  : {'color' : '\033[30;45m' , 'loglevel' : 2},
            'error'     : {'color' : '\033[31m'    , 'loglevel' : 3},
            'warning'   : {'color' : '\033[33m'    , 'loglevel' : 4},
            'notice'    : {'color' : '\033[37;44m' , 'loglevel' : 5},
            'info'      : {'color' : '\033[32m'    , 'loglevel' : 6},          # '\033[32m',
            'debug'     : {'color' : '\033[36m'    , 'loglevel' : 7},
            # 'process'   : '\033[35m',
        }
        pass

    def get_vars(self):
        self.text_color = self.color_lookup.get(self.log_type.lower()).get('color')
        self.method_called_from = path_taken = ' > '.join([f"{_func.filename.split('/')[-1].split('.')[0]}.{_func.function}|Line -> {_func.lineno}" for _func in inspect.stack()[3:]]) # pardon me lol; need to make this not messy. job for future me.
        self.file_called_from = ' > '.join(set([f"{_func.filename.split('/')[-1]}" for _func in inspect.stack()[3:-1]]))
        self.date_time = str(dt.datetime.now())[0:19]
    
    def print_log(self, message):
        self.get_vars()
        if self.loglevel >= self.color_lookup.get(self.log_type.lower()).get('loglevel'):
            print(f'{self.text_color}{self.date_time} [{self.log_type.upper()}] ({self.file_called_from}) > ({self.method_called_from}):\033[00m {message}')
        if self.tofile:
            with open(self.logfile, 'a') as _l: _l.write(f'{self.date_time} [{self.log_type.upper()}] ({self.file_called_from}) > ({self.method_called_from}): {message}\n')
    
    def emergency(self, message):
        """Emergency Message

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
            
    def alert(self, message):
        """Alert Message

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
            
    def critical(self, message):
        """Critical Message

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
            
    def error(self, message):
        """Error Message

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
    
    def warning(self, message):
        """Warning Message

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
            
    def notice(self, message):
        """Notice

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
            
    def debug(self, message):
        """Debug Message

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
            
    def info(self, message):
        """Info Message

        Parameters
        ----------
        message : str > message to print
        """
        self.log_type = inspect.stack()[0][3]
        self.print_log(message)
            
def main():
    log = Log()
    log.debug('Test Debug Message')

def test():
    # a = inspect.stack()
    path_taken = ' > '.join([_func.function for _func in inspect.stack()])
    print(path_taken)

if __name__ == '__main__':
    test()