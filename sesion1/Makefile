CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11
TARGETS = 1-multiply_matrices
OBJ = 1-multiply_matrices.o functions.o

all: $(TARGETS)

$(TARGETS): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

1-multiply_matrices.o: 1-multiply_matrices.c
	$(CC) $(CFLAGS) -c $<

functions.o: functions.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(TARGETS) $(OBJ)