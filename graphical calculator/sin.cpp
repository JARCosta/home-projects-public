#include <iostream>
#include <vector>
#include <sys/ioctl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

using namespace std;


int main() {

    int columns;
    int pointer;

    struct winsize w;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);
    columns = w.ws_col;
    printf ("terminal lines %d\n", w.ws_row);
    printf ("terminal columns %d\n", w.ws_col);
    
    char start;
    printf("ready to start? ");
    start = getchar();
    if(start != 'y') return 0;

    pointer = 0;
    bool up = true;
    while(1){
        if(pointer == columns || pointer == -1) up = !up;
        if(up) pointer++;
        else pointer--;
        usleep(10000);
        char line[columns];
        memset(line,' ',columns);
        for(int i = 0; i < pointer; i++){
            line[i] = 'B';
        }

        printf("%s\n",line);
    }
    cout << "\n";
    return 0;
}