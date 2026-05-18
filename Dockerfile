FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip \
    iputils-ping \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install ollama opencv-python

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

WORKDIR /ros_workspace