@echo off
SET countLoop=0
:loop
ping 192.168.1.79
SET /A countLoop=countLoop+1
echo %countLoop%
goto loop

