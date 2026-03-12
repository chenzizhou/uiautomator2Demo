@echo on

adb devices -l

for /f "skip=1 tokens=1" %%i in ('adb devices -l') do (
    adb -s %%i remount
	rem adb -s %%i pull /data/data/com.huawei.hwddmp ./db/%%i
    rem BDG0119B15000179  FRU6R20218000006
    rem adb -s BDG0119B15000179 push install/atx-agent /data/local/tmp
    rem adb -s BDG0119B15000179 shell chmod 755 /data/local/tmp/atx-agent
    rem adb -s BDG0119B15000179 shell /data/local/tmp/atx-agent server -d
    adb -s %%i install install/app-uiautomator.apk
    adb -s %%i install install/app-uiautomator-test.apk
    adb -s %%i push install/minicap /data/local/tmp
    adb -s %%i push install/minitouch /data/local/tmp
    adb -s %%i push install/atx-agent /data/local/tmp
    adb -s %%i shell chmod 755 /data/local/tmp/atx-agent
    adb -s %%i shell /data/local/tmp/atx-agent server -d
)
