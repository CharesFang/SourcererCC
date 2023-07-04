import os
import config
import unittest
from tests.code import extractPythonFunction


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
        