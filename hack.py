import ctypes
import os
import threading
import time
from sys import exit

from csgo import helper as h
from csgo.entity import Entity
from csgo.local import LocalPlayer
from csgo.memory import Memory
from hex_keycodes import *

flag = {"working": True}


def wall_hack():
    while True:
        if flag["working"]:
            try:
                for i in range(1, 1024):
                    entity_list = mem.game_handle.read_uint(ent.glow_object() + 0x38 * (i - 1) + 0x4)

                    if entity_list <= 0:
                        continue
                    if ent.class_id(entity_list) is None:
                        continue
                    if ent.get_dormant(entity_list):
                        continue

                    if ent.class_id(entity_list) == 40:
                        if ent.get_team(entity_list) != ent.get_team(lp.local_player()):
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 0.47)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 0.24)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 1.0)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

                    elif h.class_id_c4(ent.class_id(entity_list)) or h.class_id_gun(ent.class_id(entity_list)):
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 0.95)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 0.12)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 0.54)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

                    elif h.class_id_grenade(ent.class_id(entity_list)):
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 1.0)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 1.0)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 1.0)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)
            except Exception:
                pass
            time.sleep(0.001)
        else:
            print("WallHack finished")
            return


def trigger_bot(key: int, delay: float):
    t = 2
    ct = 3
    while True:
        if flag["working"]:
            try:
                if ctypes.windll.user32.GetAsyncKeyState(key):
                    local_player_id = ent.get_team(lp.local_player())
                    if local_player_id == t:
                        if ent.get_team(lp.get_entity_by_crosshair()) == ct:
                            time.sleep(delay)
                            lp.force_attack(6)
                    elif local_player_id == ct:
                        if ent.get_team(lp.get_entity_by_crosshair()) == t:
                            time.sleep(delay)
                            lp.force_attack(6)
            except Exception:
                pass
            time.sleep(0.01)
        else:
            print("TriggerBot finished")
            return


def bunny_hop(key: int):
    while True:
        if flag["working"]:
            try:
                if lp.get_current_state() == 5:
                    while ctypes.windll.user32.GetAsyncKeyState(key):
                        if ent.get_flag(lp.local_player()) == 257:
                            lp.force_jump(5)
                            time.sleep(0.01)
                        else:
                            lp.force_jump(4)
                            time.sleep(0.01)
            except Exception:
                pass
            time.sleep(0.001)
        else:
            print("BunnyHop finished")
            return


def radar_hack():
    while True:
        if flag["working"]:
            try:
                if ent.in_game():
                    for i in ent.entity_list:
                        ent.set_is_visible(i, True)
            except Exception:
                pass
            time.sleep(1)
        else:
            print("RadarHack finished")
            return


def fov_changer(key_add: int, key_subtract: int, key_normalize: int):
    while True:
        if flag["working"]:
            try:
                v1 = lp.get_fov()
                if ent.in_game():
                    if ctypes.windll.user32.GetAsyncKeyState(key_add):
                        v2 = v1 + 1
                        lp.set_fov(v2)
                    elif ctypes.windll.user32.GetAsyncKeyState(key_subtract):
                        v2 = v1 - 1
                        lp.set_fov(v2)
                    elif ctypes.windll.user32.GetAsyncKeyState(key_normalize):
                        lp.set_fov(90)
            except Exception:
                pass
            time.sleep(0.1)
        else:
            print("FovChanger finished")
            return


def close_cheat(key: int):
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(key):
            print("Exiting...")
            if ent.in_game():
                lp.set_fov(90)
            mem.game_handle.write_int(ent.engine_ptr() + 0x174, -1)
            flag["working"] = False
            return
        time.sleep(0.2)


def start_threads():
    threading.Thread(target=wall_hack).start()
    threading.Thread(target=trigger_bot, args=[VK_MENU, 0.02]).start()
    threading.Thread(target=bunny_hop, args=[VK_SPACE]).start()
    threading.Thread(target=radar_hack).start()
    threading.Thread(target=fov_changer, args=[VK_UP, VK_DOWN, VK_RIGHT]).start()
    threading.Thread(target=close_cheat, args=[VK_DELETE]).start()


if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW("NoName External")
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    try:
        mem = Memory()
        ent = Entity(mem)
        lp = LocalPlayer(mem)
        ent.entity_loop()
        start_threads()
        print("Cheat activated successfully!")
        print("TriggerBot — hold Alt")
        print("BunnyHop — hold Space")
        print("ChangeFov —  up arrow to add, down arrow to subtract, right arrow to normalize")
        print("Exit — press Delete")
    except Exception as e:
        print(e)
        input()
        exit(0)
