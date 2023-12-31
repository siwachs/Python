def multiply_matrix():
    mat1 = [[1, 1],
            [2, 2]]

    mat2 = [[1, 1],
            [2, 2]]

    row1 = len(mat1)
    col1 = len(mat1[0])

    row2 = len(mat2)
    col2 = len(mat2[0])

    if col1 != row2:
        print("Columns of mat1 not equal to rows of mat2")
        return

    mat3 = [[0 for _ in range(row2)] for _ in range(col1)]
    for i in range(0, row1):
        for j in range(0, col2):
            for k in range(0, row2):
                mat3[i][j] += mat1[i][k] + mat2[k][j]
    print(mat3)


if __name__ == "__main__":
    multiply_matrix()
