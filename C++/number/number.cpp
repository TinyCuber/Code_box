#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    // Initialize the random number seed
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    // Generate a random number between 1 and 100
    int secretNumber = std::rand() % 100 + 1;
    int guess;
    int attempts = 0;

    std::cout << "Welcome to the number guessing game! I've already thought of a number between 1 and 100. You can start guessing now." << std::endl;

    do {
        std::cout << "Please enter your guess: ";
        std::cin >> guess;
        attempts++;

        if (guess > secretNumber) {
            std::cout << "Your guess is too high. Try again." << std::endl;
        } else if (guess < secretNumber) {
            std::cout << "Your guess is too low. Try again." << std::endl;
        } else {
            std::cout << "Congratulations! You guessed it right! You took " << attempts << " attempts in total." << std::endl;
        }
    } while (guess != secretNumber);

    return 0;
}