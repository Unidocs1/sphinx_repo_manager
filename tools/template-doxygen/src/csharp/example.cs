using System;

/**
 * @file example.cs
 * @brief This file contains the definition of the Example namespace, which includes
 *        an enumeration for arithmetic operations, an interface for arithmetic methods,
 *        and a simple calculator class that implements these methods.
 */

namespace Example
{
    /// <summary>
    /// Arithmetic operations enumeration.
    /// This enum defines basic arithmetic operations.
    /// </summary>
    public enum Operation
    {
        ADD,      // Addition operation
        MULTIPLY, // Multiplication operation
        SUBTRACT, // Subtraction operation
        DIVIDE    // Division operation
    }

    /// <summary>
    /// Interface for arithmetic operations.
    /// This interface defines methods for basic arithmetic operations.
    /// </summary>
    public interface IArithmetic
    {
        /// <summary>
        /// Adds two integers.
        /// This method takes two integers as input and returns their sum.
        /// </summary>
        /// <param name="a">First integer.</param>
        /// <param name="b">Second integer.</param>
        /// <returns>Sum of the two integers.</returns>
        int Add(int a, int b);

        /// <summary>
        /// Multiplies two integers.
        /// This method takes two integers as input and returns their product.
        /// </summary>
        /// <param name="a">First integer.</param>
        /// <param name="b">Second integer.</param>
        /// <returns>Product of the two integers.</returns>
        int Multiply(int a, int b);
    }

    /// <summary>
    /// A simple calculator class.
    /// This class provides basic arithmetic operations.
    /// </summary>
    public class Calculator : IArithmetic
    {
        /// <summary>
        /// Constructor for Calculator.
        /// </summary>
        public Calculator()
        {
        }

        /// <summary>
        /// Adds two integers.
        /// This method takes two integers as input and returns their sum.
        /// </summary>
        /// <param name="a">First integer.</param>
        /// <param name="b">Second integer.</param>
        /// <returns>Sum of the two integers.</returns>
        public int Add(int a, int b)
        {
            return a + b;
        }

        /// <summary>
        /// Multiplies two integers.
        /// This method takes two integers as input and returns their product.
        /// </summary>
        /// <param name="a">First integer.</param>
        /// <param name="b">Second integer.</param>
        /// <returns>Product of the two integers.</returns>
        public int Multiply(int a, int b)
        {
            return a * b;
        }

        /// <summary>
        /// Performs an arithmetic operation.
        /// This method takes two integers and an operation type as input
        /// and returns the result of the operation.
        /// </summary>
        /// <param name="a">First integer.</param>
        /// <param name="b">Second integer.</param>
        /// <param name="op">Operation type.</param>
        /// <returns>Result of the arithmetic operation.</returns>
        /// <exception cref="DivideByZeroException">Thrown when attempting to divide by zero.</exception>
        /// <exception cref="ArgumentException">Thrown when an invalid operation type is provided.</exception>
        public int PerformOperation(int a, int b, Operation op)
        {
            switch (op)
            {
                case Operation.ADD:
                    return Add(a, b);
                case Operation.MULTIPLY:
                    return Multiply(a, b);
                case Operation.SUBTRACT:
                    return a - b;
                case Operation.DIVIDE:
                    if (b == 0)
                        throw new DivideByZeroException("Division by zero is not allowed.");
                    return a / b;
                default:
                    throw new ArgumentException("Invalid operation type.");
            }
        }
    }
}
