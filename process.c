#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#include <arpa/inet.h>
#include <strings.h>
#include <sys/socket.h>

#define PORT 8080
#define SA struct sockaddr

#define REQUEST 1
#define GRANT 2
#define RELEASE 3

#define F 10