# Welcome to My Cpp redis server
***

## Task


## Description

```md

1. TCP Server
    1.1 Socket communication
    1.2 Connections and requests
    1.3 Concurrency and connection termination
2. Protocol (RESP)
    2.1 RESP request parsing and response encoding
    2.2 Validation and error responses
3. Event Loop
    3.1 Event scheduling and handler setup
    3.2 TCP server integration for request management
4. Data Structures
    4.1 Sorting Structures
    4.2 AVL Tree, Treap, Trie, B-Tree, and Log (implement and test each)
    4.3 Hashing Structures
    4.4 Open Addressing and Chaining (implement and test each)
5. Serialization
    5.1 Serialization and deserialization of data
6. Memory Management
    6.1 Memory allocation and cleanup strategies
7. Persistence
    7.1 Data snapshotting or periodic writes to disk
    7.2 Data recovery on server restart
8. Testing Suite
    8.1 Unit and integration tests
    8.2 Edge case handling and stress testing
```
## RESP protocol
RESP data type |    Cat    | First byte |
************** | ********* | ********** |
simple str     | simple    |     +      |
simple err     | simple    |     -      |
integer        | simple    |     :      |
Bulk str       | aggregate |     $      |
Arrays         | aggregate |     *      |
Nulls          | simple    |     -      |
Booleans       | simple    |     #      |
Doubles        | simple    |     ,      |
Big numbers    | simple    |     (      |
Bulk errors    | aggregate |     !      |
verbatim str   | aggregate |     =      |
Maps           | aggregate |     %      |
Attributes     | aggregate |     `      |
Sets           | aggregate |     ~      |
Pushes         | aggregate |     >      |




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
