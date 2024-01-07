#include <Python.h>

static PyObject* py_add(PyObject* self, PyObject* args) {
  int a, b;
  if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;
  }
  return PyLong_FromLong(a + b);
}

static PyObject* py_sub(PyObject* self, PyObject* args) {
  int a, b;
  if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;
  }
  return PyLong_FromLong(a - b);
}

static PyObject* py_mul(PyObject* self, PyObject* args) {
  int a, b;
  if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;
  }
  return PyLong_FromLong(a * b);
}

static PyObject* py_div(PyObject* self, PyObject* args) {
  int a, b;
  if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;
  }
  if (b == 0) {
    PyErr_SetString(PyExc_ZeroDivisionError, "Cannot divide by zero");
    return NULL;
  }
  return PyLong_FromLong(a / b);
}

static PyMethodDef CalculatorMethods[] = {
    {"add", py_add, METH_VARARGS, "Add two numbers"},
    {"sub", py_sub, METH_VARARGS, "Subtract two numbers"},
    {"mul", py_mul, METH_VARARGS, "Multiply two numbers"},
    {"div", py_div, METH_VARARGS, "Divide two numbers"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef calculator = {PyModuleDef_HEAD_INIT, "calculator",
                                        NULL, -1, CalculatorMethods};

PyMODINIT_FUNC PyInit_calculator(void) { return PyModule_Create(&calculator); }
