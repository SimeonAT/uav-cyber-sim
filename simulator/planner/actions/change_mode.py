"""
Defines actions for changing UAV flight modes using MAVLink commands.

Includes logic for creating a mode-switching Action with execution and verification
steps based on HEARTBEAT messages and supported flight modes.
"""

from simulator.helpers.connections.mavlink.enums import (
  CopterMode, ModeFlag, CustomMainMode, CustomSubModeAuto, CustomSubModePOSCTL
)
from simulator.planner.action import Action
from simulator.planner.step import Step

import logging
from pymavlink import mavutil
from simulator.config import TIMEOUT

class SwitchMode(Step):
    """Step to switch the UAV flight mode."""

    def __init__(self, name: str,
                 base_mode: int,
                 main_mode: CustomMainMode,
                 sub_mode: CustomSubModeAuto | CustomSubModePOSCTL) -> None:
        super().__init__(name)
        # self.flight_mode = flight_mode
        self.base_mode = base_mode
        self.main_mode = main_mode
        self.sub_mode = sub_mode

    def exec_fn(self) -> None:
        """Send the SET_MODE command to the UAV with the given mode value."""
        # self.conn.mav.set_mode_send(
        #     self.conn.target_system,
        #     ModeFlag.CUSTOM_MODE_ENABLED,
        #     self.flight_mode.value,
        # )
        self.conn.mav.command_long_send(self.conn.target_system, self.conn.target_component,
                                        mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                                        self.base_mode, self.main_mode, self.sub_mode, 0,
                                        0, 0, 0)

    # def check_fn(self) -> bool:
    #     """Verify the UAV has switched to the target flight mode."""
    #     msg = self.conn.recv_match(type="HEARTBEAT")
    #     if msg and msg.custom_mode == self.flight_mode.value:
    #         return True
    #     return False

    def check_fn(self) -> bool:
      """
      Verify the UAV has switched to the target flight mode.
      This function was written by Claude AI.
      
      PX4 packs `custom_mode` as a union (see px4_custom_mode.h):
      reserved (bits 0-15), main_mode (bits 16-23), sub_mode (bits 24-31)
      
      So the raw uint32 from HEARTBEAT has to be unpacked before comparing
      against self.main_mode / self.sub_mode, unlike ArduPilot's flat
      custom_mode integer.

      Also checks COMMAND_ACK: HEARTBEAT alone gives no failure signal, so a rejected
      MAV_CMD_DO_SET_MODE (e.g. result=1, TEMPORARILY_REJECTED, which PX4 returns without
      a prior setpoint stream) would otherwise just hang silently. Logs the rejection reason
      instead. An ACK alone isn't success — only a matching HEARTBEAT confirms the switch.
      """
      msg = self.conn.recv_match(type=["HEARTBEAT", "COMMAND_ACK"],
                                 blocking=False, timeout=TIMEOUT)
      if not msg:
        return False

      if msg.get_type() == "COMMAND_ACK":
          if msg.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
              if msg.result != mavutil.mavlink.MAV_RESULT_ACCEPTED:
                  logging.error(
                      f"Mode Switch Rejected: result={msg.result} "
                      f"({mavutil.mavlink.enums['MAV_RESULT'][msg.result].name})"
                  )
          return False  # ACK alone doesn't confirm the mode is active yet

      recv_main_mode = (msg.custom_mode >> 16) & 0xFF
      recv_sub_mode = (msg.custom_mode >> 24) & 0xFF

      if recv_main_mode != self.main_mode:
        return False

      if recv_sub_mode != self.sub_mode:
        return False

      return True

# def make_set_mode(flight_mode: CopterMode) -> Action[Step]:
#     """Create an Action to switch the UAV flight mode."""
#     name = Action.Names.CHANGE_FLIGHTMODE
#     action = Action[Step](name, emoji=name.emoji)
#     step = SwitchMode(name=f"Switch to {flight_mode.name}", flight_mode=flight_mode)
#     action.add(step)
#     return action

def make_set_mode(base_mode: int,
                  main_mode: CustomMainMode,
                  sub_mode: CustomSubModeAuto | CustomSubModePOSCTL) -> Action[Step]:
    """Create an Action to switch the UAV flight mode."""
    name = Action.Names.CHANGE_FLIGHTMODE
    action = Action[Step](name, emoji=name.emoji)
    step = SwitchMode(name=f"Switch to base mode: {base_mode}, {main_mode.name} + {sub_mode.name}",
                      base_mode=base_mode, main_mode=main_mode, sub_mode=sub_mode)
    action.add(step)
    return action
