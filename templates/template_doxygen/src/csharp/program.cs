using System;

/**
 * @file example.cs
 * @brief This file contains a program class that demonstrates the usage of the 
 *        Calculator class. The Calculator class is defined in the Example namespace.
 */

namespace Example
{
    //// <summary>
    /// Main class to demonstrate the usage of Calculator.
    /// </summary>
    public class Program
    {
        /// <summary>
        /// Main method to demonstrate the usage of Calculator.
        /// </summary>
        /// <param name="args">Command-line arguments.</param>
        public static void Main(string[] args)
        {
            Calculator calc = new Calculator();
            int a = 10;
            int b = 5;

            Console.WriteLine("Addition: " + calc.PerformOperation(a, b, Operation.ADD));
            Console.WriteLine("Multiplication: " + calc.PerformOperation(a, b, Operation.MULTIPLY));
            Console.WriteLine("Subtraction: " + calc.PerformOperation(a, b, Operation.SUBTRACT));
            Console.WriteLine("Division: " + calc.PerformOperation(a, b, Operation.DIVIDE));
        }
    }
}
