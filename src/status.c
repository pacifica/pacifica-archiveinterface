#include <Python.h>
#include <string.h>

static PyObject *
myemsl_archiveinterface_status(PyObject *self, PyObject *args)
{
    const char *filepath;
    int sts;
    /*
        get the filepath passed in from the python code
    */
    if (!PyArg_ParseTuple(args, "s", &filepath))
        return NULL;
    sts = strlen(filepath);
    return Py_BuildValue("i", sts);
}

static PyMethodDef StatusMethods[] = {
    {"hpss_status", myemsl_archiveinterface_status, METH_VARARGS,
     "Get the status for a file in the archive."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_archiveinterface(void)
{
    (void) Py_InitModule("_archiveinterface", StatusMethods);
}
