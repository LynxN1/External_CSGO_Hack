from csgo import offsets
from csgo.helper import *
from csgo.local import LocalPlayer
from csgo.memory import game_handle, client_dll, engine_dll


class Entity(LocalPlayer):
    def __init__(self) -> None:
        self.entity_list = []
        self.glow_objects_list = []
        self.player = self.get_entity(0)

    def entity_loop(self):
        self.entity_list.clear()
        try:
            for i in range(1, 32):
                entity = game_handle.read_uint(client_dll + offsets.dwEntityList + i * 0x10)
                if entity != 0:
                    self.entity_list.append(entity)
        except Exception as err:
            print(err)

    def glow_objects_loop(self):
        self.glow_objects_list.clear()
        try:
            for i in range(1, 2222):
                entity = game_handle.read_uint(self.glow_object() + 0x38 * (i - 1) + 0x4)
                if entity != 0:
                    self.glow_objects_list.append(entity)
        except Exception as err:
            print(err)

    def get_entity(self, entity):
        return game_handle.read_uint((client_dll + offsets.dwEntityList) + entity * 0x10)

    def get_life_state(self, entity):
        return game_handle.read_int(entity + offsets.m_lifeState)

    def get_health(self, entity):
        return game_handle.read_int(entity + offsets.m_iHealth)

    def get_team(self, entity):
        return game_handle.read_int(entity + offsets.m_iTeamNum)

    def get_dormant(self, entity):
        return game_handle.read_bool(entity + offsets.m_bDormant)

    def set_dormant(self, entity, val: bool):
        return game_handle.write_bool(entity + offsets.m_bDormant, val)

    def is_visible(self, entity):
        return game_handle.read_bool(entity + offsets.m_bSpotted)

    def set_is_visible(self, entity, val: bool):
        return game_handle.write_bool(entity + offsets.m_bSpotted, val)

    def is_defusing(self, entity):
        return game_handle.read_bool(entity + offsets.m_bIsDefusing)

    def get_flag(self, entity):
        return game_handle.read_int(entity + offsets.m_fFlags)

    def get_shots_fired(self, entity):
        return game_handle.read_uint(entity + offsets.m_iShotsFired)

    def get_total_hits(self, entity):
        return game_handle.read_uint(entity + 0x103f8)  # m_totalHitsOnServer

    def is_bomb_planted(self):
        return game_handle.read_bool(
            game_handle.read_int(
                client_dll + offsets.dwGameRulesProxy) + offsets.m_bBombPlanted)

    def glow_object(self):
        return game_handle.read_uint(client_dll + offsets.dwGlowObjectManager)

    def glow_object_size(self):
        return game_handle.read_uint(self.glow_object() + 0xC)

    def glow_index(self, entity):
        return game_handle.read_uint(entity + offsets.m_iGlowIndex)

    def is_bomb_planted(self):
        return game_handle.read_bool((client_dll + offsets.dwGameRulesProxy) + offsets.m_bBombPlanted)

    def is_valid(self, entity):
        if self.get_team(entity) != 0 and self.get_health(entity) > 0 and self.get_dormant(entity) == False:
            return True
        else:
            return False

    def engine_ptr(self):
        return game_handle.read_uint(engine_dll + offsets.dwClientState)

    def in_game(self):
        return game_handle.read_uint(self.engine_ptr() + offsets.dwClientState_State) == 6

    def class_id(self, entity):
        dwClientNetworkable = game_handle.read_uint(entity + 0x8)
        dwGetClientClassFn = game_handle.read_uint(dwClientNetworkable + 0x8)
        dwEntityClientClass = game_handle.read_uint(dwGetClientClassFn + 0x1)
        classID = game_handle.read_uint(dwEntityClientClass + 0x14)
        return classID

    def get_position(self, entity):
        x = game_handle.read_float(entity + offsets.m_vecOrigin)
        y = game_handle.read_float(entity + offsets.m_vecOrigin + 0x4)
        z = game_handle.read_float(entity + offsets.m_vecOrigin + 0x8)
        return Vector3(x, y, z)

    def get_bone_position(self, entity, bone_id):
        base = game_handle.read_int(entity + offsets.m_dwBoneMatrix)
        x = game_handle.read_float(base + 0x30 * bone_id + 0x0c)
        y = game_handle.read_float(base + 0x30 * bone_id + 0x1c)
        z = game_handle.read_float(base + 0x30 * bone_id + 0x2c)
        return Vector3(x, y, z)

    def active_weapon(self):
        actWeapon = game_handle.read_uint(self.local_player() + offsets.m_hActiveWeapon) & 0xFFF
        actWeapon = game_handle.read_uint(client_dll + offsets.dwEntityList + (actWeapon - 1) * 0x10)
        return game_handle.read_short(actWeapon + offsets.m_iItemDefinitionIndex)

    def get_name(self, entity):
        player_info = game_handle.read_uint(self.engine_ptr() + offsets.dwClientState_PlayerInfo)

        player_info_items = game_handle.read_uint(
            game_handle.read_uint(player_info + 0x40) + 0xC
        )
        info = game_handle.read_uint(player_info_items + 0x28 + (entity * 0x34))

        if info > 0:
            return game_handle.read_string(info + 0x10)

    def get_rank(self, entity):
        player_resources = game_handle.read_uint(client_dll + offsets.dwPlayerResource)
        return game_handle.read_int(player_resources + offsets.m_iCompetitiveRanking + (entity * 0x4))
