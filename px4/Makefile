all: px4-pymavlink

px4-pymavlink:
	python3 ./px4-pymavlink.py

tutorial:
	python3 ./mavlink_example.py

wireshark:
	cd ~/PX4-Autopilot/src/modules/mavlink/mavlink && \
	mavgen.py --lang=WLua --wire-protocol=2.0 \
		--output=mavlink_2_development message_definitions/v1.0/development.xml && \
	mkdir -p /home/ubuntu/.local/lib/wireshark/plugins && \
	cp ./mavlink_2_development.lua /home/ubuntu/.local/lib/wireshark/plugins && \
	rm ./mavlink_2_development.lua