@echo off
C:\Languages\Python-3.10\envs\flask\Scripts\pip.exe  install -U pip -vv --proxy http://user:pass@pamo.admin-smolensk.ru:3128 --retries 10 -i https://pypi.python.org/simple
rem --index-url=http://pypi.python.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org
rem C:\Languages\Python-3.10\envs\flask\Scripts\pip.exe  install %1 -vv --proxy http://user:pass@pamo.admin-smolensk.ru:3128 --retries 10 -i https://pypi.python.org/simple
