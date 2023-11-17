from flask import Flask , render_template , request
import numpy as np

class Matrix:
    def __init__(self, input):
        assert type(input) == list, "Bad input"
        self.input = input

    def __str__(self):
        return "The following output matrix is " + str(self.input)
    def __add__(self, other):
        assert type(other) == Matrix and len(self.input) == len(other.input), "Math rules violation"
        m = len(self.input)
        n = len(self.input[0])
        c = [["0" for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                c[i][j] = self.input[i][j] + other.input[i][j]
        return Matrix(c)

    def __sub__(self, other):
        assert type(other) == Matrix and len(self.input) == len(other.input), "Math rules violation"
        m = len(self.input)
        n = len(self.input[0])
        c = [["0" for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                c[i][j] = self.input[i][j] - other.input[i][j]
        return Matrix(c)

    def __neg__(self):
        m = len(self.input)
        n = len(self.input[0])
        c = [["0" for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                c[i][j] = -1 * self.input[i][j]
        return Matrix(c)

    def __mul__(self, other):
        assert len(self.input[0]) == len(other.input), "These matrices can't be multiplied"
        c = [["0" for _ in range(len(other.input[0]))] for _ in range(len(self.input))]

        for i in range(len(self.input)):
            for j in range(len(other.input[0])):
                total = 0
                for j2 in range(len(other.input)):
                    total += self.input[i][j2] * other.input[j2][j]
                c[i][j] = total

        return Matrix(c)
def mult2(input1, c):
        assert type(input1) == Matrix , "Invalid input"
        m = len(input1.input)
        n = len(input1.input[0])
        result = [["0" for _ in range(n)] for _ in range(m)]

        for i in range(m):
            for j in range(n):
                result[i][j] = input1.input[i][j] * c

        return Matrix(result)


def determinant(input1):
    assert type(input1) == Matrix and len(input1.input) == len(input1.input[0]), "Incorrect input"

    if len(input1.input) == 2:
        return input1.input[0][0] * input1.input[1][1] - input1.input[0][1] * input1.input[1][0]
    elif len(input1.input) == 3:
        part1 = input1.input[0][0] * (input1.input[1][1] * input1.input[2][2] - input1.input[1][2] * input1.input[2][1])
        part2 = input1.input[0][1] * (input1.input[1][2] * input1.input[2][0] - input1.input[1][0] * input1.input[2][2])
        part3 = input1.input[0][2] * (input1.input[1][0] * input1.input[2][1] - input1.input[1][1] * input1.input[2][0])
        return part1 + part2 + part3
    else:
        det = np.linalg.det(input1.input)
        return det


def transpose(input1):
    assert type(input1) == Matrix, "Incorrect input"

    m = len(input1.input)
    n = len(input1.input[0])

    c = [["0" for _ in range(m)] for _ in range(n)]

    for i in range(m):
        for j in range(n):
            c[j][i] = input1.input[i][j]

    return Matrix(c)


def trace(input1):
    assert type(input1) == Matrix and len(input1.input) == len(input1.input[0]), "Incorrect input"

    total = 0
    i = 0
    j = 0

    while i < len(input1.input) and j < len(input1.input[0]):
        total += input1.input[i][j]
        i += 1
        j += 1

    return total


def inverse(input1):
    assert type(input1) == Matrix, "Incorrect input"

    return np.linalg.inv(input1.input)


def solve(input1):
    m = len(input1.input)
    n = len(input1.input[0])

    c = [[0 for _ in range(n - 1)] for _ in range(m)]
    c2 = [[0] for _ in range(m)]

    for i in range(m):
        for j in range(n - 1):
            c[i][j] = input1.input[i][j]
    for i in range(m):
        c2[i][0] = input1.input[i][n - 1]

    return np.linalg.solve(c, c2)
app = Flask(__name__, template_folder='Templates')
app.secret_key = "3847564739fhfhdjk"
@app.route("/")
def home() :
    return render_template("home.html")
@app.route("/dim" , methods=["GET", "POST"])
def string():
    if request.method == 'POST':
        matrix_data = request.form.get("matrix")
        matrix_data = eval(matrix_data)
        dim = str(str(len(matrix_data))+"x"+str(len(matrix_data[0])))
        matrix0 = Matrix(matrix_data)
        return str(matrix0)+" are= " + dim
    else:
        return "Method not allowed"
@app.route("/add" , methods=["GET", "POST"] )
def addin () :
    if request.method == "POST" :
        matrix_data0 = request.form.get("matrix")
        matrix_data1 = request.form.get("matrix2")
        matrix_data0 = eval(matrix_data0)
        matrix_data1 = eval(matrix_data1)
        matrix0= Matrix(matrix_data0)
        matrix1 = Matrix(matrix_data1)
        v =  matrix0 + matrix1
        return "the desired output is= " + str(v)
@app.route("/sub" , methods=["GET", "POST"] )
def subin () :
    if request.method == "POST" :
        matrix_data0 = request.form.get("matrix")
        matrix_data1 = request.form.get("matrix2")
        matrix_data0 = eval(matrix_data0)
        matrix_data1 = eval(matrix_data1)
        matrix0= Matrix(matrix_data0)
        matrix1 = Matrix(matrix_data1)
        v =  matrix0 - matrix1
        return "the desired output is= " + str(v)
@app.route("/neg", methods=["GET", "POST"])
def negate():
    if request.method == "POST":
        matrix_data = request.form.get("matrix")
        matrix_data = eval(matrix_data)
        matrix = Matrix(matrix_data)
        negated_matrix = -matrix
        return str(negated_matrix)
    else:
        return "Method not allowed"
@app.route("/mult" , methods=["GET", "POST"] )
def mult0 () :
    if request.method == "POST" :
        matrix_data0 = request.form.get("matrix")
        matrix_data1 = request.form.get("matrix2")
        matrix_data0 = eval(matrix_data0)
        matrix_data1 = eval(matrix_data1)
        matrix0= Matrix(matrix_data0)
        matrix1 = Matrix(matrix_data1)
        v =  matrix0*matrix1
        return "the desired output is= " + str(v)
@app.route("/mult1" , methods=["GET","POST"])
def multk () :
    if request.method == "POST" :
        matrix_data = request.form.get("matrix")
        constant = int(request.form.get("k") )
        matrix1 = eval(matrix_data)
        matrix = Matrix(matrix1)
        v = mult2(matrix,constant)
        return "the desired output is= " + str(v)
@app.route("/det" , methods=["GET","POST"])
def det1() :
    if request.method =='POST' :
        matrix_data = request.form.get("matrix")
        matrix = eval(matrix_data)
        matrix1 = Matrix(matrix)
        return "the determinant of the input matrix is= " +str(determinant(matrix1))
@app.route("/transpose" , methods=["GET","POST"])
def transpose1() :
    if request.method =='POST' :
        matrix_data = request.form.get("matrix")
        matrix = eval(matrix_data)
        matrix1 = Matrix(matrix)
        return "the transpose of the input matrix is= " +str(transpose(matrix1))
@app.route("/trace" , methods=["GET","POST"])
def trace1() :
    if request.method =='POST' :
        matrix_data = request.form.get("matrix")
        matrix = eval(matrix_data)
        matrix1 = Matrix ( matrix )   
        return "the trace of the input matrix is= " +str(trace(matrix1))
@app.route("/inverse" , methods=["GET","POST"])
def inverse1() :
    if request.method =='POST' :
        matrix_data = request.form.get("matrix")
        matrix = eval(matrix_data)
        matrix1 = Matrix(matrix)
        return "the inverse of the input matrix is= " +str(inverse(matrix1))
@app.route("/solve" , methods=["GET","POST"])
def solve1() :
    if request.method =='POST' :
        matrix_data = request.form.get("matrix")
        matrix = eval(matrix_data)
        matrix1 = Matrix(matrix)
        return "the solution of the input matrix is= " +str(solve(matrix1))
