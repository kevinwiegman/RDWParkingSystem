from inspect import currentframe


def get_linenumber():
    cf = currentframe()
    return "Error code at line: " + str(cf.f_back.f_lineno)

