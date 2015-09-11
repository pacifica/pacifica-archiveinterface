#include <Python.h>
#include "numpy/arrayobject.h"
#include <string.h>
#include "hpss_api.h"

static PyObject *archiveInterfaceError;

static PyObject *
myemsl_archiveinterface_mtime(PyObject *self, PyObject *args)
{
    const char *filepath;
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
   rcode = hpss_Stat((char*)filepath, &Buf);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    } 
    
    return Py_BuildValue("i", (int)Buf.hpss_st_mtime);
}

static PyObject *
myemsl_archiveinterface_ctime(PyObject *self, PyObject *args)
{
    const char *filepath;
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
   rcode = hpss_Stat((char*)filepath, &Buf);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    } 
    
    return Py_BuildValue("i", (int)Buf.hpss_st_ctime);
}

static PyObject *
myemsl_archiveinterface_filesize(PyObject *self, PyObject *args)
{
    const char *filepath;
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
   rcode = hpss_Stat((char*)filepath, &Buf);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    } 
    
    return Py_BuildValue("i", (int)Buf.st_size);
}

static PyObject *
myemsl_archiveinterface_status(PyObject *self, PyObject *args)
{
    const char *filepath;
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
    rcode = hpss_FileGetXAttributes((char*)filepath, API_GET_STATS_FOR_ALL_LEVELS, 0, &attrs);
    if(rcode < 0)
    {
        PyErr_SetString(archiveInterfaceError, strerror(errno));
        return NULL;
    }

    /* Loop over each level getting the bytes at that level and it it to the tuple for return */
    for(i=0; i < HPSS_MAX_STORAGE_LEVELS; i++)
    {
        bytes = attrs.SCAttrib[i].BytesAtLevel;
        PyTuple_SetItem(bytes_per_level, i,  Py_BuildValue("l", (long)bytes));
    }

    return bytes_per_level;
}

static PyObject *
myemsl_archiveinterface_ping_core(PyObject *self, PyObject *args)
{
      
    return Py_BuildValue("i", 1);
}

static PyMethodDef StatusMethods[] = {
    {"hpss_status", myemsl_archiveinterface_status, METH_VARARGS,
     "Get the status for a file in the archive."},
     {"hpss_mtime", myemsl_archiveinterface_mtime, METH_VARARGS,
     "Get the mtime for a file in the archive."},
     {"hpss_ctime", myemsl_archiveinterface_ctime, METH_VARARGS,
     "Get the ctime for a file in the archive."},
     {"hpss_filesize", myemsl_archiveinterface_filesize, METH_VARARGS,
     "Get the filesize for a file in the archive."},
     {"hpss_ping_core", myemsl_archiveinterface_ping_core, METH_VARARGS,
     "Check if the Core Server is actively responding."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_archiveinterface(void)
{
    PyObject * m;
    m = Py_InitModule("_archiveinterface", StatusMethods);
    if (m == NULL)
    {
        return;
    }

    archiveInterfaceError = PyErr_NewException("archiveInterface.error", NULL, NULL);
    Py_INCREF(archiveInterfaceError);
    PyModule_AddObject(m,"error",archiveInterfaceError);
}
