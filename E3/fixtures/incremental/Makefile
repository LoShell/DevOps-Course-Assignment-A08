CC := gcc
CPPFLAGS := -Iinclude -DMODE=7
CFLAGS := -Wall -Wextra -O2
HEADERS := include/common.h include/config.h

.PHONY: all clean
all: bin/demo

bin/demo: build/main.o
	mkdir -p bin
	$(CC) $(CFLAGS) build/main.o -o bin/demo

build/main.o: src/main.c $(HEADERS)
	mkdir -p build
	$(CC) $(CPPFLAGS) $(CFLAGS) -c src/main.c -o build/main.o

clean:
	rm -rf build bin
