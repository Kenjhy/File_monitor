if you cant kill proccess wit trl + c 

Get-WmiObject Win32_Process | Where-Object {$_.CommandLine -like '*en_file_monitor_amaris_test.py*'} | Select-Object ProcessId,CommandLine

then

taskkill /F /PID <PID>