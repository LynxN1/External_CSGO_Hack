import re

from pymem import Pymem, process

try:
    game_handle = Pymem("csgo.exe")
    client_dll = process.module_from_name(game_handle.process_handle, "client.dll").lpBaseOfDll
    client_dll_size = process.module_from_name(game_handle.process_handle, "client.dll").SizeOfImage
    engine_dll = process.module_from_name(game_handle.process_handle, "engine.dll").lpBaseOfDll
except Exception as e:
    input(e)
    exit(0)


def get_sig(modname, pattern, extra=0, offset=0, relative=True):
    module = process.module_from_name(game_handle.process_handle, modname)
    _bytes = game_handle.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, _bytes).start()
    non_relative = game_handle.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = game_handle.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return yes_relative if relative else non_relative
