REM This script will copy the contents of this folder over to Golem (raspberry pi)
REM /Y means perform and overwrite on the copy
xcopy %cd% \\GOLEM\Golem /Y /e
exit