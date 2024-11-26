#include "example.h"
#include <stdexcept>

/**
 * @file example.cpp
 * @brief Example implementation file to demonstrate Doxygen comments.
 *
 * This file contains example implementations of functions and classes
 * to demonstrate how to use Doxygen for generating documentation.
 */

namespace example
{
    /**
     * @brief Constructor for Calculator.
     */
    Calculator::Calculator() {}

    /**
     * @brief Adds two integers.
     *
     * This method takes two integers as input and returns their sum.
     *
     * @param a First integer.
     * @param b Second integer.
     * @return Sum of the two integers.
     */
    int Calculator::add(int a, int b)
    {
        return a + b;
    }

    /**
     * @brief Multiplies two integers.
     *
     * This method takes two integers as input and returns their product.
     *
     * @param a First integer.
     * @param b Second integer.
     * @return Product of the two integers.
     */
    int Calculator::multiply(int a, int b)
    {
        return a * b;
    }

    /**
     * @brief Performs an arithmetic operation.
     *
     * This method takes two integers and an operation type as input
     * and returns the result of the operation.
     *
     * @param a First integer.
     * @param b Second integer.
     * @param op Operation type.
     * @return Result of the arithmetic operation.
     */
    int Calculator::performOperation(int a, int b, Operation op)
    {
        switch (op)
        {
        case Operation::ADD:
            return add(a, b);
        case Operation::MULTIPLY:
            return multiply(a, b);
        case Operation::SUBTRACT:
            return a - b;
        case Operation::DIVIDE:
            if (b != 0)
            {
                return a / b;
            }
            else
            {
                // Handle division by zero
                throw std::invalid_argument("Division by zero");
            }
        default:
            throw std::invalid_argument("Invalid operation");
        }
    }
} // namespace example