#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#include <arpa/inet.h>
#include <strings.h>
#include <string.h>
#include <sys/socket.h>

#define PORT 8080
#define SA struct sockaddr

#define REQUEST 1
#define GRANT 2
#define RELEASE 3

#define F 10

void *terminalThread(void *args) {
    bool loop_terminal = 1;
    do {
        int in;
        scanf("Input terminal: %d", &in);
        if (i == 1) {
            printf("a fila de pedidos atual");
        } else if (i == 2) {
            printf("quantas vezes cada processo foi atendido");
        } else if (i == 3) {
            pthread_cancel(args);
            loop_terminal = 0;
        }
    } while (loop_terminal == 1);
}

void *coordinatorThread(void *args) {
    int sockfd, connfd, len;
	struct sockaddr_in servaddr, cli;

	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd == -1) {
		printf("Erro ao criar o socket\n");
		exit(0);
	}
	bzero(&servaddr, sizeof(servaddr));

	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(PORT);

    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) {
		printf("Erro no bind\n");
		exit(0);
	}

    char message[F];
    char *msg, *prcs, *content
    bool loop = 1;
    int num;

    do {
        bzero(message, sizeof(message));
        if (recvfrom(sockfd, message, sizeof(message), 0,
            (SA*)&cli, sizeof(cli))) {
            printf("Erro ao receber mensagem\n");
            exit(0);
        }
        char * token = strtok(message, "|");
        msg = token;
        token = strtok(NULL, "|");
        prcs = token;
        token = strtok(NULL, "|");
        content = token;
        
    } while (loop == 1);
}

int main() {
    
}