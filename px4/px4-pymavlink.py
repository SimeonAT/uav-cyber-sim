from pymavlink import mavutil
import mavtest

ONBOARD_PORT = 14540

# Start a connection listening on a UDP port
conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

conn.wait_heartbeat()
print(f"Heartbeat from system {conn.target_system} component {conn.target_component})")