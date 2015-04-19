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


class Test_BaseBuilderClass(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.error_message = "sugar.Function_BaseBuilder only can be used under a "\
                             "context manager."
    # required syntax

    def test_mandatory_end_property(self):
        error_message = "missing 'end' property. You must get the '.end' "\
                        "property at the final of the method chaining."
        with self.assertRaisesRegex(SyntaxError, error_message):
            with sugar._BaseBuilder() as let:
                let('')

    def test_mandatory_context_manager(self):
        is_as = sugar._BaseBuilder()
        with self.assertRaisesRegex(SyntaxError, self.error_message):
            is_as.end

    # __call__ method

    def test_context_manager_Function(self):
        with sugar._BaseBuilder() as let:
            function = let('').end
        self.assertTrue(isinstance(function, types.FunctionType))

    def test_basic_function_source_code(self):
        with sugar._BaseBuilder() as let:
            let('docstring').end

        expected = "def function():\n" \
                   " 'docstring'\n" \
                   " yield \n"
        self.assertEqual(expected, let.source)

    def test_mandatory_context_manager_with_the__call__method(self):
        is_as = sugar._BaseBuilder()
        with self.assertRaisesRegex(SyntaxError, self.error_message):
            is_as('')

    # takes method

    def test_signature_builded_by_takes_method(self):
        local = 'a local variable'
        with sugar._BaseBuilder() as let:
            let(
                'function that add two numbers.'
            ).takes(
                ('a', 'as a number'),
                ('b', 'as another number'),
                ('local', 'an argument named "local"'),
                ('GLOBAL_VARIABLE', 'argument named "GLOBAL_VARIABLE"')
            ).end
        expected = "def function(a: 'as a number', b: 'as another number', " \
                                 "local: 'an argument named \"local\"', " \
                                 "GLOBAL_VARIABLE: 'argument named "\
                                 "\"GLOBAL_VARIABLE\"'):\n"\
                   " 'function that add two numbers.'\n" \
                   " yield \n"
        self.assertEqual(expected, let.source)

    def test_that_takes_method_fill_the_global_namespace(self):
        with sugar._BaseBuilder() as let:
            let('').takes(('a', '')).end
            self.assertTrue(isinstance(a, sugar.Expression))

    def test_takes_method_clear_the_var_from_the_global_namespace(self):
        with sugar._BaseBuilder() as let:
            let('').takes(('b', '')).end
        with self.assertRaisesRegex(NameError, "name 'b' is not defined"):
            b

    def test_takes_method_restore_the_global_variable_value(self):
        with sugar._BaseBuilder() as let:
            let('').takes(('GLOBAL_VARIABLE', '')).end
        self.assertEqual(GLOBAL_VARIABLE, 'original value')

    def test_mandatory_context_manager_with_takes_method(self):
        is_as = sugar._BaseBuilder()
        with self.assertRaisesRegex(SyntaxError, self.error_message):
            is_as.takes()

    # returns method

    def test_returns_method(self):
        with sugar._BaseBuilder() as let:
            let('').returns('the volume of the cylinder').end
        expected = "def function() -> 'the volume of the cylinder':\n"\
                   " yield \n"
        self.assertEqual(expected, let.source)

    def test_mandatory_context_manager_with_returns_method(self):
        is_as = sugar._BaseBuilder()
        with self.assertRaisesRegex(SyntaxError, self.error_message):
            is_as.returns('')

    # consts method

    def test_expression_builded_by_consts_method(self):
        with sugar._BaseBuilder() as let:
            let('').consts(PI=3.14, e=2.72).do(PI*e).end
        self.assertTrue(" e = 2.72\n" in let.source)
        self.assertTrue(" PI = 3.14\n" in let.source)
        self.assertTrue(" yield PI*(e)\n" in let.source)

    def test_consts_method_fill_the_global_namespace(self):
        with sugar._BaseBuilder() as let:
            let('').consts(a='').end
            self.assertTrue(isinstance(a, sugar.Expression))

    def test_consts_method_clear_the_var_from_the_global_namespace(self):
        with sugar._BaseBuilder() as let:
            let('').consts(b='').end
        with self.assertRaisesRegex(NameError, "name 'b' is not defined"):
            b

    def test_consts_method_restore_the_global_variable_value(self):
        with sugar._BaseBuilder() as let:
            let('').consts(GLOBAL_VARIABLE='').end
        self.assertEqual(GLOBAL_VARIABLE, 'original value')

    def test_mandatory_context_manager_with_consts_method(self):
        is_as = sugar._BaseBuilder()
        with self.assertRaisesRegex(SyntaxError, self.error_message):
            is_as.consts(a=1)

    @unittest.skip('unimplemented')
    def test_ValueError_if_pass_a_function_as_value(self):
        pass

    @unittest.skip('unimplemented')
    def test_ValueError_if_pass_lambda_function_as_value(self):
        pass

    @unittest.skip('unimplemented')
    def test_ValueError_if_pass_a_funciton_maked_with_Build_class(self):
        pass

    @unittest.skip('unimplemented')
    def test_ValueError_if_pass_a_generator(self):
        pass

    # do method

    def test_do_method(self):
        with sugar._BaseBuilder() as let:
            let(
                'function that add two numbers.'
            ).takes(
                ('a', 'as a number'),
                ('b', 'as another number'),
            ).do(
                a + b
            ).end
        expected = "def function(a: 'as a number', b: 'as another number'):\n"\
                   " 'function that add two numbers.'\n" \
                   " yield a+(b)\n"
        self.assertEqual(expected, let.source)

    def test_do_method_with_an_regular_object(self):
        with sugar._BaseBuilder() as let:
            let('').do(None).end
        expected = "def function():\n" \
                   " yield None\n"
        self.assertEqual(expected, let.source)

    def test_mandatory_context_manager_with_do_method(self):
        is_as = sugar._BaseBuilder()
        with self.assertRaisesRegex(SyntaxError, self.error_message):
            is_as.do(None)

    # method calling order

    @unittest.skip('unimplemented')
    def test__call__before_take(self):
        pass

    @unittest.skip('unimplemented')
    def test__call__before_returns(self):
        pass

    @unittest.skip('unimplemented')
    def test__call__before_consts(self):
        pass

    @unittest.skip('unimplemented')
    def test__call__before_do(self):
        pass

    @unittest.skip('unimplemented')
    def test_take_before_returns(self):
        pass

    @unittest.skip('unimplemented')
    def test_take_before_consts(self):
        pass

    @unittest.skip('unimplemented')
    def test_take_before_do(self):
        pass

    @unittest.skip('unimplemented')
    def test_returns_before_consts(self):
        pass

    @unittest.skip('unimplemented')
    def test_returns_before_do(self):
        pass

    @unittest.skip('unimplemented')
    def test_consts_before_do(self):
        pass

    # can not call each method twice or more

    @unittest.skip('unimplemented')
    def test_RuntimeError_if__call__method_is_called_twice(self):
        pass

    @unittest.skip('unimplemented')
    def test_RuntimeError_if_take_method_is_called_twice(self):
        pass

    @unittest.skip('unimplemented')
    def test_RuntimeError_if_returs_method_is_called_twice(self):
        pass

    @unittest.skip('unimplemented')
    def test_RuntimeError_if_consts_method_is_called_twice(self):
        pass

    @unittest.skip('unimplemented')
    def test_RuntimeError_if_do_method_is_called_twice(self):
        pass


@unittest.skip('unimplemented')
class TestBuildScope(unittest.TestCase):
    def test_RuntimeError_if_Build_is_called_in_a_local_scope_function(self):
        pass

    def test_RuntimeError_if_Build_is_called_in_a_local_scope_class(self):
        pass


if __name__ == '__main__':
    unittest.main()
