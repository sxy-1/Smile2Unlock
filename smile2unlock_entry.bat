@echo off

if "%1"=="show" goto begin
start mshta vbscript:createobject("wscript.shell").run("%~f0 show",0)(window.close)&&exit
:begin
::执行具体任务
call activate Smile2Unlock_last
@REM conda在bat中使用call
@REM cd D:/pyproject/Smile2Unlock
@REM 无论改bat在哪，都不需要指定路径，将会在任务计划中指定
python ./smile2unlock_entry.py

::https://blog.csdn.net/xiaoyw71/article/details/135340701
::bat文件会使用cmd 请放入杀软白名单