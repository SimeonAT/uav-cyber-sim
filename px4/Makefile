PX4_AUTOPILOT_PATH ?= $(HOME)/PX4-Autopilot
PX4_BUILD_DIR := $(PX4_AUTOPILOT_PATH)/build/px4_sitl_default

all: offboard

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

build-px4-only:
	ninja -C $(PX4_BUILD_DIR) px4
	@test -f $(PX4_BUILD_DIR)/bin/px4 && \
	  echo "bin/px4 built successfully at $(PX4_BUILD_DIR)/bin/px4" || \
	  (echo "bin/px4 missing after build - link step likely failed" && exit 1)

start-px4:
	$(PX4_BUILD_DIR)/bin/px4 $(PX4_BUILD_DIR)/etc