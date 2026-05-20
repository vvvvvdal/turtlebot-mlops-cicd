.PHONY: install test run

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --log-cli-level=INFO

run:
	python3 src/ros2_turtlebot_node.py
