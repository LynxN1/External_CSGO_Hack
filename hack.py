import ctypes
import os
import threading
import time
from sys import exit

import win32con as keymap
from tabulate import tabulate

from csgo import helper as h
from csgo.entity import Entity
from csgo.local import LocalPlayer
from csgo.memory import game_handle

WORKING = True
IN_GAME = False
TRIGGER_BOT_KEY = keymap.VK_MENU
BUNNY_HOP_KEY = keymap.VK_SPACE
CLOSE_CHEAT_KEY = keymap.VK_DELETE
FOV_ADD_KEY = keymap.VK_PRIOR
FOV_SUBTRACT_KEY = keymap.VK_NEXT
FOV_NORMALIZE_KEY = keymap.VK_HOME


def wall_hack():
    while WORKING:
        if IN_GAME:
            for i in range(1, 100):
                try:
                    entity_list = game_handle.read_uint(ent.glow_object() + 0x38 * (i - 1) + 0x4)

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
                            game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), (100 - health) / 100.0)
                            # G
                            game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), health / 100.0)
                            # A
                            game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 1.0)

                            game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                            game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

                    elif h.class_id_c4(ent.class_id(entity_list)) or h.class_id_gun(ent.class_id(entity_list)):
                        # R
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 0.95)
                        # G
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 0.12)
                        # B
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 0.54)
                        # A
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)

                        game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                        game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

                    elif h.class_id_grenade(ent.class_id(entity_list)):
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 1.0)
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 1.0)
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 1.0)
                        game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)
                        game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                        game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)
                except:
                    pass
        time.sleep(0.001)
    print("WallHack finished")


def trigger_bot():
    t = 2
    ct = 3
    delay = 0.03
    while WORKING:
        if IN_GAME:
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
        time.sleep(0.001)
    print("TriggerBot finished")


def bunny_hop():
    while WORKING:
        if IN_GAME:
            if lp.get_current_state() == 5:
                while ctypes.windll.user32.GetAsyncKeyState(BUNNY_HOP_KEY):
                    if ent.get_flag(lp.local_player()) == 257:
                        lp.force_jump(5)
                        time.sleep(0.01)
                    else:
                        lp.force_jump(4)
                        time.sleep(0.01)
        time.sleep(0.001)
    print("BunnyHop finished")


def radar_hack():
    while WORKING:
        if IN_GAME:
            for i in ent.entity_list:
                ent.set_is_visible(i, True)
        time.sleep(0.001)
    print("RadarHack finished")


def fov_changer():
    while WORKING:
        if IN_GAME:
            try:
                v1 = lp.get_fov()
                if ctypes.windll.user32.GetAsyncKeyState(FOV_ADD_KEY):
                    v2 = v1 + 1
                    lp.set_fov(v2)
                elif ctypes.windll.user32.GetAsyncKeyState(FOV_SUBTRACT_KEY):
                    v2 = v1 - 1
                    lp.set_fov(v2)
                elif ctypes.windll.user32.GetAsyncKeyState(FOV_NORMALIZE_KEY):
                    lp.set_fov(90)
            except:
                pass
        time.sleep(0.1)
    print("FovChanger finished")


def check_in_game_status():
    global IN_GAME
    while WORKING:
        IN_GAME = ent.in_game()
        time.sleep(2.5)


def close_cheat():
    global WORKING
    while WORKING:
        if ctypes.windll.user32.GetAsyncKeyState(CLOSE_CHEAT_KEY):
            print("Exiting...")
            if IN_GAME:
                lp.set_fov(90)
            WORKING = False
        time.sleep(0.2)


def show_info():
    headers = ["Function", "Key"]
    table = [
        ["Triggerbot", "Alt"],
        ["Bunnyhop", "Space"],
        ["Change FOV", "Page Up, Page Down, Home"],
        ["Exit", "Delete"]
    ]
    print(tabulate(table, headers, tablefmt="github"))
    print()


def start_threads():
    threading.Thread(target=wall_hack).start()
    threading.Thread(target=trigger_bot).start()
    threading.Thread(target=bunny_hop).start()
    threading.Thread(target=radar_hack).start()
    threading.Thread(target=fov_changer).start()
    threading.Thread(target=check_in_game_status).start()
    threading.Thread(target=close_cheat).start()


if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW("NoName External")
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    try:
        ent = Entity()
        lp = LocalPlayer()
        ent.entity_loop()
        start_threads()
        print("Cheat activated successfully!" + "\n")
        show_info()
    except Exception as e:
        input(e)
        exit(0)
