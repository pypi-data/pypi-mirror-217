from cnextb.device import *

if __name__ == '__main__':
    dev = scan_devices()
    dev_str = ''
    for ele in dev.keys():
        if 'USB' in ele:
            dev_str = ele
            break
    cnexdev = CnextbDevice(dev_str)
    cnexdev.exe_cmd("RUN:POWER DOWN")
    cnexdev.exe_cmd("RUN:POWER UP")
