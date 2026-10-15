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

// void* find_solution_old2(Output(*adjacent_states)(Output), bool(*goal_condition)(void*), void* start_state, int size_of_state){
//     int step = 10;
//     int node_making_child = 0;
//     int next_node = 1;
//     int node_list_size = step;
//     Node *node_list = (Node*)malloc(step * sizeof(Node));
//     if (node_list == NULL) {
//         printf("Memory allocation failed.\n");
//         exit(1);
//         return NULL;
//     }
//     node_list[0].memory = start_state;
//     Output output;
//     Node *parent;
//     while (true){
//         output = (*adjacent_states)(node_making_child);
//         for (int i = 0; i < output.num_states; i++){
//             node_list[next_node].state = output.state;
//             node_list[next_node].parent = &node_making_child;
//             if((*goal_condition)(node_list[next_node].state)){
//                 void* min_path = malloc(node_making_child*sizeof(*void));
//                 if (min_path == NULL) {
//                     printf("Memory allocation failed.\n");
//                     exit(1);
//                     return NULL
//                 }
//                 min_path[0] = node_list[next_node].state;
//                 parent = node_list[next_node].parent;
//                 for (int node = 1; node < next_node; node++){
//                     if (node_list[next_node-node] == parent){
//                         parent = node_list[next_node-node].parent;
//                         min_path[node] = node_list[next_node-node].state;
//                     }else{
//                         free(node_list[next_node-node]);
//                     }
//                     return min_path;
//                 }
//             }
//             next_node++;
//             if(next_node > node_list_size){
//                 node_list_size += step;
//                 node_list = realloc(node_list_size);
//                 if (node_list == NULL) {
//                     printf("Memory allocation failed.\n");
//                     exit(1);
//                     return NULL
//                 }
//             }
//         }
//         node_making_child++;
//     }
// }
// *void find_solution_old1(Output(*adjacent_states)(*Node), bool(*goal_condition)(*void), *void start_state, int size_of_state){
//     int step = 10;
//     int node_making_child = 0;
//     int next_node = 1;
//     int node_list_size = step;
//     Node *node_list = (*Node)malloc(step * sizeof(*Node));
//     *node_list[0] = Node;
//     *node_list[0].memory = start_state;
//     Output output;
//     Node *parent;
//     while (true){
//         output = (*adjacent_states)(node_making_child);
//         for (int i = 0; i < output.num_states; i++){
//             node_list[next_node] = output.state + size_of_state*i;
//             if((*goal_condition)((*node_list[next_node]).state)){
//                 void* min_path = malloc(node_making_child*sizeof(*void));
//                 min_path[0] = (*node_list[next_node]).state;
//                 parent = (*node_list[next_node]).parent;
//                 for (int node = 0; node > next_node; node++){
//                     if (node_list[next_node-node] == parent){
//                         parent = (*node_list[next_node-node]).parent;
//                         min_path[node] = (*node_list[next_node-node]).state;
//                     }else{
//                         free(node_list[next_node-node]);
//                     }
//                     return min_path;
//                 }
//             }
//             next_node++;
//             if(next_node > node_list_size){
//                 node_list_size+=step;
//                 node_list = realloc(node_list_size);
//             }
//         }
//         node_making_child++;
//     }
// }
// Output find_solution_old0(*Output(*all_possible_moves_function)(*Node), bool(*goal_condition)(*void), *void start_node){
//     Output *output;
//     int step = 10;
//     int num_nodes = 1;
//     int current_node = 0;
//     int memory = step;
//     Node* node_list = (*Node)malloc(step * sizeof(*Node));
//     node_list[0] = *Node;
//     node_list[num_nodes].memory = start_node;
//     while (true){
//         output = (*all_possible_moves_function)(node_list[current_node]);
//         for (int i = 0; i < output.state_memory_size; i++){
//             num_nodes++;
//             node_list[num_nodes] = *Node;
//             node_list[num_nodes].memory = *(&output+i).state;
//             node_list[num_nodes].parent = output[i].state;
//             // node_list[num_nodes].memory = output[i].state;
//             // node_list[num_nodes].parent = output[i].state;
//             if (memory == num_nodes+1){
//                 memory+=step;
//                 node_list* = (Node*)realloc(memory + step * sizeof(Node*));
//             }
//             if ((*goal_condition)(output.state)){
//                 void* min_path = malloc(current_node * sizeof(void*));
//                 Output temporary = output;
//                 for (int j = 0; j > current_node; j++){
//                     min_path[node_list] = temporary.state;
//                     temporary = *temporary.parent;
//                 }
//                 free(node_list);
//                 return min_path;
//             }
//         }
//         current_node++;
//     }
// } 

// umjetnost je sve u što je uloženo više truda nego što je potrebno (uključujući i ideju) za ostvariti svrhu ili korist tog predmeta