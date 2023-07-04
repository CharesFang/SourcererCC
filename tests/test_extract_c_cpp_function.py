import os
import config
import unittest
from tests.code import extractPythonFunction
from tests.code.extractCPPFunction import ExtractCPPFunction


class TestExtractPythonFunction(unittest.TestCase):
    def setUp(self) -> None:
        self.test_py_file = os.path.join(config.TEST_RESOURCES_DIR, "functions.py")
        return super().setUp()
    
    def test_get_py_functions(self):
        with open(self.test_py_file) as f:
            py_file = f.read()
        
        block_linenos, strings = extractPythonFunction.getFunctions(
            filestring=py_file,
            logging=None,
            file_path=self.test_py_file
        )

        # block numbers: List{Tuple[start, end]}
        print("\t".join(map(lambda x: f"{x[0]}-{x[1]}", block_linenos)))

        # function strings: List[str]
        print("\n".join(strings))


class TestExtractCPPFunction(unittest.TestCase):
    def setUp(self) -> None:
        self.cpp_extractor = ExtractCPPFunction()
        self.test_c_file = os.path.join(config.TEST_RESOURCES_DIR, "adcxx1c.c")
        return super().setUp()
    
    def test_get_cpp_functions(self):
        self.cpp_extractor.get_functions(self.test_c_file)
