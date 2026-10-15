CC = gcc
SRCS = klotski_test.c graph_find.c
INCLUDES = -Iincludes
LIBS = -lm
TARGET = klotski
CFLAGS = -O3 -fopenmp

$(TARGET): $(SRCS)
	$(CC) $(SRCS) $(CFLAGS) $(INCLUDES) $(LIBS) -o $(TARGET)
 
clean:
	rm -f $(TARGET)
 
.PHONY: clean
