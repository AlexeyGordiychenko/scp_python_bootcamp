# Define the function mul that takes two lists of lists (matrices) and returns their product
def mul(list x, list y):
    # Check if x and y are lists of lists of integers
    if not all(isinstance(row, list) and all(isinstance(elem, int) for elem in row) for row in x):
        raise TypeError("x must be a list of lists of integers")
    if not all(isinstance(row, list) and all(isinstance(elem, int) for elem in row) for row in y):
        raise TypeError("y must be a list of lists of integers")
    
    # Get the dimensions of the matrices
    cdef int x_rows = len(x)
    cdef int x_cols = len(x[0]) if x_rows > 0 else 0
    cdef int y_rows = len(y)
    cdef int y_cols = len(y[0]) if y_rows > 0 else 0
    
    # Check if the matrices can be multiplied
    if x_cols != y_rows:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    
    # Initialize the result matrix with zeros
    cdef list result = [[0 for _ in range(y_cols)] for _ in range(x_rows)]
    
    # Perform the matrix multiplication
    cdef int i, j, k
    for i in range(x_rows):
        for j in range(y_cols):
            for k in range(x_cols):
                result[i][j] += x[i][k] * y[k][j]
    
    return result
