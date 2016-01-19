# pygen.py  17/01/2016  D.J.Whale
#
# Generator for pcode.py that generates python from each of the actions.

import sys

class Generator():
    def __init__(self):
        self.indentlev = 0
        # stack of active case statements being parsed
        # holds a list [exprstr, optioncounter]
        self.case = []

    def indent(self):
        self.indentlev += 4

    def outdent(self):
        self.indentlev -= 4

    def out(self, msg):
        print((" " * self.indentlev) + msg)

    #----- GENERATED ON THE FLY -----------------------------------------------

    def OUTPUT(self, p, i_expr):
        expr = p[i_expr]
        self.out("print(%s)" % str(expr))

    def assign(self, p, i_id, i_expr):
        id = p[i_id]
        expr = p[i_expr]
        self.out("%s = %s" % (id, expr))

    def array1assign(self, p, i_id, i_indexexpr, i_valueexpr):
        id = p[i_id]
        indexexpr = p[i_indexexpr]
        valueexpr = p[i_valueexpr]
        #TODO arrays need to auto-size, for this to work
        self.out("%s[%s] = %s" % (id, indexexpr, valueexpr))

    def array2assign(self, p, i_id, i_index1expr, i_index2expr, i_valueexpr):
        id = p[i_id]
        index1expr = p[i_index1expr]
        index2expr = p[i_index2expr]
        valueexpr  = p[i_valueexpr]
        #TODO arrays need to auto-size, for this to work
        self.out("%s[%s][%s] = %s" % (id, index1expr, index2expr, valueexpr))

    def arrayinit(self, p, i_id, i_initialiser):
        id = p[i_id]
        initialiser = p[i_initialiser]
        self.out("%s = [%s]" % (id, initialiser))

    def READLINE(self, p, i_file, i_expr):
        file = p[i_file]
        expr = p[i_expr]
        p[0] = "readline(%s, %s)" % (file, expr)
        #TODO runtime support required

    def WRITELINE(self, p, i_file, i_expr1, i_expr2):
        file = p[i_file]
        expr1 = p[i_expr1]
        expr2 = p[i_expr2]
        self.out("writeline(%s, %s, %s)" % (file, expr1, expr2))
        #TODO runtime support required

    def IF(self, p, i_expr):
        expr = p[i_expr]
        self.out("if %s:" % expr)
        self.indent()

    def ELSE(self, p):
        self.outdent()
        self.out("else:")
        self.indent()

    def ENDIF(self, p):
        self.outdent()
        #self.out("")

    def WHILE(self, p, i_expr):
        expr = p[i_expr]
        self.out("while %s:" % expr)
        self.indent()

    def ENDWHILE(self, p):
        self.outdent()
        #self.out("")

    def REPEAT(self, p):
        self.out("while True:")
        self.indent()

    def UNTIL(self, p, i_expr):
        expr = p[i_expr]
        self.out("if %s: break" % expr)
        self.outdent()
        #self.out("")

    def FOR(self, p, i_id, i_from, i_to):
        id = p[i_id]
        f = p[i_from]
        t = p[i_to]
        self.out("for %s in range(%s, %s):" % (id, f, t))
        self.indent()

    def ENDFOR(self, p):
        self.outdent()
        #self.out("")

    def CASE(self, p, i_expr):
        expr = p[i_expr]
        self.case.append([expr, 0])

    def WHEN(self, p, i_expr):
        expr = p[i_expr]
        info = self.case[-1]
        check, count = info

        if count == 0:
            self.out("if %s == %s:" % (check, expr))
        else:
            self.out("elif %s == %s:" % (check, expr))
        self.indent()
        count += 1
        (self.case[-1])[1] = count

    def ENDWHEN(self, p):
        self.outdent()
        #self.out("")

    def CASEELSE(self, p):
        self.out("else:")
        self.indent()

    def ENDCASEELSE(self, p):
        self.outdent()

    def ENDCASE(self, p):
        self.case.pop()

    def defparams(self, p, i_params, i_id):
        params = p[i_params]
        id = p[i_id]
        r = params + ", " + id
        p[0] = id

    def FUNCTION(self, p, i_id, i_params):
        id = p[i_id]
        params = p[i_params]
        self.out("def %s(%s):" % (id, params))
        self.indent()

    def RETURN(self, p, i_expr):
        expr = p[i_expr]
        p[0]="Return"
        self.out("return %s" % str(expr))

    def ENDFUNCTION(self, p):
        self.outdent()
        #self.out("")

    def PROCEDURE(self, p, i_id, i_params):
        id = p[i_id]
        params = p[i_params]
        self.out("def %s(%s):" % (id, params))
        self.indent()
        self.out("pass") # temporary fix for empty procedures

    def ENDPROCEDURE(self, p):
        self.outdent()
        #self.out("")

    def callparams(self, p, i_params, i_expr):
        params = p[i_params]
        expr = p[i_expr]
        r = params + ", " + expr
        p[0] = r

    def proccall(self, p, i_id, i_params):
        id = p[i_id]
        params = p[i_params]
        self.out("%s(%s)" % (id, params))

    def fncall(self, p, i_id, i_params):
        id = p[i_id]
        params = p[i_params]
        r = "%s(%s)" % (id, params)
        p[0] = r

    def bracket(self, p, i_expr):
        expr = p[i_expr]
        r = "(" + expr + ")"
        p[0] = r

    def boolean(self, p, value):
        r = value
        p[0] = r


    #---- PASSED ON THE PARSE STACK -------------------------------------------

    def number(self, p, i_number):
        number = p[i_number]
        p[0]=str(number)

    def id(self, p, i_id):
        id = p[i_id]
        p[0]=id

    def string(self, p, i_string):
        string = p[i_string]
        p[0]=string

    def USERINPUT(self, p):
        p[0]="raw_input()"

    def LEN(self, p, i_id):
        id = p[i_id]
        r = "len(%s)" % id
        p[0] = r

    def plus(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "+" + str(right)
        p[0] = r

    def minus(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "-" + str(right)
        p[0] = r

    def times(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "*" + str(right)
        p[0] = r

    def divide(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "/" + str(right)
        p[0] = r

    def MOD(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "%" + str(right)
        p[0] = r

    def uminus(self, p, i_expr):
        expr = p[i_expr]
        r = "-" + str(expr)
        p[0] = r

    def uplus(self, p, i_expr):
        expr = p[i_expr]
        r = expr
        p[0] = r

    def NOT(self, p, i_expr):
        expr = p[i_expr]
        r = "! " + str(expr)
        p[0] = r

    def equal(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "==" + str(right)
        p[0] = r

    def notequal(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "!=" + str(right)
        p[0] = r

    def lessequal(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "<=" + str(right)
        p[0] = r

    def greaterequal(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + ">=" + str(right)
        p[0] = r

    def greater(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + ">" + str(right)
        p[0] = r

    def less(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "<" + str(right)
        p[0] = r

    def AND(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + " and " + str(right)
        p[0] = r

    def OR(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + " or " + str(right)
        p[0] = r

    def XOR(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        r = str(left) + "^" + str(right)
        p[0] = r

    #----- HELPERS ------------------------------------------------------------

    def copy(self, p, i_item):
        item = p[i_item]
        r = item
        p[0] = r

    def empty(self, p):
        p[0] = ""

    def comma(self, p, i_left, i_right):
        left = p[i_left]
        right = p[i_right]
        try:
            r = left + ", " + right
        except TypeError:
            r = str(left) + ", " + str(right)
        p[0] = r

    def concat(self, p, i_one, i_two):
        one = p[i_one]
        two = p[i_two]
        try:
            both = one + two
        except TypeError:
            both = str(one) + str(two)
        p[0] = both



#----- TEST -------------------------------------------------------------------

def test():
    generator = Generator()
    # TODO call various methods with p parameters, to test output

if __name__ == "__main__":
    test()

# END
