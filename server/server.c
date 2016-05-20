//##############################################################
//# Authors: Christine Hwang (ch458) and Tania Tocalini (tvt9)
//# Date:    5-18-2016
//# Project: Lost and Found
//# Summary: This is a simple server created using sockets.       
//################################################################
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 10102

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

void sigint_handler(int sig)
{
    printf(0, "Ahhh! SIGINT!\n", 14);
}

int main(int argc, char *argv[])
{
     int sockfd, newsockfd;
     socklen_t clilen;
     char buffer[256];
     struct sockaddr_in serv_addr, cli_addr;
     int n;
     FILE *fifo;
     struct sigaction sa;

     sa.sa_handler = sigint_handler;
     sa.sa_flags = 0; // or SA_RESTART
     sigemptyset(&sa.sa_mask);

     sockfd = socket(AF_INET, SOCK_STREAM, 0);

     if (sockfd < 0)
        error("ERROR opening socket");

     bzero((char *) &serv_addr, sizeof(serv_addr));
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(PORT);

     if (bind(sockfd, (struct sockaddr *) &serv_addr,
              sizeof(serv_addr)) < 0)
              error("ERROR on binding");

     printf("%s\n", (struct sockaddr *) &serv_addr);

     listen(sockfd,5);
     clilen = sizeof(cli_addr);
     newsockfd = accept(sockfd,
                 (struct sockaddr *) &cli_addr,
                 &clilen);

     if (newsockfd < 0)
          error("ERROR on accept");

     bzero(buffer,256);
     while (1) {
       memset(buffer, 0, 256);
       n = read(newsockfd,buffer,255);

       if (sigaction(SIGINT, &sa, NULL) == -1) {
         close(newsockfd);
         close(sockfd);
         perror("sigaction");
         exit(1);
       }

       if (n < 0) {
         error("ERROR reading from socket");
         close(newsockfd);
         close(sockfd);
       }

       fifo = fopen("/home/pi/rssi-raspi/rssi", "a");

       printf("Here is the message: %s\n",buffer);
       fprintf(fifo, "%s", buffer);
       fclose(fifo);

       //n = write(newsockfd,"I got your message",18);
       //if (n < 0) error("ERROR writing to socket");
     }
     close(newsockfd);
     close(sockfd);
     return 0;
}

