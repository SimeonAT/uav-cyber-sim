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

jinja:
	python3 ./jinja.py

# A zombie (Z-state) process is already dead — it's just waiting
# for its parent to call wait()/reap it. `kill -9` on a zombie
# PID does nothing, since there's no running code left to signal.
# `kill-sim` below kills the *live* px4/gzserver/gzclient/proxy/
# logic processes so they stop accumulating further zombies.
# Existing zombies only clear once their parent (almost
# certainly the Jupyter kernel, per the notebook-based dev loop)
# either reaps them or exits — if `zombies` still shows a
# nonzero count after `kill-sim`, restart the kernel next.
#
# All of the code below, along with this comment, was written by Claude AI (Anthropic).

clean-processes: kill-sim zombies clean ports

# Kill all live (non-zombie) sim-related processes.
kill-sim:
	-pkill -9 -f "bin/px4"
	-pkill -9 -f "gzserver"
	-pkill -9 -f "gzclient"
	-pkill -9 -f "simulator.proxy"
	-pkill -9 -f "simulator.logic"
	@echo "Killed live px4/gzserver/gzclient/proxy/logic processes (if any were running)."

# Report current zombie count, grouped by process name, so you can tell
# whether a kernel restart actually cleared them.
zombies:
	@echo "Zombie process count by name:"
	@ps aux | awk '$$8 ~ /Z/ {print $$11}' | sort | uniq -c | sort -rn

# Report what's actually bound on the ports this project cares about.
# Falls back to /proc if neither ss nor lsof is installed.
ports:
	@echo "Checking 4560 / 14540-14549 / 14580-14589 ..."
	@if command -v ss >/dev/null 2>&1; then \
		sudo ss -tulnp | grep -E "4560|1454[0-9]|1458[0-9]" || echo "Nothing bound."; \
	elif command -v lsof >/dev/null 2>&1; then \
		sudo lsof -i -P -n | grep -E "4560|1454[0-9]|1458[0-9]" || echo "Nothing bound."; \
	else \
		echo "Neither ss nor lsof installed — install one with:"; \
		echo "  sudo apt update && sudo apt install -y iproute2   # for ss"; \
		echo "  sudo apt update && sudo apt install -y lsof       # for lsof"; \
	fi

# Full cleanup pass: kill live processes, then report what's left.
clean: kill-sim
	@sleep 1
	@$(MAKE) zombies
	@echo ""
	@echo "If zombie count above is still nonzero, restart the Jupyter kernel —"
	@echo "zombies only clear when their parent process reaps or exits."