#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
typedef struct nodes {
    int i;
    struct nodes* next;
} node;


typedef struct variables {
    node* in;
    node* out;
} var;

void substring(const char* string, char* substring, int start, int length);

int main(void) {
    
    // open file
   FILE* file = fopen("hornex2.txt", "r");
    if (file == NULL) {
        printf("couldn't open file %s\n", strerror(errno));
        exit(1);
    }
    // declare input buffer
    char input[100];
    // read from file and  get number of variables
    fgets(input, 100, file);
    input[strcspn(input, "\n")] = '\0';
    char* token = strtok(input, " ");
    int var_count = atoi(token);
    
    // read from files and get number of contraints
    fgets(input, 100, file);
    input[strcspn(input, "\n")] = '\0';
    token = strtok(input, " ");
    int con_count = atoi(token);


    // Output array
    int o[var_count];
    memset (o, 0, sizeof(o));
    // right hand sides
    int b[con_count];
    
    // variable array
    var* arr[var_count];
    
    

    // allocate var struct for each variable
    for (int i = 0; i < var_count; i++) {
        arr[i] = malloc(sizeof(var));
        // set in and out lists to null
        arr[i]->in = NULL;
        arr[i]->out = NULL;
    }
  // loop through the constraints
    for (int i = 0; i < con_count; i++) {
        // get the first line of constraints
        fgets(input, 100, file);
        // null terminate the input
        input[strcspn(input, "\n")] = '\0';
        // split the first line on the spaces, should give the first variable
        token = strtok(input, " ");
        
        // array for substrings
        char sub[10];
                char* prev = NULL;
        // loop through the tokens, each constraint, variable, >=, or RHS
        while (token != NULL) {
            // previous token so we know what came before the current token
            // check if the current token is a "-"
            if (strcmp(token, "-") == 0) {
                strcpy(prev, "-");
                token = strtok(NULL, " ");
                continue;
            } else if (strcmp(token, ">=") == 0) {
                token = strtok(NULL, " ");
                b[i] = atoi(token);
            } else {
                // get the first char in the variable
                substring(token, sub, 1, 1);
                // if its a negative variable
                 if (prev == NULL) {
                    if (strcmp(sub, "-") == 0) {                  
                        substring(token, sub, 3, 1);
                        node* p = malloc(sizeof(node));
                        p->i = i;
                        p->next = arr[atoi(sub) - 1]->out;
                        arr[atoi(sub) - 1]->out = p;
                        prev = malloc(1);
                        strcpy(prev, "x");
                    } else {
                        // get the number of the varioble
                        substring(token, sub, 2, 1);                        
                         // insert the new index at the head of the in list
                        node* p = malloc(sizeof(node));
                        p->i = i;
                        p->next = arr[atoi(sub) - 1]->in;
                        arr[atoi(sub) - 1]->in = p;
                        // copy the x into prev just to make it non-null
                        prev = malloc(1);
                        strcpy(prev, "x");
                    }
                // this is not the first variable                                                
                } else {
                    if (strcmp(prev, "-") == 0) {
                            substring(token, sub, 2, 1);
                            node* p = malloc(sizeof(node));
                            p->i = i;
                            p->next = arr[atoi(sub) - 1]->out;
                            arr[atoi(sub) - 1]->out = p;
                    } else if(strcmp(sub, "x") == 0) {
                            substring(token, sub, 2, 1);
                            node* p = malloc(sizeof(node));
                            p->i = i;
                            p->next = arr[atoi(sub) - 1]->in;
                            arr[atoi(sub) - 1]->in = p;
                    } else {
                            printf("File invalid\n");
                    }
                }
            }
            token = strtok(NULL, " ");
        }
    }

    for (int i = 0; i < var_count; i++) {
        node* p = malloc(sizeof(node)); 
        if (arr[i]->in == NULL) {
            
            p->i = -1;
            p->next = NULL;
            arr[i]->in = p;
        } else if (arr[i]->out == NULL) {
            p->i = -1;
            p->next = NULL;
            arr[i]->out = p;
        }
    }
    for (int r = 1; r < var_count - 1; r++) {
        for (int i = 0; i < var_count; i++) {
            if (arr[i]->in->i == -1) {
                continue;
            }
            
            node* f = arr[i]->in;           
            int c = b[f->i];
            while (f != NULL) {
                if (c < b[f->i]) {
                    c = b[f->i];
                }
                f = f->next;
            }
            if (c > 0) {
                node* p = arr[i]->in;
                while (p != NULL) {
                    b[p->i] -= c;
                    p = p->next;
                }
                if (arr[i]->out->i == -1) {
                   o[i] += c; 
                   continue;
                }
                p = arr[i]->out;
                while (p != NULL) {
                    b[p->i] += c;
                    p = p->next;
                }
                o[i] += c;
            }
        }
    }
    for (int i = 0; i < con_count; i++) {
         if (b[i] > 0) {
            printf("System is infeasible\n");
            return -1;
        }
    }
    printf("System is feasible\n");
    for (int i = 0; i < var_count; i++) {
        printf("Var x%d is %d\n", i + 1, o[i]);
    } 
    return 0; 
}


void substring(const char* string, char* substring, int start, int length) {
    int c = 0;
    while (c < length) {
        substring[c] = string[start + c - 1];
        c++;
    }
    substring[c] = '\0';
}
