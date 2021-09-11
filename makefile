all:
	make build && make install && make test

build:
	gcc lake.c -o lake

install:
	cp lake /sbin/ && cp lake.py /sbin/

test:
	touch lakefile && echo "all = lambda: {run('clear'), print('LaKe is installed!')}" > lakefile && lake
