from math import sqrt, pow


X = 100
Y = 100

def get_device_coords(r1, r2):
    
    x = X - (pow(X, 2)+pow(r2, 2)-pow(r1, 2)) / (2 * X)
    x = round(x)

    temp = (pow(X, 2)+pow(r2, 2)-pow(r1, 2)) / (2*X*r2)
    h = r2 * sqrt( 1 - pow(temp, 2) )
    y = Y - h
    print(y)
    y = round(y)

    return x, y
