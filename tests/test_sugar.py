import unittest

import sugar

class ExpressionTest(unittest.TestCase):
    def test_bynary_left_operators(self):
        x = sugar.Expression('x')
        add = x+2
        and_ = x&2
        div = x/2
        eq = x==2
        floordiv = x//2
        ge = x>=2
        gt = x>2
        le = x<=2
        lshift = x<<2
        lt = x<2
        matmul = x@2
        mod = x%2
        mul = x*2
        ne = x!=2
        or_ = x|2
        pow = x**2
        rshift = x>>2
        sub = x-2
        truediv = x/2
        xor = x^2

        self.assertEqual(add.expression, 'x+(2)')
        self.assertEqual(and_.expression, 'x&(2)')
        self.assertEqual(div.expression, 'x/(2)')
        self.assertEqual(eq.expression, 'x==(2)')
        self.assertEqual(floordiv.expression, 'x//(2)')
        self.assertEqual(ge.expression, 'x>=(2)')
        self.assertEqual(gt.expression, 'x>(2)')
        self.assertEqual(le.expression, 'x<=(2)')
        self.assertEqual(lshift.expression, 'x<<(2)')
        self.assertEqual(lt.expression, 'x<(2)')
        self.assertEqual(matmul.expression, 'x@(2)')
        self.assertEqual(mod.expression, 'x%(2)')
        self.assertEqual(mul.expression, 'x*(2)')
        self.assertEqual(ne.expression, 'x!=(2)')
        self.assertEqual(or_.expression, 'x|(2)')
        self.assertEqual(pow.expression, 'x**(2)')
        self.assertEqual(rshift.expression, 'x>>(2)')
        self.assertEqual(sub.expression, 'x-(2)')
        self.assertEqual(truediv.expression, 'x/(2)')
        self.assertEqual(xor.expression, 'x^(2)')

    def test_bynary_right_operators(self):
        x = sugar.Expression('x')
        radd = 2+x
        rand = 2&x
        rdiv = 2/x
        rfloordiv = 2//x
        rlshift = 2<<x
        rmatmul = 2@x
        rmod = 2%x
        rmul = 2*x
        ror_ = 2|x
        rpow = 2**x
        rrshift = 2>>x
        rsub = 2-x
        rtruediv = 2/x
        rxor = 2^x

        self.assertEqual(radd.expression, '(2)+x')
        self.assertEqual(rand.expression, '(2)&x')
        self.assertEqual(rdiv.expression, '(2)/x')
        self.assertEqual(rfloordiv.expression, '(2)//x')
        self.assertEqual(rlshift.expression, '(2)<<x')
        self.assertEqual(rmatmul.expression, '(2)@x')
        self.assertEqual(rmod.expression, '(2)%x')
        self.assertEqual(rmul.expression, '(2)*x')
        self.assertEqual(ror_.expression, '(2)|x')
        self.assertEqual(rpow.expression, '(2)**x')
        self.assertEqual(rrshift.expression, '(2)>>x')
        self.assertEqual(rsub.expression, '(2)-x')
        self.assertEqual(rtruediv.expression, '(2)/x')
        self.assertEqual(rxor.expression, '(2)^x')

    def test_unary_operators(self):
        x = sugar.Expression('x')
        invert = ~x
        neg = -x
        pos = +x

        self.assertEqual(invert.expression, '~(x)')
        self.assertEqual(neg.expression, '-(x)')
        self.assertEqual(pos.expression, '+(x)')
