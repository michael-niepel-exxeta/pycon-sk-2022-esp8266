# This file is executed on every boot (including wake-boot from deepsleep)
#uos.dupterm(None, 1) # disable REPL on UART(0)
#import webrepl
#webrepl.start()
# disable debug
import esp
esp.osdebug(None)
# enable garbage collector
import gc
gc.collect()
