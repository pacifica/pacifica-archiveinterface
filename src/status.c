#include <Python.h>
#include "numpy/arrayobject.h"
#include <string.h>
#include "hpss_api.h"

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
        return NULL;
    }

    /*
        Get file descriptor so we can call the hpss fStat on the file.
    */
   rcode = hpss_Stat((char*)filepath, &Buf);
    if(rcode < 0)
    {
        return Py_BuildValue("s", strerror(errno));
    } 
    
    return Py_BuildValue("i", (int)Buf.hpss_st_mtime);
    //return Py_BuildValue("s", "test");
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
        return NULL;
    }

    /*
        Get file descriptor so we can call the hpss fStat on the file.
    */
   rcode = hpss_Stat((char*)filepath, &Buf);
    if(rcode < 0)
    {
        return Py_BuildValue("s", strerror(errno));
    } 
    
    return Py_BuildValue("i", (int)Buf.hpss_st_ctime);
}

static PyObject *
myemsl_archiveinterface_status(PyObject *self, PyObject *args)
{
    const char *filepath;
    PyObject * alpha = PyTuple_New(100);
    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "s", &filepath))
    {
        return NULL;
    }

    int dims[100] = {0};
    int i;
    for(i=0; i < 100; i++)
    {
        PyTuple_SetItem(alpha, i,  Py_BuildValue("i", dims[i]));
    }

    //return Py_BuildValue("O", alpha);


    //sts = strlen(filepath);
    return alpha;
}

static PyMethodDef StatusMethods[] = {
    {"hpss_status", myemsl_archiveinterface_status, METH_VARARGS,
     "Get the status for a file in the archive."},
     {"hpss_mtime", myemsl_archiveinterface_mtime, METH_VARARGS,
     "Get the mtime for a file in the archive."},
     {"hpss_ctime", myemsl_archiveinterface_ctime, METH_VARARGS,
     "Get the ctime for a file in the archive."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_archiveinterface(void)
{
    (void) Py_InitModule("_archiveinterface", StatusMethods);
}
