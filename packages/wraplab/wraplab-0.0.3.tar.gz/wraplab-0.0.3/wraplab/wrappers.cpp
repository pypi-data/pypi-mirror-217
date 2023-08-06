#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

namespace py = pybind11;

float add(float arg1, float arg2) {
    return arg1 + arg2;
}

class Matrix {
    private:
        int cols, rows;
        std::vector<std::vector<float>> data;

    public:
        // constructor
        Matrix(int rows, int cols) {
            this->cols = cols;
            this->rows = rows;
            this->data = std::vector<std::vector<float>>(rows, std::vector<float>(cols, 0));
        }

        // Static method to create a matrix filled with zeros
        static Matrix zeros(int rows, int columns) {
            return Matrix(rows, columns);
        }

        static Matrix ones(int rows, int columns) {
            Matrix matrix(rows, columns);
            for (int i = 0; i < matrix.rows; i++) {
                for (int j = 0; j < matrix.cols; j++) {
                    matrix.data[i][j] = 1;
                }
            }
            return matrix;
        }

            // Method to convert data to a NumPy matrix
    py::array_t<float> numpy() {
        auto nrows = static_cast<size_t>(rows);
        auto ncols = static_cast<size_t>(cols);

        py::array_t<float> np_matrix({ nrows, ncols });
        auto buf = np_matrix.request();
        float* ptr = static_cast<float*>(buf.ptr);

        for (size_t i = 0; i < nrows; i++) {
            for (size_t j = 0; j < ncols; j++) {
                ptr[i * ncols + j] = data[i][j];
            }
        }

        return np_matrix;
    }
        
};

PYBIND11_MODULE(engine, handle) {
    handle.doc() = "This is the module docs.";
    handle.def("add", &add, "A function which adds two numbers"); 
        
    py::class_<Matrix>(handle, "Matrix")
        .def(py::init<int, int>())
        .def_static("zeros", &Matrix::zeros)
        .def_static("ones", &Matrix::ones)
        .def("numpy", &Matrix::numpy);
}