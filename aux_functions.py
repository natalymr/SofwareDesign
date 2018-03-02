from src.cli import *


# =
def exe_equal_sign(expression):

    name = ""
    val = ""
    ind_eq = expression.find("=")

    for i in range(0, ind_eq):
        name += expression[i]
    for i in range(ind_eq + 1, len(expression)):
        val += expression[i]

    if '"' in val or "'" in val:
        if (val[0] == '"' and val[len(val) - 1] == '"')\
                or (val[0] == "'" and val[len(val) - 1] == "'"):
            val = val[1:]
            val = val[:-1]

    dict_of_variables[name] = val

    return


# $
def exe_dollar_sign(expression):

    ind_dollar = expression.find("$")
    name = ""

    for i in range(ind_dollar + 1, len(expression)):
        name += expression[i]

    if "=" in expression:
        ind_equal = expression.find("=")
        var = ""
        for i in range(0, ind_equal):
            var += expression[i]
        exe_equal_sign(var + "=" + str(dict_of_variables[name]))

    return str(dict_of_variables[name])
