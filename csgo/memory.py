import re

import pymem


# try:
#     game_handle = pymem.Pymem('csgo.exe')
#     client_dll = pymem.pymem.process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
#     client_dll_size = pymem.pymem.process.module_from_name(game_handle.process_handle, 'client.dll').SizeOfImage
#     engine_dll = pymem.pymem.process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll
# except ProcessNotFound as e:
#     print(e)
#     os._exit(0)


class Memory:
    def __init__(self):
        self.game_handle = pymem.Pymem('csgo.exe')
        self.client_dll = pymem.pymem.process.module_from_name(self.game_handle.process_handle, 'client.dll').lpBaseOfDll
        self.client_dll_size = pymem.pymem.process.module_from_name(self.game_handle.process_handle, 'client.dll').SizeOfImage
        self.engine_dll = pymem.pymem.process.module_from_name(self.game_handle.process_handle, 'engine.dll').lpBaseOfDll

    def get_sig(self, modname, pattern, extra=0, offset=0, relative=True):
        module = pymem.pymem.process.module_from_name(self.game_handle.process_handle, modname)
        _bytes = self.game_handle.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
        match = re.search(pattern, _bytes).start()
        non_relative = self.game_handle.read_int(module.lpBaseOfDll + match + offset) + extra
        yes_relative = self.game_handle.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
        return yes_relative if relative else non_relative
