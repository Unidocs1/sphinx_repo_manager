#ifndef EXAMPLE_H
#define EXAMPLE_H

/**
 * @file example.h
 * @brief Example header file to demonstrate Doxygen comments.
 *
 * This file contains example functions, classes, interfaces, and enums
 * to demonstrate how to use Doxygen for generating documentation.
 */

namespace example
{
    /**
     * @brief Arithmetic operations enumeration.
     *
     * This enum defines basic arithmetic operations.
     */
    enum class Operation
    {
        ADD,      /**< Addition operation */
        MULTIPLY, /**< Multiplication operation */
        SUBTRACT, /**< Subtraction operation */
        DIVIDE    /**< Division operation */
    };

    /**
     * @brief Interface for arithmetic operations.
     *
     * This interface defines methods for basic arithmetic operations.
     */
    class IArithmetic
    {
    public:
        /**
         * @brief Virtual destructor for IArithmetic.
         */
        virtual ~IArithmetic() {}

        /**
         * @brief Adds two integers.
         *
         * This method takes two integers as input and returns their sum.
         *
         * @param a First integer.
         * @param b Second integer.
         * @return Sum of the two integers.
         */
        virtual int add(int a, int b) = 0;

        /**
         * @brief Multiplies two integers.
         *
         * This method takes two integers as input and returns their product.
         *
         * @param a First integer.
         * @param b Second integer.
         * @return Product of the two integers.
         */
        virtual int multiply(int a, int b) = 0;
    };

    /**
     * @class Calculator
     * @brief A simple calculator class.
     *
     * This class provides basic arithmetic operations.
     */
    class Calculator : public IArithmetic
    {
    public:
        /**
         * @brief Constructor for Calculator.
         */
        Calculator();

        /**
         * @brief Adds two integers.
         *
         * This method takes two integers as input and returns their sum.
         *
         * @param a First integer.
         * @param b Second integer.
         * @return Sum of the two integers.
         */
        int add(int a, int b) override;

        /**
         * @brief Multiplies two integers.
         *
         * This method takes two integers as input and returns their product.
         *
         * @param a First integer.
         * @param b Second integer.
         * @return Product of the two integers.
         */
        int multiply(int a, int b) override;

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
        int performOperation(int a, int b, Operation op);
    };

} // namespace example

#endif // EXAMPLE_H