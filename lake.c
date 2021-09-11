#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char const *argv[]) {
	unsigned char buffer_size = strlen("python3 /sbin/lake.py");
	for (unsigned char i = 1; i < argc; ++i) buffer_size += strlen(argv[i]) + 1;

	char* buffer = malloc(buffer_size);
	if (buffer == NULL) {
		puts("malloc returned null!");
		return -1;
	}

	strcpy(buffer, "python3 /sbin/lake.py");
	for (unsigned char i = 1; i < argc; ++i) {
		strcat(buffer, " ");
		strcat(buffer, argv[i]);
	}

	return system(buffer);
}
