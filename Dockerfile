FROM ubuntu:24.04

# Set environment variables to non-interactive
ENV DEBIAN_FRONTEND=non-interactive

# Update package list and install essential packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    llvm-14 llvm-14-dev \
    clang \
    nasm \
    cmake \
    pkg-config \
    git \
    wget \
    unzip \
    curl \
    lua5.4 \
    python3

# Clean up to reduce image size
RUN   apt-get autoremove -y && \
      apt-get clean && \
      rm -rf /var/lib/apt/lists/*

# installing hiredis, might end managing RESP myself
RUN git clone https://github.com/redis/hiredis.git && \
    cd hiredis && \
    make && \
    make install && \
    ldconfig

# Install google-test
RUN wget -O google-test.zip https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip && \
    unzip google-test.zip && \
    cd googletest-* && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    cd ../../ && \
    rm -rf google-test.zip googletest-*

# Reset environment variable
ENV DEBIAN_FRONTEND=

# Set the working directory
WORKDIR /workspace

# Set the default command
CMD ["bash"]
