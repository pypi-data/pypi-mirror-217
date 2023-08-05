from JestingLang.LexerParser import LexerParser
from JestingLang.Core.JVisitors.PrettyPrintingVisitors import PrintingVisitor, TreePrinter
from JestingLang.Core.JVisitors.ContextfreeInterpreterVisitor import ContextfreeInterpreterVisitor
from JestingLang.Core.JVisitors.ContextBoundInterpreterVisitor import ContextBoundInterpreterVisitor
from JestingLang.Core.JDereferencer.KeyValueDereferencer import KeyValueDereferencer

if __name__ == "__main__":

    lexerParser = LexerParser()
    lexer = lexerParser.lexer
    parser = lexerParser.parser

    def intoAST(line):
        _line = line[1:]
        lexer.input(_line)
        _parsed_tree = parser.parse(_line)
        return _parsed_tree

    visitor_pointer = []

    def run(line, visitorp=visitor_pointer):
        if len(visitorp) == 0:
            visitorp.append(ContextBoundInterpreterVisitor(KeyValueDereferencer(), resolveVolatile=False))
        if line[0] != "=":
            return "INVALID LINE!"
        _line = line[1:]
        lexer.input(_line)
        _parsed_tree = parser.parse(_line)
        _visitor = visitorp[0]
        return _visitor.visit(_parsed_tree), _parsed_tree

    print("Examples of visitors")
    print("--------------------")

    visitor1 = PrintingVisitor()
    visitor2 = TreePrinter()
    visitor3 = ContextfreeInterpreterVisitor(resolveVolatile=False)
    mapContext = KeyValueDereferencer()
    visitor4 = ContextBoundInterpreterVisitor(mapContext, resolveVolatile=False)

    visitors = [visitor1, visitor2, visitor3, visitor4]
    visitors_names=["Printer", "TreePrinter", "ContextFree", "ContextBound"]

    response = None
    while response not in map(str, range(4)):
        response = input("\n".join(["Pick a visitor:"] + ["  {}. {}".format(n,item)
                                                          for n,item in enumerate(visitors_names)]+['']))

    _visitor=visitors[int(response)]

    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if s[0] == "=":
            tree = intoAST(s)
            if tree is not None:
                new_tree = _visitor.visit(tree)
                try:
                    value = new_tree.value
                    print(value)
                except:
                    print(new_tree)
        if s[0] == ":":
            if len(s.split(":")) == 3:
                _, key, string = s.split(":")
            else:
                key, string = (None, s[1:])
            string = "=" + string
            tree = intoAST(string)
            if tree is not None:
                tree = _visitor.visit(tree)
                if key is not None and response == "3":
                    mapContext.write(key, tree)
            if response == "3":
                print(mapContext.show())
            else:
                try:
                    value = tree.value
                    print(value)
                except:
                    print(tree)
