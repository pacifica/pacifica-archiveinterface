#include <Python.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include "hpss_api.h"
#include <sys/types.h>
#include <utime.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <hpss_errno.h>
#include <hpss_api.h>
#include <hpss_Getenv.h>
#include <hpss_limits.h>

static PyObject *archiveInterfaceError;

static PyObject *
pacifica_archiveinterface_mtime(PyObject *self, PyObject *args)
{
    char *filepath;
    int rcode;
    hpss_stat_t Buf;
    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "s", &filepath))
    {
        PyErr_SetString(archiveInterfaceError, "Error parsing filepath argument");
        return NULL;
    }

    /*
        Get file descriptor so we can call the hpss fStat on the file.
    */
   rcode = hpss_Stat(filepath, &Buf);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    } 
    /* Sleep is a hack to get around other hpss thread not finished yet
    */
    usleep(30000);
    return Py_BuildValue("i", (int)Buf.hpss_st_mtime);
}

static PyObject *
pacifica_archiveinterface_ctime(PyObject *self, PyObject *args)
{
    char *filepath;
    int rcode;
    hpss_stat_t Buf;
    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "s", &filepath))
    {
        PyErr_SetString(archiveInterfaceError, "Error parsing filepath argument");
        return NULL;
    }

    /*
        Get file descriptor so we can call the hpss fStat on the file.
    */
   rcode = hpss_Stat(filepath, &Buf);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    } 
    /* Sleep is a hack to get around other hpss thread not finished yet
    */
    usleep(30000);
    return Py_BuildValue("i", (int)Buf.hpss_st_ctime);
}

static PyObject *
pacifica_archiveinterface_filesize(PyObject *self, PyObject *args)
{
    char *filepath;
    int rcode;
    hpss_stat_t Buf;
    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "s", &filepath))
    {
        PyErr_SetString(archiveInterfaceError, "Error parsing filepath argument");
        return NULL;
    }

    /*
        Get file descriptor so we can call the hpss fStat on the file.
    */
   rcode = hpss_Stat(filepath, &Buf);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    } 
    /* Sleep is a hack to get around other hpss thread not finished yet
    */
    usleep(30000);
    return Py_BuildValue("i", (int)Buf.st_size);
}

static PyObject *
pacifica_archiveinterface_status(PyObject *self, PyObject *args)
{
    char *filepath;
    PyObject * bytes_per_level= PyTuple_New(HPSS_MAX_STORAGE_LEVELS);
    int rcode;
    int i;
    u_signed64 bytes;
    hpss_xfileattr_t attrs;

    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "s", &filepath))
    {
        PyErr_SetString(archiveInterfaceError, "Error parsing filepath argument");
        return NULL;
    }

    /* Store hpss file xattributes into attrs*/
    rcode = hpss_FileGetXAttributes(filepath, API_GET_STATS_FOR_ALL_LEVELS, 0, &attrs);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    }

    /* Loop over each level getting the bytes at that level and it it to the tuple for return */
    for(i=0; i < HPSS_MAX_STORAGE_LEVELS; i++)
    {
        bytes = attrs.SCAttrib[i].BytesAtLevel;
        PyTuple_SetItem(bytes_per_level, i,  Py_BuildValue("L", (long long)bytes));
    }
    /* Sleep is a hack to get around other hpss thread not finished yet
    */
    usleep(30000);
    return bytes_per_level;
}

static PyObject *
pacifica_archiveinterface_ping_core(PyObject *self, PyObject *args)
{
    /*
        latency[0] = time ping responds in seconds (epoch)
        latency[1] = time ping responds mseconds
        latency[2] = time when ping request was sent (epoch)
        to get latency = latency[2] - latency[0]
    */
    PyObject * latency= PyTuple_New(4);
    int ret;
    hpss_uuid_t uuid;
    struct timeval tv;
    unsigned32 secs,usecs;

    /*
        The Hex values used here corresond to the EMSL HPSS CORE server
        getting these values dynamically becomes difficult
    */
    uuid.time_low = 0xe52ea34e;
    uuid.time_mid = 0xc9aa;
    uuid.time_hi_and_version = 0x11de;
    uuid.clock_seq_hi_and_reserved = 0xb4;
    uuid.clock_seq_low = 0x08;
    uuid.node[0] = 0x00;
    uuid.node[1] = 0x21;
    uuid.node[2] = 0x5e;
    uuid.node[3] = 0xdc;
    uuid.node[4] = 0x76;
    uuid.node[5] = 0x4c;

    /* Obtain current time as seconds elapsed since the Epoch. */
    gettimeofday(&tv,NULL);

    /* Attempt to ping the CORE server*/
    ret = hpss_PingCore(&uuid,&secs,&usecs);
    //throw exception if server doesnt respond
    if(ret < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    }


    PyTuple_SetItem(latency, 0,  Py_BuildValue("i", secs)); 
    PyTuple_SetItem(latency, 1,  Py_BuildValue("i", usecs)); 
    PyTuple_SetItem(latency, 2,  Py_BuildValue("i", tv.tv_sec)); 
    PyTuple_SetItem(latency, 3,  Py_BuildValue("i", tv.tv_usec));
    return latency;
}

static PyObject *
pacifica_archiveinterface_stage(PyObject *self, PyObject *args)
{
    char *filepath;
    char * filepathCopy;
    int rcode;
    int fd = 0;
    
    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "s", &filepath))
    {
        PyErr_SetString(archiveInterfaceError, "Error parsing filepath argument");
        return NULL;
    }
    
    filepathCopy = strdup(filepath);


    fd = hpss_Open(filepathCopy, O_RDWR | O_NONBLOCK, 000, NULL, NULL, NULL);
    if(fd < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    }

    rcode = hpss_Stage(fd, 0, cast64m(0), 0, BFS_STAGE_ALL);
    if(rcode != 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        hpss_Close(fd);
        free(filepathCopy);
        return NULL;
    }
    hpss_Close(fd); 
    /* Sleep is a hack to get around other hpss thread not finished yet
    */
    free(filepathCopy);
    usleep(30000);
    Py_RETURN_NONE;
}

static PyObject *
pacifica_archiveinterface_utime(PyObject *self, PyObject *args)
{
    char *filepath;
    float mtime;
    struct utimbuf t;
    int rcode;

    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "sf", &filepath, &mtime))
    {
        PyErr_SetString(archiveInterfaceError, "Error parsing arguments");
        return NULL;
    }


    t.modtime = mtime;
    t.actime = mtime;


    rcode = hpss_Utime(filepath, &t);
    if(rcode != 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    }
    Py_RETURN_NONE;
}


static PyMethodDef StatusMethods[] = {
    {"hpss_status", pacifica_archiveinterface_status, METH_VARARGS,
        "Get the status for a file in the archive."},
    {"hpss_mtime", pacifica_archiveinterface_mtime, METH_VARARGS,
        "Get the mtime for a file in the archive."},
    {"hpss_ctime", pacifica_archiveinterface_ctime, METH_VARARGS,
        "Get the ctime for a file in the archive."},
    {"hpss_filesize", pacifica_archiveinterface_filesize, METH_VARARGS,
        "Get the filesize for a file in the archive."},
    {"hpss_ping_core", pacifica_archiveinterface_ping_core, METH_VARARGS,
        "Check if the Core Server is actively responding."},
    {"hpss_stage", pacifica_archiveinterface_stage, METH_VARARGS,
        "Stage a file to disk within hpss"},
    {"hpss_utime", pacifica_archiveinterface_utime, METH_VARARGS,
        "Set the modified time on a file"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_hpssExtensions(void)
{
    PyObject * m;
    m = Py_InitModule("_hpssExtensions", StatusMethods);
    if (m == NULL)
    {
        return;
    }

    archiveInterfaceError = PyErr_NewException("archiveInterface.error", NULL, NULL);
    Py_INCREF(archiveInterfaceError);
    PyModule_AddObject(m,"error",archiveInterfaceError);
}
