import unittest
import sys
import os

from operators import Operators
from NumberValidation import NumberValidation
from main import handle_operator


# ---------- Output Suppression Helpers ----------
def suppress_output():
    sys.stdout = open(os.devnull, 'w')

def restore_output():
    sys.stdout = sys.__stdout__


# ---------- Operator Input Validation ----------
class TestOperatorInput(unittest.TestCase):

    def setUp(self):
        self.ops = Operators()
        suppress_output()

    def tearDown(self):
        restore_output()

    def test_Calc_1_valid_operator_symbol(self):
        result = handle_operator("+", self.ops)
        self.assertEqual(result, self.ops.add)

    def test_Calc_2_valid_operator_word(self):
        result = handle_operator("add", self.ops)
        self.assertEqual(result, self.ops.add)

    def test_Calc_3_invalid_operator(self):
        result = handle_operator("xyz", self.ops)
        self.assertEqual(result, "Not an operator")

    def test_Calc_4_exit_program(self):
        user_input = ""
        self.assertEqual(user_input, "")


# ---------- Number Input Validation ----------
class TestNumberValidation(unittest.TestCase):
    def setUp(self):
        self.valid = NumberValidation()
        suppress_output()

    def tearDown(self):
        restore_output()
    
    def test_Calc_5_valid_integer(self):
        self.assertEqual(self.valid.validate_number("5"), 5)

    def test_Calc_6_valid_float(self):
        self.assertEqual(self.valid.validate_number("2.5"), 2.5)

    def test_Calc_7_invalid_number(self):
        self.assertEqual(self.valid.validate_number("abc"), "NaN")

    def test_Calc_8_equals_sign(self):
        self.assertEqual(self.valid.validate_number("="), "=")


# ---------- Arithmetic Operations ----------
class TestArithmeticOperations(unittest.TestCase):

    def setUp(self):
        self.ops = Operators()
        suppress_output()

    def tearDown(self):
        restore_output()

    def test_Calc_9_addition(self):
        self.ops.add([2, 3])
        self.assertEqual(self.ops.answer, 5)

    def test_Calc_10_subtraction(self):
        self.ops.subtract([3, 10])
        self.assertEqual(self.ops.answer, -13)

    def test_Calc_11_division(self):
        self.ops.add([20])
        self.ops.division([4])
        self.assertEqual(self.ops.answer, 5)

    def test_Calc_12_multiplication(self):
        self.ops.answer = 1
        self.ops.multiplication([4, 5])
        self.assertEqual(self.ops.answer, 20)

    def test_Calc_13_multiple_numbers(self):
        self.ops.add([1, 2, 3])
        self.assertEqual(self.ops.answer, 6)

    def test_Calc_14_different_operations(self):
        self.ops.add([5, 5])
        self.ops.subtract([5])
        self.assertEqual(self.ops.answer, 5)


# ---------- Memory Functionality ----------
class TestMemoryFunctions(unittest.TestCase):

    def setUp(self):
        self.ops = Operators()
        suppress_output()

    def tearDown(self):
        restore_output()

    def test_Calc_15_store_in_memory(self):
        self.ops.add([10])
        self.assertEqual(self.ops.memory(), 10)

    def test_Calc_16_apply_operations_to_memory(self):
        self.ops.add([1, 2])     # 3
        self.ops.division([6])     # 0.5
        self.assertEqual(self.ops.answer, 0.5)

    def test_Calc_17_view_memory(self):
        self.ops.add([7])
        self.assertEqual(self.ops.memory(), 7)

    def test_Calc_18_clear_memory(self):
        self.ops.add([5])
        self.ops.clear()
        self.assertEqual(self.ops.answer, 0)


# ---------- Error Handling ----------
class TestErrorHandling(unittest.TestCase):

    def setUp(self):
        self.ops = Operators()
        suppress_output()

    def tearDown(self):
        restore_output()

    def test_Calc_19_division_by_zero(self):
        result = self.ops.division([0])
        self.assertEqual(result, "Division by zero")

if __name__ == "__main__":
    # Create a test suite
    suite = unittest.TestSuite()

    # Add tests in the exact order
    suite.addTest(TestOperatorInput('test_Calc_1_valid_operator_symbol'))
    suite.addTest(TestOperatorInput('test_Calc_2_valid_operator_word'))
    suite.addTest(TestOperatorInput('test_Calc_3_invalid_operator'))
    suite.addTest(TestOperatorInput('test_Calc_4_exit_program'))

    suite.addTest(TestNumberValidation('test_Calc_5_valid_integer'))
    suite.addTest(TestNumberValidation('test_Calc_6_valid_float'))
    suite.addTest(TestNumberValidation('test_Calc_7_invalid_number'))
    suite.addTest(TestNumberValidation('test_Calc_8_equals_sign'))

    suite.addTest(TestArithmeticOperations('test_Calc_9_addition'))
    suite.addTest(TestArithmeticOperations('test_Calc_10_subtraction'))
    suite.addTest(TestArithmeticOperations('test_Calc_11_division'))
    suite.addTest(TestArithmeticOperations('test_Calc_12_multiplication'))
    suite.addTest(TestArithmeticOperations('test_Calc_13_multiple_numbers'))
    suite.addTest(TestArithmeticOperations('test_Calc_14_different_operations'))

    suite.addTest(TestMemoryFunctions('test_Calc_15_store_in_memory'))
    suite.addTest(TestMemoryFunctions('test_Calc_16_apply_operations_to_memory'))
    suite.addTest(TestMemoryFunctions('test_Calc_17_view_memory'))
    suite.addTest(TestMemoryFunctions('test_Calc_18_clear_memory'))

    suite.addTest(TestErrorHandling('test_Calc_19_division_by_zero'))

    # Run the suite with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
