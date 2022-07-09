#include <iostream>
#include <string.h>
#include <vector>
#include <chrono>
#include <map>

using namespace std;

typedef struct user {
    char* user_name;
    int credit_card;
    int expire_date;
}User;

map<char*, User* > UM;
vector<char*> UV;
int UC;

void create_account(char* username, int credit_card, int expire_date){
    User new_user;
    new_user.credit_card = credit_card;
    new_user.expire_date = expire_date;
    new_user.user_name = username;

    UV.push_back(username);
    UM[username] = &new_user;
    UC++;
    printf("%s %d %d\n", username, UM[username] -> credit_card, UM[username] -> expire_date);
}

void update(char* username, int credit_card, int expire_date){
    User* us = UM[username];
    us -> credit_card = credit_card;
    us -> expire_date = expire_date;
}

void acrescenta(char* username, int credit_card, int expire_date){
    if (UM[username] != NULL)
        update(username, credit_card, expire_date);
    else{
        create_account(username, credit_card, expire_date);
    }
}

void consulta (char* user_name){
    if(UM[user_name] != NULL){
        int cc = UM[user_name] -> credit_card;
        printf("%d %d\n", user_name, cc, UM[user_name] -> expire_date);
    }
}

void listagem(){
    for(int i = 0; i < UC; i++){
        printf("%d %d\n", UM[UV[i]] -> credit_card, UM[UV[i]] -> expire_date);
    }
}

void input_handle(){
    char in[20];
    while(1){
        scanf("%s", in);
        if(strcmp(in,"ACRESCENTA") == 0){
            char* user;
            int cc, de;
            scanf("%s %d %d", &user, &cc, &de);
            acrescenta(user,cc,de);
        }else if( strcmp(in, "CONSULTA") == 0){
            char* user;
            scanf("%s", &user);
            consulta(user);
        }else if( strcmp(in, "LISTAGEM") == 0){
            listagem();
        }else if( strcmp(in, "APAGA") == 0){
            UC = 0;
            //free(UV);
            //free(UM);
        }else if(  strcmp(in, "FIM") == 0){
            return;
        }
    }
}

int main() {
    UC = 0;
    auto start = chrono::high_resolution_clock::now();

    input_handle();

    auto stop = chrono::high_resolution_clock::now();
    auto input = chrono::duration_cast<chrono::microseconds>(stop - start);
    cout << "time: " << input.count() << " μs\n";
    return 0;
}