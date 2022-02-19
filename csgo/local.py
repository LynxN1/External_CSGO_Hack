import struct

from csgo import offsets
from csgo.helper import *
from csgo.memory import game_handle, client_dll


class LocalPlayer:

    def local_player(self):
        return game_handle.read_uint(client_dll + offsets.dwLocalPlayer)

    def get_current_state(self):
        return game_handle.read_int(client_dll + offsets.dwForceJump)

    def get_crosshair_id(self):
        return game_handle.read_uint(self.local_player() + offsets.m_iCrosshairId)

    def get_entity_by_crosshair(self):
        return game_handle.read_uint(client_dll + offsets.dwEntityList + ((self.get_crosshair_id() - 1) * 0x10))

    def get_team_by_crosshair(self, entity):
        return game_handle.read_int(entity + offsets.m_iTeamNum)

    def force_jump(self, flag):
        game_handle.write_int(client_dll + offsets.dwForceJump, flag)

    def force_attack(self, flag):
        game_handle.write_uint(client_dll + offsets.dwForceAttack, flag)

    def force_attack2(self, flag):
        game_handle.write_uint(client_dll + offsets.dwForceAttack2, flag)

    def get_fov(self):
        return game_handle.read_int(self.local_player() + offsets.m_iDefaultFOV)

    def set_fov(self, value):
        game_handle.write_int(self.local_player() + offsets.m_iDefaultFOV, value)

    def aim_punch_angle(self):
        x = game_handle.read_float(self.local_player() + offsets.m_aimPunchAngle)
        y = game_handle.read_float(self.local_player() + offsets.m_aimPunchAngle + 0x4)
        z = game_handle.read_float(self.local_player() + offsets.m_aimPunchAngle + 0x8)
        return Vector3(x, y, z)

    def view_matrix(self):
        view = game_handle.read_bytes(client_dll + offsets.dwViewMatrix, 64)
        matrix = struct.unpack("16f", view)
        return matrix
