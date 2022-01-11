get_number_of_squares = g = lambda n, i=1: i * i < n and -~g(n - i * i, i + 1)


print(get_number_of_squares(6))
