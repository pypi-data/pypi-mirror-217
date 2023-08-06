from QuBuilders import quloaders
import unittest


class test(unittest.TestCase):

    def test_read_file(self):
        file = open("data_sample/eq/exa.json", 'r', encoding="utf-8")
        qu = quloaders.read_file_j(file_object=file)
        self.assertEqual(qu.answers == ["adison"], True)  # checking if the answer of the question will be true

    def test_read_all_files(self):
        qus = quloaders.read_all_files_j("data_sample/eq/", "hello", "fffffff")
        self.assertEqual(qus[1].answers == ["goodbye"], False)


if __name__ == "__main__":
    unittest.main()
