
@echo off
title MUSICSRE-236
color 0a

echo /w vous demande d'appuyer une touche pour commencer
echo /i si la destination n'existe pas il va cree le repertoire
echo /Uniquement DISCO, D2B, DSS, MAX, CODEC.
echo Script to export only what is mandatory to run the simulation



xcopy /e /i /w        X:\MSRE\Ref\MSRE_10.2.0\install\Windows\x86_64\lib       C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Windows\x86_64\lib 
xcopy /e /i	      	  X:\MSRE\Ref\MSRE_10.2.0\install\Windows\x86_64\bin       C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Windows\x86_64\bin
xcopy /e /i		      X:\MSRE\Ref\MSRE_10.2.0\install\Windows\i386\bin         C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Windows\i386\bin
echo.
xcopy /e /i           X:\MSRE\Ref\MSRE_10.2.0\install\Windows\i386\lib         C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Windows\i386\lib


echo.
echo ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪ LINUX ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ LINUX  ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪ 


xcopy /e /i	  		X:\MSRE\Ref\MSRE_10.2.0\install\Linux\x86_64\lib            C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Linux\x86_64\lib
xcopy /e /i	  		X:\MSRE\Ref\MSRE_10.2.0\install\Linux\x86_64\bin	        C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Linux\x86_64\bin
echo.
xcopy /e /i	  		X:\MSRE\Ref\MSRE_10.2.0\install\Linux\i386\bin	        	C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Linux\i386\bin
xcopy /e /i	  		X:\MSRE\Ref\MSRE_10.2.0\install\Linux\i386\lib	        	C:\Users\%USERNAME%\Desktop\MSRE_RUN\MSRE_10.2.0\install\Linux\i386\lib





ECHO %USERNAME% les fichier ses sont opiès :) :)

pause


