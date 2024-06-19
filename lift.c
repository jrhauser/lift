#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <time.h>
typedef struct nodes {
    int i;
    struct nodes* next;
} node;


typedef struct variables {
    node* in;
    node* out;
} var;

void substring(const char* string, char* substring, int start, int length);

int main(int argc, char* argv[]) {
    clock_t beginning = clock();
   // verify command line arguments
    if (argc != 2) {
        puts("Expected one argument, the path of the file containing the HCS");
        exit(1);
    }
    
    // open hornexfile
   FILE* hornexfile = fopen(argv[1], "r");
    if (hornexfile == NULL) {
        printf("Couldn't open hornexfile %s\n", strerror(errno));
        exit(1);
    }

    // open/create results file
    FILE* resultsFile = fopen("timing.csv", "ab+");
    if (resultsFile == NULL) {
        printf("Couldn't open hornexfile %s\n", strerror(errno));
        exit(1);
    }
    
    // declare input buffer
    char input[100];
    // read from hornexfile and  get number of variables
    fgets(input, 100, hornexfile);
    input[strcspn(input, "\n")] = '\0';
    char* token = strtok(input, " ");
    int var_count = atoi(token);
    
    // read from hornexfiles and get number of contraints
    fgets(input, 100, hornexfile);
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
        fgets(input, 100, hornexfile);
        // null terminate the input
        input[strcspn(input, "\n")] = '\0';
        // split the first line on the spaces, should give the first variable
        token = strtok(input, " ");
        
        // array for substrings
        char sub[10];

        // previous token so we know what came before the current token
        char* prev = NULL;
        // loop through the tokens, each constraint, variable, >=, or RHS
        while (token != NULL) {
            // check if the current token is a "-"
            if (strcmp(token, "-") == 0) {
                strcpy(prev, "-");
                token = strtok(NULL, " ");
                continue;
            // check for the right hand side and save it
            } else if (strcmp(token, ">=") == 0) {
                token = strtok(NULL, " ");
                b[i] = atoi(token);
            } else {
                // get the first char in the variable
                substring(token, sub, 1, 1);
                // if its the first variable
                 if (prev == NULL) {
                    if (strcmp(sub, "-") == 0) {    
                        // get the number of the variable and put it in the out list              
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
                    // The variable is negative
                    if (strcmp(prev, "-") == 0) {
                            // get the number of the variable
                            substring(token, sub, 2, 1);
                            
                            // insert the new index at the head of the out list
                            node* p = malloc(sizeof(node));
                            p->i = i;
                            p->next = arr[atoi(sub) - 1]->out;
                            arr[atoi(sub) - 1]->out = p;
                    // the variable is positive
                    } else if(strcmp(sub, "x") == 0) {
                            // get the number of the variable
                            substring(token, sub, 2, 1);

                            // insert the ne index at the head of in list
                            node* p = malloc(sizeof(node));
                            p->i = i;
                            p->next = arr[atoi(sub) - 1]->in;
                            arr[atoi(sub) - 1]->in = p;
                    } else {
                            printf("hornexfile invalid\n");
                    }
                }
            }
            token = strtok(NULL, " ");
        }
    }
    fclose(hornexfile);
    // allocate nodes for empty in or out list for each variable and store a -1 to indicate the list is empty
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

    clock_t startingAlgorithim = clock();
    // done with setup now time for the algorithim
    int neg = 0;
    for (int i = 0; i < con_count; i++) {
        if (b[i] < 0) {
            neg++;
        }
    }
    if (neg == con_count) {
        // system is feasibe all variables are 0
        //printf("System is feasible\n");
        //for (int i = 0; i < var_count; i++) {
           // printf("Var x%d is %d\n", i + 1, o[i]);
      // }
        
        clock_t zeroSolution = clock();
        fprintf(resultsFile, "0,");
        //From beginning to start of algortithim
        fprintf(resultsFile, "%f,", ((double)(startingAlgorithim - beginning))/CLOCKS_PER_SEC );
        // From start of algorithim to  solution 
        fprintf(resultsFile, "%f,", ((double)(zeroSolution - startingAlgorithim))/CLOCKS_PER_SEC );
        // total time
        fprintf(resultsFile, "%f\n", ((double)(zeroSolution - beginning))/CLOCKS_PER_SEC );

        fclose(resultsFile);
        return 0; 
    }
    // the meat of the algorithim outer for loop
    for (int r = 1; r < var_count + 1; r++) {
        // inner for loop
        for (int i = 0; i < var_count; i++) {
            // if the variable never appears positively we can continue without lifting
            if (arr[i]->in->i == -1) {
                continue;
            }
            
            // find the positive variable's biggest RHS
            node* f = arr[i]->in;           
            int c = b[f->i];
            while (f != NULL) {
                if (c < b[f->i]) {
                    c = b[f->i];
                }
                f = f->next;
            }
            // the lifting procedure
            if (c > 0) {
                // decrement all the places the variable appears positively
                node* p = arr[i]->in;
                while (p != NULL) {
                    b[p->i] -= c;
                    p = p->next;
                }
                // if the out list is empty, the variable never appears negatively, increment the output array by c and continue
                if (arr[i]->out->i == -1) {
                   o[i] += c; 
                   continue;
                }
                // increment all the places the variable appears negatively
                p = arr[i]->out;
                while (p != NULL) {
                    b[p->i] += c;
                    p = p->next;
                }
                // increment the output array by c and continue
                o[i] += c;
            }
        }
    }
    // if any constraint is still positive the system is infeasible
    for (int i = 0; i < con_count; i++) {
         if (b[i] > 0) {
            //printf("System is infeasible\n");
            clock_t infeasibleSolution = clock();

            fprintf(resultsFile, "0,");
            //From beginning to start of algortithim
            fprintf(resultsFile, "%f,", ((double)(startingAlgorithim - beginning))/CLOCKS_PER_SEC );
            // From start of algorithim to  solution 
            fprintf(resultsFile, "%f,", ((double)(infeasibleSolution - startingAlgorithim))/CLOCKS_PER_SEC );
            // total time
            fprintf(resultsFile,"%f\n", ((double)(infeasibleSolution - beginning))/CLOCKS_PER_SEC );
            fclose(resultsFile);
            return -1;
        }
    }
    // otherwise the system is feasible
  //  printf("System is feasible\n");
    //for (int i = 0; i < var_count; i++) {
        // print the output
       // printf("Var x%d is %d\n", i + 1, o[i]);
   // } 
    clock_t feasibleSolution = clock();

    fprintf(resultsFile, "1,");
    //From beginning to start of algortithim
    fprintf(resultsFile, "%f,", ((double)(startingAlgorithim - beginning))/CLOCKS_PER_SEC );
    // From start of algorithim to  solution 
    fprintf(resultsFile, "%f,", ((double)(feasibleSolution - startingAlgorithim))/CLOCKS_PER_SEC );
    // total time
    fprintf(resultsFile, "%f\n", ((double)(feasibleSolution - beginning))/CLOCKS_PER_SEC );
    fclose(resultsFile);
    return 0; 
}

// substring function
void substring(const char* string, char* substring, int start, int length) {
    int c = 0;
    while (c < length) {
        substring[c] = string[start + c - 1];
        c++;
    }
    substring[c] = '\0';
}
