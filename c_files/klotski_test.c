#include <stdio.h>
#include <stdlib.h>
#include "./graph_find.c"

#define g_num_blocks 10

typedef struct{
    int x[g_num_blocks];
    int y[g_num_blocks];
} State;
const State g_size = {{1,1,1,1,1,1,2,1,2,1}, {2,1,1,2,1,1,1,2,2,2}};

typedef struct{
    int x;
    int y;
} Board_dimensions;

Board_dimensions g_board_dimensions = {4,5};

int negative_to_zero(int a){
    if (a < 0) return 0;
    return a;
}

bool is_empty(State* node, int xcheck, int ycheck){
    for (int i = 0; i < g_num_blocks; i++){
        if (node->y[i] <= ycheck && node->x[i] <= xcheck && node->y[i] + g_size.y[i] > ycheck && node->x[i] + g_size.x[i] > xcheck){
            return false;
        }
    }
    return true;
}

Output all_possible_moves(void* node){
    (State*)node;
    State positions[8];
    int position_index = 0;
    bool empty_matrix[g_board_dimensions.y][g_board_dimensions.x];
    for (int y = 0; y < g_board_dimensions.y; y++){
        for (int x = 0; x < g_board_dimensions.x; x++){
            empty_matrix[y][x] = is_empty(node, x, y);
        }
    }
    for (int shape = 0; shape < g_num_blocks; shape++){
        if(node.x[shape] + g_size.x[shape] > g_board_dimensions.x){
            bool is_move_possible = true;
            for (int i = 0; i < g_size.y[shape]; i++){
                if (!is_empty(node, node.x[shape]+i, node.y[shape]+g_size.y[shape])){
                    is_move_possible = false;
                    break;
                }
            }
            if(is_move_possible{
                positions[position_index] = node;
                positions[position_index][shape].y++;
                position_index++;
            })
        }
        if(node.y[shape] + g_size.y[shape] > g_board_dimensions.y){
            bool is_move_possible = true;
            for (int i = 0; i < g_size.x[shape]; i++){
                if (!is_empty(node, node.y[shape]+g_size.x[shape], node.x[shape]+i)){
                    is_move_possible = false;
                    break;
                }
            }
            if(is_move_possible{
                positions[position_index] = node;
                positions[position_index][shape].x++;
                position_index++;
            })
        }
        if(node.y < 0){
            bool is_move_possible = true;
            for (int i = 0; i < g_size.y; i++){
                if(!is_empty(node, node.x[shape]+i, node.y[shape]-1)){
                    is_move_possible = false;
                    break;
                }
            }
            if(is_move_possible){
                positions[position_index] = node;
                positions[position_index][shape].y--;
                position_index++;
            }
        }
        if(node.x < 0){
            bool is_move_possible = true;
            for (int i = 0; i < g_size.x; i++){
                if(!is_empty(node, node.y[shape]-1, node.x[shape]+i)){
                    is_move_possible = false;
                    break;
                }
            }
            if(is_move_possible){
                positions[position_index] = node;
                positions[position_index][shape].y--;
                position_index++;
            }
        }
    }
    Output output;
    output.state = malloc(position_index * sizeof(State));
    output.num_states = position_index;
    return output;
}

int main(void){
    State start_node = {{0,1,2,3,1,2,1,0,1,3}, {0,0,0,0,1,1,2,3,3,3}}; 
    for (int y = 4; y>-1; y--){
        for (int x = 0; x<4; x++){
            bool empty = is_empty(&start_node, x, y);
            printf("%d ", empty);
        }
        printf("\n");
    }
    return 0;
}