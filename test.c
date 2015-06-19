#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "myemslarchive.h"

int main(int argc, char * argv[])
{
	if (argc > 1) //make sure that an id was passed in
	{
		if( checkisdigit(argv[1]))
		{
			char * arg = argv[1];
			int id = atoi(arg);
			char * filename = id2filename(id);
			printf("%s\n",filename);
		}
		else
		{
			printf("No valid integer passed in\n");
		}
	}
	else
	{
		printf("Incorrect Number of Arguments passed in, missing Id\n");
	}
	return 0;
}
