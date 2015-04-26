import unittest
import types

import sugar


GLOBAL = 'original value'


class ExpressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.var = sugar.Expression('self.var')

    # Left operators

    def test_left_add_operator(self):
        self.assertEqual((self.var + 2).__expr__, 'self.var+(2)')

    def test_left_and_operator(self):
        self.assertEqual((self.var & 2).__expr__, 'self.var&(2)')

    def test_left_div_operator(self):
        self.assertEqual((self.var / 2).__expr__, 'self.var/(2)')

    def test_left_eq_operator(self):
        self.assertEqual((self.var == 2).__expr__, 'self.var==(2)')

    def test_left_floordiv_operator(self):
        self.assertEqual((self.var // 2).__expr__, 'self.var//(2)')

    def test_left_ge_operator(self):
        self.assertEqual((self.var >= 2).__expr__, 'self.var>=(2)')

    def test_left_gt_operator(self):
        self.assertEqual((self.var > 2).__expr__, 'self.var>(2)')

    def test_left_le_operator(self):
        self.assertEqual((self.var <= 2).__expr__, 'self.var<=(2)')

    def test_left_lshift_operator(self):
        self.assertEqual((self.var << 2).__expr__, 'self.var<<(2)')

    def test_left_lt_operator(self):
        self.assertEqual((self.var < 2).__expr__, 'self.var<(2)')

    def test_left_matmul_operator(self):
        self.assertEqual((self.var @ 2).__expr__, 'self.var@(2)')

    def test_left_mod_operator(self):
        self.assertEqual((self.var % 2).__expr__, 'self.var%(2)')

    def test_left_mul_operator(self):
        self.assertEqual((self.var * 2).__expr__, 'self.var*(2)')

    def test_left_ne_operator(self):
        self.assertEqual((self.var != 2).__expr__, 'self.var!=(2)')

    def test_left_or_operator(self):
        self.assertEqual((self.var | 2).__expr__, 'self.var|(2)')

    def test_left_pow_operator(self):
        self.assertEqual((self.var ** 2).__expr__, 'self.var**(2)')

    def test_left_rshift_operator(self):
        self.assertEqual((self.var >> 2).__expr__, 'self.var>>(2)')

    def test_left_sub_operator(self):
        self.assertEqual((self.var - 2).__expr__, 'self.var-(2)')

    def test_left_truediv_operator(self):
        self.assertEqual((self.var / 2).__expr__, 'self.var/(2)')

    def test_left_xor_operator(self):
        self.assertEqual((self.var ^ 2).__expr__, 'self.var^(2)')

    # Right operators

    def test_right_radd_operator(self):
        self.assertEqual((2 + self.var).__expr__, '(2)+self.var')

    def test_right_rand_operator(self):
        self.assertEqual((2 & self.var).__expr__, '(2)&self.var')

    def test_right_rdiv_operator(self):
        self.assertEqual((2 / self.var).__expr__, '(2)/self.var')

    def test_rflooright_rfloordiv_operator(self):
        self.assertEqual((2 // self.var).__expr__, '(2)//self.var')

    def test_rlsright_rlshift_operator(self):
        self.assertEqual((2 << self.var).__expr__, '(2)<<self.var')

    def test_rmaright_rmatmul_operator(self):
        self.assertEqual((2 @ self.var).__expr__, '(2)@self.var')

    def test_right_rmod_operator(self):
        self.assertEqual((2 % self.var).__expr__, '(2)%self.var')

    def test_right_rmul_operator(self):
        self.assertEqual((2 * self.var).__expr__, '(2)*self.var')

    def test_right_ror_operator(self):
        self.assertEqual((2 | self.var).__expr__, '(2)|self.var')

    def test_right_rpow_operator(self):
        self.assertEqual((2 ** self.var).__expr__, '(2)**self.var')

    def test_right_rrshift_operator(self):
        self.assertEqual((2 >> self.var).__expr__, '(2)>>self.var')

    def test_right_rsub_operator(self):
        self.assertEqual((2 - self.var).__expr__, '(2)-self.var')

    def test_right_rtruediv_operator(self):
        self.assertEqual((2 / self.var).__expr__, '(2)/self.var')

    def test_right_rxor_operator(self):
        self.assertEqual((2 ^ self.var).__expr__, '(2)^self.var')

    # Unary operators

    def test_invert_unary_operator(self):
        self.assertEqual((~self.var).__expr__, '~(self.var)')

    def test_neg_unary_operator(self):
        self.assertEqual((-self.var).__expr__, '-(self.var)')

    def test_pos_unary_operator(self):
        self.assertEqual((+self.var).__expr__, '+(self.var)')

    # Built in functions

    def test_abs_built_in_function(self):
        self.assertEqual((abs(self.var)).__expr__, 'abs(self.var)')

    def test_round_built_in_function(self):
        self.assertEqual((round(self.var, 2)).__expr__, 'round(self.var, 2)')

    def test_reversed_built_in_function(self):
        self.assertEqual(reversed(self.var).__expr__, 'reversed(self.var)')

    # Attribute and item access

    def test__getattr__method(self):
        self.assertEqual(self.var.attribute.__expr__, '(self.var).attribute')
        attribute = getattr(self.var, 'attribute')
        self.assertEqual(attribute.__expr__, '(self.var).attribute')

    def test__getitem__method(self):
        self.assertEqual(self.var[1].__expr__, "(self.var)[1]")
        self.assertEqual(self.var[1, 2].__expr__, "(self.var)[(1, 2)]")
        self.assertEqual(self.var['key'].__expr__, "(self.var)['key']")

    def test__repr__method(self):
        self.assertEqual(repr(self.var), "self.var")


# This class is not runned if not inherit from unittest.TestCase
# class FailedExpressionBehaviours(unittest.TestCase):
class FailedExpressionBehaviours:
    @classmethod
    def setUpClass(self):
        self.var = sugar.Expression('self.var')

    @unittest.expectedFailure
    def test_len_built_in_function(self):
        "TypeError: 'Expression' object cannot let interpreted as an integer"
        self.assertEqual(len(self.var).__expr__, 'len(self.var)')

    @unittest.expectedFailure
    def test_iter_built_in_function(self):
        """TypeError: iter() returned non-iterator of type 'Expression'"""
        self.assertEqual(iter(self.var).__expr__, 'iter(self.var)')

    @unittest.expectedFailure
    def test_contains_built_in_function(self):
        "TypeError: 'Expression' object cannot let interpreted as an integer"
        self.assertEqual(('item' in self.var).__expr__,
                         "('item' in self.var)")

    @unittest.expectedFailure
    def test_isinstance_built_in_function(self):
        """AttributeError: 'bool' object has no attribute '__expr__'"""
        self.assertEqual(isinstance(self.var, type).__expr__,
                         'isinstance(self.var, type)')

    @unittest.expectedFailure
    def test_issubclass_built_in_function(self):
        """TypeError: issubclass() arg 1 must let a class"""
        self.assertEqual(issubclass(self.var, type).__expr__,
                         'issubclass(self.var, type)')


class TestLetClass(unittest.TestCase):
    # Do class

    def test_basic_source_code(self):
        obtained = sugar.Let(lambda: sugar.Do(None))
        expected = "def function():\n"\
                   " yield None\n"
        self.assertEqual(expected, obtained.source)

    def test_basic_operation(self):
        x, y = sugar.Expression('x'), sugar.Expression('y')
        obtained = sugar.Let(lambda: sugar.Do(x + y))
        expected = "def function():\n"\
                   " yield x+(y)\n"
        self.assertEqual(expected, obtained.source)

    # signature

    def test_signature(self):
        obtained = sugar.Let(lambda x, y: sugar.Do(x+y))
        expected = "def function(x, y):\n"\
                   " yield x+(y)\n"
        self.assertEqual(expected, obtained.source)

    def test_signature_with_default_arguments(self):
        obtained = sugar.Let(lambda x, y=1: sugar.Do(x-y))
        expected = "def function(x, y=1):\n"\
                   " yield x-(y)\n"
        self.assertEqual(expected, obtained.source)

    # where method

    def test_where_method_without_global_or_local_variables(self):
        obtained = sugar.Let(lambda: sugar.Do(PI*e).where(PI=3.14, e=2.72))
        self.assertTrue(" e = 2.72\n" in obtained.source)
        self.assertTrue(" PI = 3.14\n" in obtained.source)
        self.assertTrue(" yield PI*(e)\n" in obtained.source)

    def test_where_method_with_global_variables(self):
        obtained = sugar.Let(lambda:
            sugar.Do(GLOBAL).where(GLOBAL='inner GLOBAL')
        )
        expected = "def function():\n"\
                   " GLOBAL = 'inner GLOBAL'\n"\
                   " yield GLOBAL\n"
        self.assertEqual(expected, obtained.source)

    def test_where_method_with_local_variables(self):
        LOCAL = 'local variable'
        obtained = sugar.Let(lambda:
                             sugar.Do(LOCAL).where(LOCAL='inner LOCAL'))
        expected = "def function():\n"\
                   " LOCAL = 'inner LOCAL'\n"\
                   " yield LOCAL\n"
        self.assertEqual(expected, obtained.source)

    def test_where_method_with_global_and_local_variables(self):
        LOCAL = 'local variable'
        obtained = sugar.Let(lambda:
            sugar.Do(
                LOCAL*GLOBAL
            ).where(
                LOCAL=10,
                GLOBAL=50
            )
        )
        self.assertTrue("LOCAL = 10\n" in obtained.source)
        self.assertTrue("GLOBAL = 50\n" in obtained.source)
        self.assertTrue("yield LOCAL*(GLOBAL)\n" in obtained.source)


@unittest.skip('unimplemented')
class Test_error_Function(unittest.TestCase):
    def test_do_method_should_raise_an_exception(self):
        pass


@unittest.skip('unimplemented')
class Test_thyself_Function(unittest.TestCase):
    def test_recursive_function_with_the_thyself_function(self):
        pass


if __name__ == '__main__':
    unittest.main()
