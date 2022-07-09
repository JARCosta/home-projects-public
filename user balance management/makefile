CC=g++
CFLAGS=-Wall -Wextra -Werror -ansi -pedantic -g -o main
all:: main 
	$(MAKE) $(MFLAGS) -C tests
soma: main.cpp
clean::
	rm -f main a.out *.o core tests/*.diff
