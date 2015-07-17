#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PREFIX "/home/chrisExamples/"
#define BUFFERSIZE (1<<10)

//for use of the get/put flags
typedef enum getPutFlag
{
	GET,
	PUT
} getPutFlag;


/*! \brief Gets a file from a Posix style file structure
*
*
* Opens the file specified in the id parameter.  (prefixed with config option) for reading.  Then
* opens the fd for writing . Will return the number of bytes read from the id file
* and written into the fd file
* If an error occurs, errno will be set and -1 will be returned.
* fd is the file descriptor that will point to the file that will be written to
* id will be turned into a filepath and will point to a file to read from which
* contents will be written into the fd file
* 
*/
int posix_get_file(int fd, int id)
{
	int totalBytesRead;
	totalBytesRead = posix_files(fd, id, GET);
	return totalBytesRead;
}

/*! \brief Puts contents into a file from a Posix style file structure
*
*
* Opens the file specified in the id parameter.  (prefixed with config option) for writing.  Then
* opens the fd for reading . Will return the number of bytes read from the fd file
* and written into the id file
* If an error occurs, errno will be set and -1 will be returned.
* fd is the file descriptor that will point to a file to read from
* id will be turned into a filepath and will point to a file to put contents form fd into
*
*/
int posix_put_file(int fd, int id)
{
	int totalBytesWritten;
	totalBytesWritten = posix_files(fd, id, PUT);
	return totalBytesWritten;
}

/*! \brief Takes an integer id and makes it into a filename, using the prefix
*
*
* Returns CHAR *The filename of the file specified with id.  If an error occurs NULL is returned
* NOTE: THe char * returned will need to be freed if it is not NULL
*
*/
char * posix_get_filename(int id)
{
	char * filename;
	int sz;
	int errsv;

	//get the size of the filepath string, and set it
	sz = snprintf(NULL, 0, "%s%d", PREFIX,id);
	if( sz < 0) //error state, errno was set from snprintf
	{
		return NULL;
	}

	filename = (char *)malloc(sz + 1);
	if(filename == NULL) //error occured with allocating memory, errno set from the malloc call
	{
		return NULL;
	}

	sz = snprintf(filename, sz+1, "%s%d", PREFIX,id);
	if( sz < 0) //error state, errno was set from snprintf
	{
		errsv = errno;
		free(filename);
		errno = errsv;
		return NULL;
	}

	return filename;
}

/*! \brief Gets the status of a specific file (on tape or disk)
*
*
* Returns a integer of whether the specified file is on disk or tape
* file:1 for file on disk, 0 for file on tape, -1 if file doesnt exist or error occured.
* id param is for finding the file
*
*/
int posix_file_status( int id)
{
	int fileStatus;
	int sz;
	FILE * file;
	char * filename = posix_get_filename(id);

	if(filename == NULL)
	{
		//error occured gettng filename
		return -1;
	}

	file = fopen(filename,"r");
	free(filename);

	if(file == NULL)
	{
		//file had error opening or doesnt exsits so return a -1
		fileStatus = -1;
		
	}
	else
	{
		fileStatus = 1;
		fclose(file);
	}

	return fileStatus;
}

/*! \brief Reads from the first file argument and writes contents in second file argument
*
*
* Returns The number of bytes copied from readFile into writeFile or -1 on error
* 
*/
int posix_file_copy_helper(FILE * readFile, FILE * writeFile)
{
	int totalBytes = 0;
	int iterationBytes = 0;
	int bytesWritten = 0;
	char buffer[BUFFERSIZE];

	//read whole file until you reach end
	while (!feof(readFile))
	{
		iterationBytes = fread(buffer, 1, (sizeof buffer), readFile);

		if(ferror(readFile)) //an error occured with fread
		{
			return -1; //return error
		}

		bytesWritten = fwrite(buffer,1,iterationBytes, writeFile);
		if(bytesWritten != iterationBytes)
		{
			//error occured.  errno set by fwrite
			return -1;
		}
		totalBytes += iterationBytes; //sum the total bytes read if some were read
	}


	return totalBytes;
}

/*! \brief Handles whether to put a file or get file, including making FILE * for both files 
*
*
* Opens the file specified in the id parameter.  (prefixed with config option).  Then
* opens the file pointed at by fd. Will return the number of bytes read and written
* If an error occurs, errno will be set and -1 will be returned.
* The files opened will be closed when read/write are done
* fd is the file descriptor that will point to a file 
* id will be turned into a filepath and will point to a file
* flag is a enum flag with options GET or PUT
*
*/
int posix_files(int fd, int id, getPutFlag flag)
{

	int sz;
	int errsv;
	int totalBytes = 0;
	FILE * idFile;
	FILE * fdFile;


	char * filename = posix_get_filename(id);
	if(filename == NULL)
	{
		//error occured gettng filename
		return -1;
	}

	//if doing a get file
	if(flag == GET)
	{
		idFile = fopen(filename,"r");
		errsv = errno;
		free(filename);
		if(idFile == NULL)
		{
			//errno is set by fopen returning NULL. Saved in errsv so set errno back to that
			//in case it was changed by free call.
			errno = errsv;
			return -1; //ext method
		}

		//open up the fd file so you can put the contents into it
		fdFile = fdopen(fd,"w");
		if(fdFile == NULL)
		{
			//err occured.  errno set by fdopen
			errsv = errno;
			fclose(idFile);
			errno= errsv;
			return -1; //ext method
		}

		totalBytes = posix_file_copy_helper(idFile, fdFile);
	}
	//for a put file
	else if(flag == PUT)
	{
		idFile = fopen(filename,"w");
		errsv = errno;
		free(filename);
		if(idFile == NULL)
		{
			//errno is set by fopen returning NULL. Saved in errsv so set errno back to that
			//in case it was changed by free call.
			errno = errsv;
			return -1; //ext method
		}

		//open up the fd file so you can read the contents from it
		fdFile = fdopen(fd,"r");
		if(fdFile == NULL)
		{
			//err occured.  errno set by fdopen
			errsv = errno;
			fclose(idFile);
			errno= errsv;
			return -1; //ext method
		}

		totalBytes = posix_file_copy_helper(fdFile, idFile);
	}
	
	if(totalBytes == -1)
	{
		//an error occured at some point along the line
		errsv = errno;
		fclose(idFile);
		fclose(fdFile);
		errno = errsv;
	}
	else
	{
		fclose(idFile);
		fclose(fdFile);
	}


	return totalBytes;
}
