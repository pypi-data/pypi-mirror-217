#include <pybind11/pybind11.h>

namespace py = pybind11;

float some_fn(float arg1, float arg2) {
    return arg1 + arg2;
}


PYBIND11_MODULE(engine, handle) {
    handle.doc() = "This is the module docs.";
    handle.def("some_fn_python_name", &some_fn, "A function which adds two numbers"); 
}