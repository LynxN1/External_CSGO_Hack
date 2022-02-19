import ctypes
import os
import threading
import time
from sys import exit

import win32con as keymap

from csgo import helper as h
from csgo.entity import Entity
from csgo.local import LocalPlayer
from csgo.memory import Memory

WORKING             = True
TRIGGER_BOT_KEY     = keymap.VK_MENU
BUNNY_HOP_KEY       = keymap.VK_SPACE
CLOSE_CHEAT_KEY     = keymap.VK_DELETE
FOV_ADD_KEY         = keymap.VK_PRIOR
FOV_SUBTRACT_KEY    = keymap.VK_NEXT
FOV_NORMALIZE_KEY   = keymap.VK_HOME


def wall_hack():
    while True:
        if WORKING:
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
                            health = ent.get_health(entity_list)
                            # R
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), (100 - health) / 100.0)
                            # G
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), health / 100.0)
                            # A
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 1.0)
                            
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

                    elif h.class_id_c4(ent.class_id(entity_list)) or h.class_id_gun(ent.class_id(entity_list)):
                        # R
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 0.95)
                        # G
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 0.12)
                        # B
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 0.54)
                        # A
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


def trigger_bot():
    t = 2
    ct = 3
    delay = 0.03
    while True:
        if WORKING:
            try:
                if ctypes.windll.user32.GetAsyncKeyState(TRIGGER_BOT_KEY):
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
            time.sleep(0.001)
        else:
            print("TriggerBot finished")
            return


def bunny_hop():
    while True:
        if WORKING:
            try:
                if lp.get_current_state() == 5:
                    while ctypes.windll.user32.GetAsyncKeyState(BUNNY_HOP_KEY):
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
        if WORKING:
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


def fov_changer():
    while True:
        if WORKING:
            try:
                v1 = lp.get_fov()
                if ent.in_game():
                    if ctypes.windll.user32.GetAsyncKeyState(FOV_ADD_KEY):
                        v2 = v1 + 1
                        lp.set_fov(v2)
                    elif ctypes.windll.user32.GetAsyncKeyState(FOV_SUBTRACT_KEY):
                        v2 = v1 - 1
                        lp.set_fov(v2)
                    elif ctypes.windll.user32.GetAsyncKeyState(FOV_NORMALIZE_KEY):
                        lp.set_fov(90)
            except Exception:
                pass
            time.sleep(0.1)
        else:
            print("FovChanger finished")
            return


def close_cheat():
    global WORKING
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(CLOSE_CHEAT_KEY):
            print("Exiting...")
            if ent.in_game():
                lp.set_fov(90)
            mem.game_handle.write_int(ent.engine_ptr() + 0x174, -1)
            WORKING = False
            return
        time.sleep(0.2)


# def test():
#     while True:
#         if ent.in_game():
#             a = lp.get_entity_by_crosshair()
#             b = ent.class_id(a)
#             print(f"{a}:{b}")
#             time.sleep(0.5)


def start_threads():
    threading.Thread(target=wall_hack).start()
    threading.Thread(target=trigger_bot).start()
    threading.Thread(target=bunny_hop).start()
    threading.Thread(target=radar_hack).start()
    threading.Thread(target=fov_changer).start()
    threading.Thread(target=close_cheat).start()
    # threading.Thread(target=test).start()


if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW("NoName External")
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    try:
        mem = Memory()
        ent = Entity(mem)
        lp = LocalPlayer(mem)
        ent.entity_loop()
        start_threads()
        print("Cheat activated successfully!" + "\n")
        print("TriggerBot\t — hold Alt")
        print("BunnyHop\t — hold Space")
        print("ChangeFov\t — Page Up, Page Down, Home")
        print("Exit\t\t — press Delete" + "\n")
    except Exception as e:
        print(e)
        input()
        exit(0)
