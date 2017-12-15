#include <stdio.h>
#include<stdlib.h>
#include<string.h>

#define MAXBUF 100

char * bin_operator(char * input_op);

int main(void)
{
    char name[MAXBUF];
    char formula[MAXBUF];
    char filename[MAXBUF];
    char *token;
    char * operators[MAXBUF];
    int counter =0;
    FILE *fptr;

    scanf("%s = %[^\n]", name, formula);
    printf("%s\n", name);
    printf("%s\n", formula);
    
    strcpy(filename, name);
    fptr = fopen(strcat(filename, ".hdl"), "w");
    fprintf(fptr, "CHIP ");
    fprintf(fptr, "%s", name);
    fprintf(fptr, "{\n");
    
    /*
    token = strtok(formula, " ");
    while (token != NULL){
        printf("%s\n", token);
        if (bin_operator(token) != NULL){
            operators[counter] = token;
            counter +=1; 
        }
        token = strtok(NULL, " ");
    }
    printf("counter : %d\n", counter);
    */
    int index= 0;
    token = formula+ index;
    while (token != NULL) {
        if (bin_operator(token) != NULL) {
            operators[counter] = token;
            counter +=1;
        }
        token = formula + index + 1;
    }

    for (int i =0; i<counter; i++){
        printf("ops : %s\n", *(operators+i));
    }
    

    fprintf(fptr, "}\n");
    fclose(fptr);


    return 0;
}


char * bin_operator(char *input_op){
    char *op = (char *) malloc(100);
    char OR = '+';
    char AND = '*';
    char IMP[] = "->";
    char NOT = '~';

    if (*input_op== OR){
        printf("Operation is OR\n");
        strcpy(op, "OR");
    }
    else if (*input_op == AND){
        printf("Operation is AND\n");
        strcpy(op, "AND");
    }
    else {
        //strcpy(op, "ERROR");
        return NULL;
    }
    return op;
}
