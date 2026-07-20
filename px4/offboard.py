from common import *
import time

HertzToSeconds = lambda hertz : 1 / hertz

STREAM_RATE_HZ = 20
STREAM_RATE_SECONDS = HertzToSeconds(STREAM_RATE_HZ)

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component}")

  while True:
    setpoint_send(conn, 0, 0, 0)
    get_message(conn, message_names="POSITION_TARGET_LOCAL_NED", blocking=False)

    time.sleep(STREAM_RATE_SECONDS)