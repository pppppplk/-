from multiprocessing import Process, Pool
import numpy as np

def element(index1, index2, A, B, file):
    global res
    i, j = index1, index2
    matrix = B.copy()
    res = 0

    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    if index1 == 0 and index2 == 0:
        with open(file, "w") as f:
            f.write(str(res) + " ")
    else:
        with open(file, "a+") as f:
            if j == 0:
                f.write("\n" + str(res) + " ")
            else:
                f.write(str(res) + " ")
    return matrix

try:
    A = np.loadtxt("matr1.txt")
    B = np.loadtxt("matr2.txt")
    pool = Pool(6) # объединяет несколько процессов
    print(" число процессов:", len(A) * len(B[0]))
    for i in range(len(A)):
        for j in range(len(B[0])):
            proc = Process(target=element, args=(i, j, A, B, "matr3.txt"))
            proc.start()
            proc.join()
            pool.apply(element, (i, j, A, B, "p.txt")) #последовательное выполнение
except Exception:
    print(" ошибка")



