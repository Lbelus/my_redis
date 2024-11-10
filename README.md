# Welcome to My Cpp redis server
***

## Task


## Description


## Installation

### Step 1. setup the Environment.
Using docker.

- Create a docker network:
```bash
docker network create redis_network
```

From the ``project root`` dir.
- Build the image:
```bash
docker build -t redis_cxx_img .
```

- Then run the container:
```bash
docker run -it --network redis_network -v .:/workspace/ --name redis_cxx_cont redis_cxx_img
```


### The Core Team
* [Lorris BELUS](//github.com/Lbelus) - Developer
