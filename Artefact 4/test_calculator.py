import pytest  # For running tests
from bidmas import Calculator  # Import the Calculator class
import math

# Class to test calculator functions
class TestCalculator:

    def setup_method(self):
        self.calc = Calculator()  # Create calculator instance before each test

    # === Basic arithmetic tests ===
    def test_calc_01_addition(self):
        assert self.calc.tokenise_expression("1+1") == 2  # Test addition

    def test_calc_02_subtraction(self):
        assert self.calc.tokenise_expression("2-5") == -3  # Test subtraction

    def test_calc_03_unary_subtraction(self):
        assert self.calc.tokenise_expression("2--5") == 7  # Test unary minus

    def test_calc_04_multiplication(self):
        assert self.calc.tokenise_expression("2*5") == 10  # Test multiplication

    def test_calc_05_division(self):
        assert self.calc.tokenise_expression("20/4") == 5  # Test division

    def test_calc_06_division_error(self):
        with pytest.raises(ZeroDivisionError):  # Expect ZeroDivisionError
            self.calc.tokenise_expression("5/0")

    # === Exponentiation tests ===
    def test_calc_07_exponentiation(self):
        assert self.calc.tokenise_expression("2**3") == 8  # Test power operator

    def test_calc_08_exponentiation_zero(self):
        assert self.calc.tokenise_expression("5**0") == 1  # Any number^0 = 1

    def test_calc_09_exponentiation_one(self):
        assert self.calc.tokenise_expression("1**100") == 1  # 1^n = 1

    # === Sine tests ===
    def test_calc_10_sin_radians(self):
        self.calc.angle_mode = True  # Set radians
        assert self.calc.tokenise_expression("sin(pi/2)") == 1.0

    def test_calc_11_sin_degrees(self):
        self.calc.angle_mode = False  # Set degrees
        assert self.calc.tokenise_expression("sin(90)") == 1.0
        
    def test_calc_12_arcsin_radians(self):
        self.calc.angle_mode = True
        assert self.calc.tokenise_expression("arcsin(1)") == round(math.pi/2,3)
    def test_calc_13_arcsin_degrees(self):
        self.calc.angle_mode = False
        assert self.calc.tokenise_expression("arcsin(1)") == 90

    # === Cosine tests ===
    def test_calc_14_cos_radians(self):
        self.calc.angle_mode = True
        assert self.calc.tokenise_expression("cos(pi/2)") == 0.0

    def test_calc_15_cos_degrees(self):
        self.calc.angle_mode = False
        assert self.calc.tokenise_expression("cos(90)") == 0.0
        
    def test_calc_16_arcos_radians(self):
        self.calc.angle_mode = True
        assert self.calc.tokenise_expression("arccos(0)") == round(math.pi/2,3)
    
    def test_calc_17_arcos_degrees(self):
        self.calc.angle_mode = False
        assert self.calc.tokenise_expression("arccos(0)") == 90

    # === Tangent tests ===
    def test_calc_18_tan_radians(self):
        self.calc.angle_mode = True
        assert self.calc.tokenise_expression("tan(pi/4)") == 1.0

    def test_calc_19_tan_degrees(self):
        self.calc.angle_mode = False
        assert self.calc.tokenise_expression("tan(45)") == 1.0
        
    def test_calc_20_arctan_radians(self):
        self.calc.angle_mode = True
        assert self.calc.tokenise_expression("arctan(1)") == round(math.pi/4,3)
    
    def test_calc_21_arctan_degrees(self):
        self.calc.angle_mode = False
        assert self.calc.tokenise_expression("arctan(1)") == 45
        

    # === Logarithm tests ===
    def test_calc_22_ln(self):
        assert self.calc.tokenise_expression("ln(e)") == 1.0  # Natural log

    def test_calc_23_log_base10(self):
        assert self.calc.tokenise_expression("log(100)") == 2.0  # Base 10 log

    def test_calc_24_log_baseN(self):
        assert self.calc.tokenise_expression("log_n(8, 2)") == 3.0  # Custom base log
        
    # === Root tests ===
    
    def test_calc_25_sqrt(self):
        assert self.calc.tokenise_expression("sqrt(4)") == 2.0
        
    def test_calc_26_cbrt(self):
        assert self.calc.tokenise_expression("cbrt(27)") == 3.0
        
    def test_calc_27_nrt(self): # Nth root
        assert self.calc.tokenise_expression("n_rt(4,2)") == 2.0
        
    # Run all tests
    def test_calculator(self):
        pytest.main(["-v"])  # Run pytest in verbose mode

# Run tests if executed directly
if __name__ == "__main__":
    test = TestCalculator()
    test.test_calculator()

