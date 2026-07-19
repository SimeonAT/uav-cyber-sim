all: mission

mission:
	python3 ./mission.py

offboard:
	python3 ./offboard.py

wireshark:
	cd ~/PX4-Autopilot/src/modules/mavlink/mavlink && \
	mavgen.py --lang=WLua --wire-protocol=2.0 \
		--output=mavlink_2_development message_definitions/v1.0/development.xml && \
	echo 'udp_dissector_table:add(14540, mavlink_proto)' >> mavlink_2_development.lua && \
	mkdir -p /home/ubuntu/.local/lib/wireshark/plugins && \
	cp ./mavlink_2_development.lua /home/ubuntu/.local/lib/wireshark/plugins && \
	rm ./mavlink_2_development.lua