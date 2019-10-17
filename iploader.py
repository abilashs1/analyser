'''
Created on Oct 15, 2019

@author: AbilashS2
'''
import os

from netloader import NetLoader, BASENAME_KEY, FILE_SIZE_KEY, MASK_KEY, USER_KEY, GROUP_KEY, TYPE_KEY, FULLPATH_KEY
from threading import Thread

def _loadingForVosThroughIp(ip, dlPath, downloadStatus):

    all_parameters = dict()
    #all_parameters[MASK_KEY] = "644"
    all_parameters[MASK_KEY] = "777"
    all_parameters[USER_KEY] = "usr"
    all_parameters[GROUP_KEY] = "system"
    all_parameters[TYPE_KEY] = "F"

    dlFullPath = dlPath
    basename = os.path.basename(dlFullPath)
    all_parameters[BASENAME_KEY] = basename

    # check if file exist and get the size
    if os.path.isfile(dlFullPath):
        size = os.path.getsize(dlFullPath)
        all_parameters[FILE_SIZE_KEY] = size
    else:
        all_parameters[FILE_SIZE_KEY] = -1

    all_parameters[FULLPATH_KEY] = dlFullPath
    loader = NetLoader(ip)
    downloadStatus.setText('Downloading...')
    status = loader.load_file(all_parameters)
    downloadStatus.setText(status)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return
    
# def load package through ip ...
def load_vos_package_ip(ip_address, package_full_path, downloadStatus):
    t1 = ThreadWithReturnValue(target=_loadingForVosThroughIp, args=(ip_address,package_full_path, downloadStatus))
    t1.start()    
    