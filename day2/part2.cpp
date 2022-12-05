#include <iostream>
#include <fstream>

int main()
{
	std::ifstream input{"input.txt"};

	std::string direction;
	int distance;

	int horizontalPosition = 0;
	int aim = 0;
	int depth = 0;

	std::cout << std::boolalpha << true << false << '\n';

	while (input >> direction >> distance) {
		if (direction == "forward") {
			horizontalPosition += distance;
			depth += aim * distance;
		} else if (direction == "down") {
			aim += distance;
		} else if (direction == "up") {
			aim -= distance;
		}
	}

	std::cout << horizontalPosition * depth << std::endl;
}