from pymavlink import mavutil

# Start a connection listening on a UDP port
conn = mavutil.mavlink_connection('udpin:localhost:14540')

conn.wait_heartbeat()

print(f"Heartbeat from system {conn.target_system} component {conn.target_component})")