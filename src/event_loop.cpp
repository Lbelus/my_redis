#include <iostream>
#include <sys/socket.h>
#include <string.h>
#include <poll.h>
#include <assert.h>


#ifndef CONN
#define CONN
struct Conn {
    int fd = -1;
    bool want_read = false;
    bool want_write = false;
    bool want_close = false;
    std::vector<uint8_t> incoming;
    std::vector<uint8_t> outgoing;
};
typedef struct Conn conn_t;
#endif


// utils;
char* itoa(int value, char* result, int base)
{
	// check that the base if valid
	if (base < 2 || base > 36) { *result = '\0'; return result; }
	char* ptr = result, *ptr1 = result, tmp_char = 0;
	int tmp_value;
	// Translating number to string with base and storing it:
	do
    {
		tmp_value = value;
		value /= base;
		*ptr++ = "zyxwvutsrqponmlkjihgfedcba9876543210123456789abcdefghijklmnopqrstuvwxyz" [35 + (tmp_value - value * base)];
	}
    while (value);
	// Apply negative sign
	if (tmp_value < 0) *ptr++ = '-';
	*ptr-- = '\0';
	
	my_revswap(ptr, ptr1, tmp_char);
	
	return result;
}

#define READ_SIZE_16 16
#define READ_SIZE_256 256

static die(const char* msg)
{
    char buffer[READ_SIZE_256] = {'\0'};
    char errno_str[READ_SIZE_16] = {'\0'};
    itoa(errno, errno_str, 10);
    strcpy(buffer, msg);
    strcat(buffer, ": [");
    strcat(buffer, errno_str);
    size_t size = strlen(buffer) + 1;
    write(STDERR_FILENO, buffer, size);
    abort();
}

int main(void)
{
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK,  0);  // or use fcntl if you are that guy
    if (fd < 0)
    {
        die("socket() failed");
    }

    int opt = 1;
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)))
    {
        die("setsockopt() failed");
    }

    // bind
    struct sockaddr_in addr = {};
    addr.sin_family = AF_INET;
    addr.sin_port = ntohs(1234)
    addr.sin_addr.s_addr = ntohl(0);
    int bind_retval = bind(fd, (const sockaddr *)&addr, sizeof(addr));
    if (bind_retval)
    {
        die("bind() failed");
    }
    // listen
    int listen_retval = listen(fd, SOMAXCONN);
    if (rv)
    {
        die("listen() failed");
    }
    
    std::vector<Conn *> fd2conn;
    std::vector<pollfd> poll_args;
    while (true)
    {
        poll_args.clear();
        poll_args.push_back({listen_fd, POLLIN, 0});
    
    }

    return EXIT_SUCCESS;
}
