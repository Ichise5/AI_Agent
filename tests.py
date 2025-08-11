# tests.py

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_content

class TestGetFiles(unittest.TestCase):
    def test_caculator(self):
        result = get_files_info("calculator",".")
        expected_result = """Result for current directory:
 - pkg: file_size=4096 bytes, is_dir=True
 - tests.py: file_size=1343 bytes, is_dir=False
 - main.py: file_size=576 bytes, is_dir=False
"""

        self.assertEqual(result,expected_result)
    
    def test_caculator_package(self):
        result = get_files_info("calculator","pkg")
        expected_result = """Result for 'pkg' directory:
 - calculator.py: file_size=1738 bytes, is_dir=False
 - render.py: file_size=767 bytes, is_dir=False
"""
        self.assertEqual(result,expected_result)
    
    def test_nonexistent_folder(self):
        result = get_files_info("calculator","/bin")
        expected_result = """Result for '/bin' directory:
Error: Cannot list "/bin" as it is outside the permitted working directory"""
        self.assertEqual(result,expected_result)

    def test_outside_boundaries(self):
        result = get_files_info("calculator","../")
        expected_result = """Result for '../' directory:
Error: Cannot list "../" as it is outside the permitted working directory"""
        self.assertEqual(result,expected_result)


class TestGetFileContents(unittest.TestCase):
    def test_caculator_main(self):
        result = get_file_content("calculator", "main.py")

    def test_caculator_pkg_calc(self):
        result = get_file_content("calculator", "pkg/calculator.py")

    def test_bin_cat(self):
        result = get_file_content("calculator", "/bin/cat") 
        expected_result = 'Error: File not found or is not a regular file: "/bin/cat"'
        self.assertEqual(result,expected_result)

    def test_pkg_nonexistent(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        expected_result = 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
        self.assertEqual(result,expected_result)
        

if __name__ == "__main__":

    """     print("Result for current directory:")
        print(get_files_info("calculator", "."))

        print("Result for 'pkg' directory:")
        print(get_files_info("calculator", "pkg"))

        print("Result for '/bin' directory:")
        print(get_files_info("calculator", "/bin"))

        print("Result for '../' directory:")
        print(get_files_info("calculator", "../")) """


    print("Result for 'main.py' file:")
    print(get_file_content("calculator", "main.py"))

    print("Result for 'pkg/calculator.py' file:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("Result for '/bin/cat' file:")
    print(get_file_content("calculator", "/bin/cat"))

    print("Result for 'pkg/does_not_exist.py' file:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

    unittest.main()

