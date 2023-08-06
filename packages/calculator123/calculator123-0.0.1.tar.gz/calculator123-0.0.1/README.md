# Calculator Package

This package provides a Calculator class that performs basic arithmetic operations and memory manipulation.

## Installation

Install the package using pip:

```bash
pip install calculator-package

### Usage

1. Import the Calculator class from the calculator module:

```python
from calculator import Calculator

Usage

from calculator_package.calculator import Calculator

# Create a Calculator instance
calculator = Calculator()

# Perform addition
result = calculator.add(2, 3)
print(result)  # Output: 5

# Perform subtraction
result = calculator.subtract(5, 2)
print(result)  # Output: 3

# Perform multiplication
result = calculator.multiply(4, 2)
print(result)  # Output: 8

# Perform division
result = calculator.divide(10, 5)
print(result)  # Output: 2.0

License

This project is licensed under the MIT License.

class Calculator:
    """
    A simple calculator class that performs basic arithmetic operations and memory manipulation.
    """

    def __init__(self):
        """
        Initialize the Calculator with memory set to 0.
        """
        self.memory = 0
    
    def add(self, num):
        """
        Add a number to the calculator's memory.
        
        Args:
            num (float): The number to be added.
        """
        self.memory += num
    
    def subtract(self, num):
        """
        Subtract a number from the calculator's memory.
        
        Args:
            num (float): The number to be subtracted.
        """
        self.memory -= num
    
    def multiply(self, num):
        """
        Multiply the calculator's memory by a number.
        
        Args:
            num (float): The number to multiply by.
        """
        self.memory *= num
    
    def divide(self, num):
        """
        Divide the calculator's memory by a number.
        
        Args:
            num (float): The number to divide by.
        
        Raises:
            ValueError: If `num` is 0.
        """
        if num != 0:
            self.memory /= num
        else:
            raise ValueError("Cannot divide by zero.")
    
    def root(self, n):
        """
        Calculate the nth root of the calculator's memory.
        
        Args:
            n (float): The root value.
        
        Raises:
            ValueError: If the calculator's memory is negative and `n` is even.
        """
        if self.memory >= 0 or n % 2 != 0:
            self.memory **= (1 / n)
        else:
            raise ValueError("Cannot calculate root of a negative number with an even root value.")
    
    def reset(self):
        """
        Reset the calculator's memory to 0.
        """
        self.memory = 0

Error Handling

The Calculator class includes error handling for certain scenarios:

Dividing by zero: If you attempt to divide the memory by zero, a ValueError will be raised.
Calculating the root of a negative number with an even root value: If you attempt to calculate the root of a negative number with an even root value, a ValueError will be raised.
Please ensure that you handle these exceptions appropriately in your code.

Testing

The package includes unit tests to ensure the basic functionality of the Calculator class. To run the tests, you can use the following command:
python -m unittest discover

