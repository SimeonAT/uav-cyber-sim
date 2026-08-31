"""Utility functions for MAVLink connections and messaging."""
#
# Import ENU/GRA only for type checkers, not at runtime, to avoid a circular import: 
# simulator.helpers.coordinates imports MAVConnection from this package, so importing
# coordinates back at module load time would try to import this file while it's still 
# mid-initialization.
#
# Authored by Claude (Sonnet 5), Anthropic, August 2026.
#
from __future__ import annotations
from typing import Literal, cast, TYPE_CHECKING
if TYPE_CHECKING:
    from simulator.helpers.coordinates import ENU, GRA

import logging
import time
from typing import Literal, cast

from pymavlink import mavutil

from simulator.helpers.connections.mavlink.customtypes.mavconn import MAVConnection
from simulator.helpers.connections.mavlink.enums import (
  Autopilot, Type, 
  Frame, MsgID
)


def connect(device: str, src_sysid: int, src_compid: int) -> MAVConnection:
    """
    Wrap `mavlink_connection` with a type cast to `MAVConnection`
    to enable clean static typing.
    Pass source_system and source_component to ensure correct sysid assignment.
    """
    return cast(
        MAVConnection,
        mavutil.mavlink_connection(  # type: ignore[arg-type]
            device, source_system=src_sysid, source_component=src_compid
        ),
    )


# taken from mavproxy
def send_heartbeat(
    conn: MAVConnection,
    sys_type: Type = Type.ONBOARD_CONTROLLER,
    ardupilot: Autopilot = Autopilot.GENERIC,
) -> None:
    """Send a GCS heartbeat message to the UAV."""
    # Set the source system ID for this connection
    conn.mav.heartbeat_send(sys_type, ardupilot, 0, 0, 0)

""" Sends MAVLink command to instruct PX4 to move UAV to the next global waypoint.
    Used to stream next waypoint to PX4 to enable the use of offboard (i.e. guided) mode.
    https://docs.px4.io/main/en/flight_modes/offboard#technical-summary

    To accomplish this task, this function's implementation is a modified version of
    `exec_fn` in `planners/action/navigation.py`.
"""
def send_setpoint(conn: MAVConnection, enu_wp: ENU, origin: GRA, type_mask: int) -> None:
  gra_wp = origin.to_abs(enu_wp)
  go_msg = mavutil.mavlink.MAVLink_set_position_target_global_int_message(
      10,
      conn.target_system,
      conn.target_component,
      Frame.GLOBAL_INT,
      type_mask,
      *gra_wp.to_global_int_alt_in_meters(),
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
  )
  conn.mav.send(go_msg)
  return


def create_udp_conn(
    base_port: int,
    offset: int,
    mode: Literal["receiver", "sender"],
    src_sysid: int,
    src_compid: int,
) -> MAVConnection:
    """Create a MAVLink-over-UDP connection."""
    port = base_port + offset
    if mode == "receiver":
        conn = connect(f"udp:127.0.0.1:{port}", src_sysid, src_compid)  # recv+send
        conn.wait_heartbeat()
    else:  # mode == "sender"
        conn = connect(f"udpout:127.0.0.1:{port}", src_sysid, src_compid)  # send-only
    return conn


def create_tcp_conn(
    base_port: int,
    offset: int,
    src_sysid: int,
    src_compid: int,
    role: Literal["client", "server"],
    sys_type: Type = Type.ONBOARD_CONTROLLER,
    ardupilot: Autopilot = Autopilot.GENERIC,
    retry_window: float = 15.0,
) -> MAVConnection:
    """Create and in or out connection and wait for geting the hearbeat in."""
    port = base_port + offset
    device_str = f"tcp{'in' if role == 'server' else ''}:127.0.0.1:{port}"
    is_client = role == "client"

    attempt = 0
    start_time = time.time()
    while True:
        attempt += 1
        try:
            conn = connect(device_str, src_sysid, src_compid)
            conn.mav.heartbeat_send(sys_type, ardupilot, 0, 0, 0)
            conn.wait_heartbeat()

            logging.info("Heartbeat from system (system %u component %u) for %s" % 
                        (conn.target_system, conn.target_component, device_str))
            return conn
        except Exception as e:
            if not is_client:
                logging.error(f"Failed to create TCP connection on port {port}: {e}")
                raise

            elapsed = time.time() - start_time
            remaining = retry_window - elapsed
            if remaining <= 0:
                logging.error(
                    f"Failed to create TCP connection on port {port} after "
                    f"{attempt} attempts: {e}"
                )
                raise e

            backoff = min(0.1 * attempt, 0.5, remaining)
            logging.warning(
                f"TCP client connection to port {port} failed (attempt {attempt}): {e}."
                f" Retrying in {backoff}"
            )
            time.sleep(backoff)
