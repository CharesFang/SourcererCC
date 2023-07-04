import antlr4
import typing as T
from tests.resources.CPP14Lexer import CPP14Lexer
from tests.resources.CPP14Parser import CPP14Parser
from tests.resources.CPP14ParserVisitor import CPP14ParserVisitor
from tests.resources.CPP14ParserListener import CPP14ParserListener


# class CPP14Visitor(CPP14ParserVisitor):


class ExtractCPPFunction:
    def __init__(self) -> None:
        pass

    def read_source(self, file: str) -> str:
        with open(file, "r") as f:
            return f.read()

    def get_functions(self, file_path: str) -> T.Tuple[T.List[T.Tuple[int, int]], T.List[str]]:
        source_file_string = self.read_source(file_path)

        input_stream = antlr4.InputStream(source_file_string)
        lexer = CPP14Lexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = CPP14Parser(stream)

        ast = parser.translationUnit()

        listener = FunctionListener()

        walker = antlr4.ParseTreeWalker()

        walker.walk(listener, ast)


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

        # print(f"function name: {function_name}, function body: {function_body}")
        # print(f"start line: {start_line}, end line: {end_line}")
