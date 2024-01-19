#include <stdlib.h>
#include <stdio.h>

struct node{
    struct node* next;
    char value;
    struct state* key;

};
struct state{
    struct node* transitions;
    char name;
    char acept_state; //es un booleano, para saber si es estado de aceptacion o no;
};
void insertTran(struct node** transitions, char tranname, struct state* newstate){
    struct node* current = *transitions;
    struct node* newtransition = (struct node*)malloc(sizeof(struct node));
    newtransition->next = NULL;
    newtransition->value = tranname;
    newtransition->key = newstate;
    while(current->next){
        current->next;
    }
    current->next = newtransition;
}

void insertState(struct state** stateq, char tranname, char is_acept){//se pasa el estado donde le vamos a agregar y lo que pasa con la transicion
    struct state* newstate = (struct state*)malloc(sizeof(struct state));
    struct node* newtransition = (struct node*)malloc(sizeof(struct node));
    newtransition->next = NULL;
    newtransition->value = 0;
    newtransition->key = NULL;
    
    newstate->transitions = newtransition;
    newstate->name = 0; //aun no se si le seguire poniendo nombre
    newstate->acept_state = is_acept;
    if(*stateq){
        *stateq = newstate;
        return;
    }
    insertTran(&((*stateq)->transitions), tranname, newstate);
}
void PrintS(struct state * pstate){
    printf("%c",pstate->name);
    struct node* current = pstate->transitions;
    while(current){
        printf("%c", current->value);
        current = current->next;
    }

}

int main(){
    struct state* estado = NULL; //TODO 
    insertState(&estado, 'a', 0);
    PrintS(estado);
    return 0;
}
