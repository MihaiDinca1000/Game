@echo off
title Mon Calculatrice
color 0B
echo Tapotez "exit" pour terminer :)


:start 

set /p gigi= tape une operation de calcule: 

set /a RESULTAT=%gigi%

echo %RESULTAT% 

if %gigi%==aurevoir exit

pause
cls
goto start 





