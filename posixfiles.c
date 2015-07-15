#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

#define PREFIX "/home/chrisExamples/"
/*! \brief Gets a file from a Posix style file structure
*
*
* Opens the file specified in the id parameter.  (prefixed with config option).  Then
* opens the file contents with the FILE* . Will return the number of bytes read. 
* If an error occurs, errno will be set and -1 will be returned.
* 
*/
int posix_get_file(FILE* file, int id)
{
	char * filename;
	int sz;
	int totalBytesRead = 0;
	char buffer[2048]; //used to read the file in chunks
	int iterationBytesRead = 0;
	int errsv;

	//get the size of the filepath string, and set it
	sz = snprintf(NULL, 0, "%s%d", PREFIX,id);
	if( sz < 0)
	{
		//error state, errno was set from snprintf
		return -1;
	}

	filename = (char *)malloc(sz + 1);
	if(filename == NULL)
	{
		//error occured with allocating memory, errno set from the malloc call
		return -1;
	}

	sz = snprintf(filename, sz+1, "%s%d", PREFIX,id);
	if( sz < 0)
	{
		//error state, errno was set from snprintf
		errsv = errno;
		free(filename);
		errno = errsv;
		return -1;
	}

	file = fopen(filename,"r");
	errsv = errno;
	free(filename);
	if(file == NULL)
	{
		//errno is set by fopen returning NULL. Saved in errsv so set errno back to that
		//in case it was changed by free call.
		errno = errsv;
		return -1; //ext method
	}

	//read whole file until you reach end
	while (!feof(file))
	{
		iterationBytesRead = fread(buffer, 1, (sizeof buffer)-1, file);

		if(ferror(file)) //an error occured with fread
		{
			errsv = errno; //want to save the real error across library calls
			fclose(file);
			errno = errsv;
			return -1; //return error
		}

		totalBytesRead += iterationBytesRead; //sum the total bytes read if some were read
	}

	fclose(file);


	return totalBytesRead;
}

/*! \brief Puts contents into a file from a Posix style file structure
*
*
* Opens the file specified in the id parameter for writing.  (prefixed with config option).  Then
* writes file contents with the FILE* . Will return the number of bytes written. 
* If an error occurs, errno will be set and -1 will be returned.
*
*/
int posix_put_file(FILE* file, int id)
{
	char * filename;
	int sz;
	int totalBytesWritten = 0;
	char buffer[2048]; //used to read the file in chunks
	int errsv;

	//strncpy(buffer, "This is a test string!", sizeof(buffer));
	sz = snprintf(NULL, 0, "This is a test string!");
	snprintf(buffer, sz+1, "This is a test string!");
	//get the size of the filepath string, and set it
	sz = snprintf(NULL, 0, "%s%d", PREFIX,id);
	if( sz < 0)
	{
		//error state, errno was set from snprintf
		return -1;
	}

	filename = (char *)malloc(sz + 1);
	if(filename == NULL)
	{
		//error occured with allocating memory, errno set from the malloc call
		return -1;
	}

	sz = snprintf(filename, sz+1, "%s%d", PREFIX,id);
	if( sz < 0)
	{
		//error state, errno was set from snprintf
		errsv = errno;
		free(filename);
		errno = errsv;
		return -1;
	}
	file = fopen(filename,"w");
	errsv = errno;
	free(filename);
	if(file == NULL)
	{
		//errno is set by fopen returning NULL. Saved in errsv so set errno back to that
		//in case it was changed by free call.
		errno = errsv;
		return -1; //ext method
	}

	totalBytesWritten = fwrite(buffer, 1, sizeof (buffer), file);
	errsv = errno;
	fclose(file);
	if(totalBytesWritten != sizeof(buffer))
	{
			errno = errsv;
			return -1; //return error since wrong number of bytes written
	}
	return totalBytesWritten;
}

/*! \brief Gets the status of a specific file (on tape or disk)
*
*
* Returns a json string of whether the specified file is on disk or tape
* file:1 for file on disk, 0 for file on tape, -1 if file doesnt exist.
* need to free the string that is returned
*
*/
char* posix_file_status(FILE* file, int id)
{
	char * json;
	char * filename;
	int sz;

	//get the size of the filepath string, and set it
	sz = snprintf(NULL, 0, "%s%d", PREFIX,id);
	filename = (char *)malloc(sz + 1);
	sz = snprintf(filename, sz+1, "%s%d", PREFIX,id);

	file = fopen(filename,"r");
	free(filename);

	if(file == NULL)
	{
		//file had error opening or doesnt exsits so return a -1 in the json
		sz = snprintf(NULL, 0, "%s", "{ \"file\": -1 }");
		json = (char *)malloc(sz + 1);
		snprintf(json, sz+1, "%s","{ \"file\": -1 }");
		
	}
	else
	{
		sz = snprintf(NULL, 0, "%s", "{ \"file\": 1 }");
		json = (char *)malloc(sz + 1);
		snprintf(json, sz+1, "%s","{ \"file\": 1 }");
		fclose(file);
	}

	return json;
}


int main(int argc, char * argv[])
{

	FILE *file;
	int bytesRead = 0;
	bytesRead = posix_get_file(file, 1);
	printf("The number of Bytes read is %d\n",bytesRead);
	
	bytesRead = posix_get_file(file, 3);
	if (bytesRead == -1)
	{
		perror("No bytes read error was");
	}

	int bytesWritten = 0;
	bytesWritten= posix_put_file(file, 2);
	printf("The number of Bytes written is %d\n",bytesWritten);

	char * status;
	status = posix_file_status(file,1);
	printf("%s\n",status);
	free(status);
	return 0;
}