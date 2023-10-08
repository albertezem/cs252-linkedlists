CC := "clang"
CFLAGS := "-gdwarf-4"
SRCS := "linkedlist.c main.c"

default:
	just --list

build:
	{{CC}} {{CFLAGS}} {{SRCS}} -o linkedlist

compile target:
	{{CC}} {{CFLAGS}} -c {{target}} -o {{trim_end_match(target, ".c")}}.o

clean:
	-rm *.o
	rm linkedlist
