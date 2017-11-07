from inspect import currentframe


class PSdebug():
    def get_linenumber():
        cf = currentframe()
        return cf.f_back.f_lineno

