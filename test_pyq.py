from pyq.astmatch import ASTMatchEngine

import unittest
import os.path
import ast


class TestASTMatchEngine(unittest.TestCase):
    def setUp(self):
        self.m = ASTMatchEngine()

    def filepath(self, filename):
        return os.path.join(os.path.dirname(__file__), 'testfiles', filename)

    def test_classes(self):
        matches = list(self.m.match('class', self.filepath('classes.py')))
        self.assertEqual(len(matches), 2)

        # check instances
        self.assertIsInstance(matches[0][0], ast.ClassDef)
        self.assertIsInstance(matches[1][0], ast.ClassDef)

        # check lines
        self.assertEqual(matches[0][1], 1)
        self.assertEqual(matches[1][1], 9)

    def test_methods(self):
        matches = list(self.m.match('class def', self.filepath('classes.py')))
        self.assertEqual(len(matches), 2)

        # check instances
        self.assertIsInstance(matches[0][0], ast.FunctionDef)
        self.assertIsInstance(matches[1][0], ast.FunctionDef)

        # check lines
        self.assertEqual(matches[0][1], 2)
        self.assertEqual(matches[1][1], 5)

    def test_methods_by_name(self):
        matches1 = list(self.m.match('class def[name=baz]',
                        self.filepath('classes.py')))
        matches2 = list(self.m.match('class def[name!=baz]',
                        self.filepath('classes.py')))

        self.assertEqual(len(matches1), 1)
        self.assertEqual(matches1[0][1], 5)

        self.assertEqual(len(matches2), 1)
        self.assertEqual(matches2[0][1], 2)

    def test_import(self):
        matches = list(self.m.match('import', self.filepath('imports.py')))

        self.assertEqual(len(matches), 4)

        # check instances
        self.assertIsInstance(matches[0][0], ast.ImportFrom)
        self.assertIsInstance(matches[1][0], ast.ImportFrom)
        self.assertIsInstance(matches[2][0], ast.Import)
        self.assertIsInstance(matches[3][0], ast.Import)

    def test_import_from(self):
        matches = list(self.m.match('import[from=foo]',
                       self.filepath('imports.py')))

        self.assertEqual(len(matches), 2)

        # check instances
        self.assertIsInstance(matches[0][0], ast.ImportFrom)
        self.assertIsInstance(matches[1][0], ast.ImportFrom)

        # check lines
        self.assertEqual(matches[0][1], 1)
        self.assertEqual(matches[1][1], 2)

    def test_import_not_from(self):
        matches = list(self.m.match('import:not([from=foo])',
                       self.filepath('imports.py')))

        self.assertEqual(len(matches), 2)

        # check instances
        self.assertIsInstance(matches[0][0], ast.Import)
        self.assertIsInstance(matches[1][0], ast.Import)

    def test_import_name(self):
        matches = list(self.m.match('import[name=example2]',
                       self.filepath('imports.py')))

        self.assertEqual(len(matches), 1)

        matches = list(self.m.match('import[name=bar], import[name=bar2]',
                       self.filepath('imports.py')))

        self.assertEqual(len(matches), 2)

    def test_import_multiple(self):
        matches1 = list(self.m.match('import[name=xyz]',
                        self.filepath('imports.py')))

        matches2 = list(self.m.match('import[name=xyz][name=bar2]',
                        self.filepath('imports.py')))

        self.assertEqual(len(matches1), 1)
        self.assertEqual(len(matches2), 1)


unittest.main(failfast=True)