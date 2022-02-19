import struct

from csgo.offsets import offset_list
from csgo.helper import *


class LocalPlayer:
    def __init__(self, mem) -> None:
        self.mem = mem

    def local_player(self):
        return self.mem.game_handle.read_uint(self.mem.client_dll + hex(offset_list["dwLocalPlayer"]))

    def get_current_state(self):
        return self.mem.game_handle.read_int(self.mem.client_dll + hex(offset_list["dwForceJump"]))

    def get_crosshair_id(self):
        return self.mem.game_handle.read_uint(self.local_player() + hex(offset_list["m_iCrosshairId"]))

    def get_entity_by_crosshair(self):
        return self.mem.game_handle.read_uint(self.mem.client_dll + hex(offset_list["dwEntityList"]) + ((self.get_crosshair_id() - 1) * 0x10))

    def get_team_by_crosshair(self):
        return self.mem.game_handle.read_int(self.get_entity_by_crosshair() + hex(offset_list["m_iTeamNum"]))

    def force_jump(self, flag):
        self.mem.game_handle.write_int(self.mem.client_dll + hex(offset_list["dwForceJump"]), flag)

    def force_attack(self, flag):
        self.mem.game_handle.write_int(self.mem.client_dll + hex(offset_list["dwForceAttack"]), flag)

    def force_attack2(self, flag):
        self.mem.game_handle.write_int(self.mem.client_dll + hex(offset_list["dwForceAttack2"]), flag)

    def get_fov(self):
        return self.mem.game_handle.read_uint(self.local_player() + hex(offset_list["m_iDefaultFOV"]))

    def set_fov(self, value):
        self.mem.game_handle.write_int(self.local_player() + hex(offset_list["m_iDefaultFOV"]), value)

    def aim_punch_angle(self):
        x = self.mem.game_handle.read_float(self.local_player() + hex(offset_list["m_aimPunchAngle"]))
        y = self.mem.game_handle.read_float(self.local_player() + hex(offset_list["m_aimPunchAngle"]) + 0x4)
        z = self.mem.game_handle.read_float(self.local_player() + hex(offset_list["m_aimPunchAngle"]) + 0x8)
        return Vector3(x, y, z)

    def view_matrix(self):
        view = self.mem.game_handle.read_bytes(self.mem.client_dll + hex(offset_list["dwViewMatrix"]), 64)
        matrix = struct.unpack("16f", view)
        return matrix
