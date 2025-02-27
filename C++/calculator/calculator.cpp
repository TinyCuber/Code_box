#include <iostream>

int main() {
    double num1, num2;
    char operation;

    // Prompt the user to enter the first number
    std::cout << "Please enter the first number: ";
    std::cin >> num1;

    // Prompt the user to enter the operator
    std::cout << "Please enter the operator (+, -, *, /): ";
    std::cin >> operation;

    // Prompt the user to enter the second number
    std::cout << "Please enter the second number: ";
    std::cin >> num2;

    double result;

    // Perform the corresponding calculation based on the operator
    switch (operation) {
        case '+':
            result = num1 + num2;
            std::cout << num1 << " + " << num2 << " = " << result << std::endl;
            break;
        case '-':
            result = num1 - num2;
            std::cout << num1 << " - " << num2 << " = " << result << std::endl;
            break;
        case '*':
            result = num1 * num2;
            std::cout << num1 << " * " << num2 << " = " << result << std::endl;
            break;
        case '/':
            if (num2 != 0) {
                result = num1 / num2;
                std::cout << num1 << " / " << num2 << " = " << result << std::endl;
            } else {
                std::cout << "Error: The divisor cannot be zero." << std::endl;
            }
            break;
        default:
            std::cout << "Error: Invalid operator." << std::endl;
    }

    return 0;
}