import antlr4
import typing as T
from resources.CPP14Lexer import CPP14Lexer
from resources.CPP14Parser import CPP14Parser
from resources.CPP14ParserListener import CPP14ParserListener


class ExtractCPPFunction:

    def read_source(self, file: str) -> str:
        with open(file, "r") as f:
            return f.read()

    def get_functions(self, file_path: str) -> T.Tuple[T.List[T.Tuple[int, int]], T.List[str]]:
        source_file_string = self.read_source(file_path)

        # read the the source code
        input_stream = antlr4.InputStream(source_file_string)
        # lex the source code
        lexer = CPP14Lexer(input_stream)
        # convert and process the first-round source code tokens
        stream = antlr4.CommonTokenStream(lexer)
        # leverage Parser to parse the tokens
        parser = CPP14Parser(stream)
        # get the AST
        ast = parser.translationUnit()

        # use the listener to extract and record our results.
        listener = FunctionListener()

        # introduce a walker to traverse the AST
        walker = antlr4.ParseTreeWalker()

        walker.walk(listener, ast)

        # Return the results we want.
        return (listener.block_linenos, listener.functions)


class FunctionListener(CPP14ParserListener):
    def __init__(self) -> None:
        self.functions: T.List[str] = list()
        self.block_linenos: T.List[T.Tuple[int, int]] = list()

    def enterFunctionDefinition(self, ctx: CPP14Parser.FunctionDefinitionContext):
        function_name = ctx.declarator().getText()
        function_body = ctx.functionBody().getText()
        
        start_line = ctx.start.line
        end_line = ctx.stop.line

        self.functions.append(f"{function_name}\n{function_body}")

        self.block_linenos.append((start_line, end_line))
