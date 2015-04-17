import unittest
import types

import sugar


GLOBAL_VARIABLE = 'original value'


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


# This class is not runned if not inherit from unittest.TestCase
# class FailedExpressionBehaviours(unittest.TestCase):
class FailedExpressionBehaviours:
    @classmethod
    def setUpClass(self):
        self.var = sugar.Expression('self.var')

    @unittest.expectedFailure
    def test_len_built_in_function(self):
        "TypeError: 'Expression' object cannot be interpreted as an integer"
        self.assertEqual(len(self.var).__expr__, 'len(self.var)')

    @unittest.expectedFailure
    def test_iter_built_in_function(self):
        """TypeError: iter() returned non-iterator of type 'Expression'"""
        self.assertEqual(iter(self.var).__expr__, 'iter(self.var)')

    @unittest.expectedFailure
    def test_contains_built_in_function(self):
        "TypeError: 'Expression' object cannot be interpreted as an integer"
        self.assertEqual(('item' in self.var).__expr__,
                         "('item' in self.var)")

    @unittest.expectedFailure
    def test_isinstance_built_in_function(self):
        """AttributeError: 'bool' object has no attribute '__expr__'"""
        self.assertEqual(isinstance(self.var, type).__expr__,
                         'isinstance(self.var, type)')

    @unittest.expectedFailure
    def test_issubclass_built_in_function(self):
        """TypeError: issubclass() arg 1 must be a class"""
        self.assertEqual(issubclass(self.var, type).__expr__,
                         'issubclass(self.var, type)')


class TestDefineClass(unittest.TestCase):
    def test_mandatority_end_property(self):
        with self.assertRaisesRegex(TypeError,
                                    "'Define' object is not callable: "
                                    "missing '.end' at the ending of the "
                                    "function definition."):
            function= sugar.Define('')
            function()

    def test_that_let_method_push_and_remove_a_variable_from_globals(self):
        # push the 'a' variable in the global namespace
        define_object = sugar.Define(''
            ).let(
                a = '',
            )
        self.assertTrue('a' in globals())

        # remove a form the global namespace
        function = define_object.end
        self.assertFalse('a' in globals())

if __name__ == '__main__':
    unittest.main()
