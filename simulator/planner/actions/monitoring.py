"""
Upload mission action module.

Defines the action to upload a mission from a file located in the `missions/` folder
to an ArduPilot-based UAV using MAVLink. The mission file should be in `.waypoints`
format.

"""

import logging

from simulator.helpers.connections.mavlink.enums import MsgID
from simulator.helpers.connections.mavlink.streams import ask_msg, stop_msg
from simulator.helpers.coordinates import GRA
from simulator.planner.action import Action
from simulator.planner.step import Step

import pymavlink.dialects.v20.development as px4mavlink
from simulator.helpers.connections.mavlink.enums import LandState

from cmd import Cmd
from pymavlink import mavutil
E7ToDeg = lambda e7 : e7 / 10**7


class CheckItems(Step):
    """Request and check all waypoints from the UAV."""

    def __init__(self, name: str):
        super().__init__(name)
        self._item_seq = 0
        self._mission_count: int | None = None

    def exec_fn(self) -> None:
        """Request the next waypoint from the UAV."""
        ask_msg(self.conn, msg_id=MsgID.MISSION_CURRENT, interval=100_000)
        self.conn.mav.mission_request_list_send(
            self.conn.target_system, self.conn.target_component
        )

    def check_fn(self) -> bool:
        """Check the next waypoint from the UAV."""
        if not self._mission_count:
            msg = self.conn.recv_match(type="MISSION_COUNT")
            if msg:
                self._mission_count = msg.count
                logging.info(
                    f"📦 Vehicle {self.conn.target_system} has {msg.count} mission items"
                )
            else:
                return False

        curr_msg = self.conn.recv_match(type="MISSION_CURRENT")
        # if not curr_msg or curr_msg.seq == self._item_seq:
        #     return False
        if not curr_msg:
          return False

        while self._item_seq < curr_msg.seq:
            logging.info(
                f"Vehicle {self.conn.target_system}: ⭐ Reached item: {self._item_seq}"
            )
            self._item_seq += 1
        self.conn.mav.mission_request_send(
            self.conn.target_system, self.conn.target_component, self._item_seq
        )
        item = self.conn.recv_match(type="MISSION_ITEM", blocking=True)
        gra_wp = GRA(lat=float(item.x), lon=float(item.y), alt=float(item.z))  # type: ignore
        self.target_pos = self.origin.to_rel(gra_wp)
        # logging.info(
        #     f"Vehicle {self.conn.target_system}: 📍 Target Position: {self.target_pos.short()}"
        # )
        if self._item_seq == self._mission_count - 1:
            return True
        return False


class CheckEndMission(Step):
    """Check for mission completion."""

    def exec_fn(self) -> None:
        """No execution needed; just checking."""
        return

    # def check_fn(self) -> bool:
    #     """Check mission completion."""
    #     msg = self.conn.recv_match(type="STATUSTEXT")
    #     if msg:
    #         text = msg.text.strip().lower()
    #         if "disarming" in text:
    #             logging.info(f"Vehicle {self.conn.target_system}: Mission completed")
    #             stop_msg(self.conn, msg_id=MsgID.GLOBAL_POSITION_INT)
    #             return True
    #     return False

    def check_fn(self) -> bool:
      """Check mission completion via the HEARTBEAT arming bit.

         Debugging assistance and code by Claude (Anthropic), Claude Sonnet 5,
         August 2026.

         Both the `planner/actions/take_off.py` and `planner/actions/land.py` files in
         `uav-cyber-sim` also utilizes `EXTENDED_SYS_STATE` whether the drone has
         taken off or landed, respectively.

         UCI TODO: In the original version of this function in `uav-cyber-sim`, 
         the function looks for the ArduPilot "disarming" string to check whether a
         mission is complete. This function implementation for PX4 is similar, checking for
         whether a drone lands to determine whether a mission is complete.

         Both implementations fail when a drone has to land or disarm mid-flight and fails to
         complete a mission. Find a better way to check for mission completion or mission failure,
         and write a `logging.info` print statement to indicate whether the mission was successful
         or a failure.
      """
      msg = self.conn.recv_match(type="EXTENDED_SYS_STATE", blocking=False)
      if msg:
        logging.info(msg)

      if msg and msg.landed_state == LandState.ON_GROUND:
        logging.info(f"Vehicle {self.conn.target_system}: Mission completed (landed)")
        stop_msg(self.conn, msg_id=MsgID.GLOBAL_POSITION_INT)
        return True
      return False


def make_monitoring() -> Action[Step]:
    """Monitor mission items."""
    name = Action.Names.MONITOR_MISSION
    monitoring = Action[Step](name=name, emoji=name.emoji)
    monitoring.add(CheckItems(name="check items"))
    monitoring.add(CheckEndMission(name="check end mission"))
    return monitoring


class ReachedItem(Step):
    """
    Check if a mission item is reached.
    Ardupilot does not send MISSION_ITEM_REACHED for all mission items.
    CheckItems is more reliable for monitoring mission progress.
    """

    def __init__(self, name: str, item: int = 0):
        super().__init__(name)
        self._item = item

    def exec_fn(self) -> None:
        """No execution needed; just checking."""
        ask_msg(conn=self.conn, msg_id=MsgID.GLOBAL_POSITION_INT, interval=100_000)

    def check_fn(self) -> bool:
        """Check if a item is reached."""
        msg = self.conn.recv_match(type="MISSION_ITEM_REACHED")
        # logging.debug(f"Vehicle {conn.target_system}: MISSION_ITEM_REACHED: {msg}")
        if msg:
            if msg.seq == self._item:
                logging.info(
                    f"Vehicle {self.conn.target_system}: ⭐ Reached item: {msg.seq}"
                )
                return True
        return False
