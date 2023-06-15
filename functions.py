import math

def null_checker(variable):
    if variable is None:
        print("Variable is null.")
    elif isinstance(variable, float) and math.isnan(variable):
        print("Variable contains NaN.")
    else:
        print("Variable is not null and does not contain NaN.")
