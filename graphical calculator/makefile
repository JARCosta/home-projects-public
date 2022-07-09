CC=g++
CFLAGS=-Wall -Wextra -Werror -ansi -pedantic -g -o sin
all:: sin 
	$(MAKE) $(MFLAGS) -C tests
soma: sin.cpp
clean::
	rm -f sin a.out *.o core tests/*.diff
