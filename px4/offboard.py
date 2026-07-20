from common import *
import time

HertzToSeconds = lambda hertz : 1 / hertz

STREAM_RATE_HZ = 20
STREAM_RATE_SECONDS = HertzToSeconds(STREAM_RATE_HZ)

Armed = False

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component}")

  start = time.time()
  while True:
    elapsed = time.time() - start

    setpoint_send(conn, 0, 0, 0)
    get_message(conn, message_names="POSITION_TARGET_LOCAL_NED", blocking=False, printstd=False)

    if elapsed > 5 and not Armed:
      send_command(conn, mavutil.mavlink.MAV_CMD_DO_SET_MODE, confirmation=0,
                   param1=mavutil.mavlink.MAV_MODE_FLAG_GUIDED_ENABLED,
                   param2=0, param3=0, param4=0, param5=0, param6=0, param7=0)
      get_message(conn, message_names="COMMAND_ACK")
      
      Armed = True

    time.sleep(STREAM_RATE_SECONDS)
