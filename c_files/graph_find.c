#include <stdio.h>
#include <errno.h>
#include <string.h>

typedef struct Node{
    void* memory;
    struct Node *parent;
}Node;
typedef struct{
    void* state;
    int num_states;
}Output;

Output find_solution_old2(Output(*adjacent_states)(void*), bool(*goal_condition)(void*), void* start_state, int size_of_state){
    int step = 10;
    int node_making_child = 0;
    int next_node = 1;
    int node_list_size = step;
    Node *node_list = (Node*)malloc(step * sizeof(Node));
    if (node_list == NULL) {
        printf("Memory allocation failed.\n");
        exit(1);
    }
    node_list[0].memory = start_state;
    Output output;
    Node *parent;
    while (true){
        output = (*adjacent_states)((void*)&node_list[node_making_child]);
        for (int i = 0; i < output.num_states; i++){
            node_list[next_node].memory = output.state;
            node_list[next_node].parent = &node_list[node_making_child];
            if((*goal_condition)(node_list[next_node].memory)){
                void* min_path = malloc(node_making_child*sizeof(void*));
                if (min_path == NULL) {
                    printf("Memory allocation failed.\n");
                    exit(1);
                }
                min_path[0] = node_list[next_node].parent;
                parent = node_list[next_node].parent;
                for (int node = 1; node < next_node; node++){
                    if (&node_list[next_node-node] == parent){
                        parent = node_list[next_node-node].parent;
                        min_path[node] = node_list[next_node-node].memory;
                    }else{
                        free(node_list[next_node-node].memory);
                    }
                    return min_path;
                }
            }
            next_node++;
            if(next_node > node_list_size){
                node_list_size += step;
                node_list = realloc(node_list, node_list_size);
                if (node_list == NULL) {
                    printf("Memory allocation failed.\n");
                    exit(1);
                }
            }
        }
        free(output.state);
        node_making_child++;
    }
    Output meta_output = {min_path, node_making_child}
    return meta_output;
}
