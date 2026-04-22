CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 -shared -fPIC
TARGET = liboperations.so

all: $(TARGET)

$(TARGET): liboperations.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
