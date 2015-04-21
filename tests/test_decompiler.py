import unittest
import ast
import dis

from sugar.decompiler import Code, Decompile


class TestStoreProperties(unittest.TestCase):
    def test_bytecode_property(self):
        decompiled = Code(lambda: None)
        self.assertTrue(isinstance(decompiled.bytecode, dis.Bytecode))

    def test_constants_property(self):
        decompiled = Code(lambda: "docstring")
        self.assertEqual(decompiled.constants, (None, 'docstring'))

    def test_enclosed_names_property(self):
        decompiled_1 = Code((lambda x: lambda: x)('enclosed'))
        self.assertEqual(decompiled_1.enclosed_names, ('x',))
        local_variable = 'local_variable'
        decompiled_2 = Code(lambda: local_variable)
        self.assertEqual(decompiled_2.enclosed_names, ('local_variable',))

    def test_global_names_property(self):
        decompiled = Code(lambda: takes)
        self.assertEqual(decompiled.global_names, ('takes',))


class TestMakeDocstring(unittest.TestCase):
    def test_docstring(self):
        expected = ast.parse('def f(): "docstring"')
        decompiled = Decompile(lambda: "docstring")
        self.assertEqual(ast.dump(expected), ast.dump(decompiled.module_node))


if __name__ == '__main__':
    unittest.main()
