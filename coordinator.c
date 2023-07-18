#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#include <pthread.h>

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

struct cancelStruct {
    pthread_t listen;
    pthread_t coordinate;
};

pthread_mutex_t mutex_queue = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_file = PTHREAD_MUTEX_INITIALIZER;

char requestQueue[100];

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
            struct cancelStruct *cS = args;
            pthread_cancel(cS->coordinate);
            pthread_cancel(cS->listen);
            loop_terminal = 0;
        }
    } while (loop_terminal == 1);
}

void *coordinatorListener(void *args) {
    int sockfd;
	struct sockaddr_in servaddr, cli;

	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd == -1) {
		printf("Erro ao criar o socket\n");
		exit(0);
	}
	bzero(&servaddr, sizeof(servaddr));

	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	servaddr.sin_port = htons(PORT);

    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) {
		printf("Erro no bind\n");
		exit(0);
	}

    char message[F];
    char *msg, *prcs, *content;
    bool loop_listen = 1;
    int num;

    do {
        bzero(message, sizeof(message));
        if (recvfrom(sockfd, message, sizeof(message), 0, (SA*)&cli, sizeof(cli))) {
            printf("Erro ao receber mensagem\n");
            exit(0);
        }
        char * token = strtok(message, "|");
        msg = token;
        token = strtok(NULL, "|");
        prcs = token;
        token = strtok(NULL, "|");
        content = token;
        if (msg == "1") {
            // REQUEST
            pthread_mutex_lock(&mutex_queue);
            // Adicionar mensagem à queue
            // Salvar informações da struct cli e do inteiro sockfd para recuperar o processo cliente
            pthread_mutex_unlock(&mutex_queue);
        }
        if (msg == "3") {
            // RELEASE
            pthread_mutex_unlock(&mutex_file);
        }
        
    } while (loop_listen == 1);
}

void *coordinatorManager(void *args) {
    bool loop_coordinator = 1;

    char message[F];

    int sockfd;
	struct sockaddr_in cli;
    do {
        pthread_mutex_lock(&mutex_queue);
        // ler mensagens na queue e retirar da queue
        pthread_mutex_unlock(&mutex_queue);
        // buscar informação de cli e de sockfd
        bzero(message, sizeof(message));
        // envia mensagem ao cliente
        // manipular message para que seja GRANT
        if (sendto(sockfd, message, sizeof(message), 0, (SA*)&cli, sizeof(cli)) < 0){
            printf("Can't send\n");
            return -1;
        }
    } while (loop_coordinator == 1);
}

int main() {
    pthread_t terminal, listen, coordinate;

    pthread_create(&listen, NULL, &coordinatorListener, NULL);
    pthread_create(&coordinate, NULL, &coordinatorManager, NULL);

    struct cancelStruct cS;
    cS.listen = listen;
    cS.coordinate = coordinate;

    pthread_create(&terminal, NULL, &terminalThread, (void *)&cS);
}