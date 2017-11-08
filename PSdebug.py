from inspect import currentframe


def get_linenumber():
    cf = currentframe()
    return str(cf.f_back.f_lineno)

