#include <iostream>
#include <fstream>

int main()
{
	std::ifstream input{"input.txt"};

	std::string direction;
	int distance;

	int horizontalPosition = 0;
	int depth = 0;

	while (input >> direction >> distance) {
		if (direction == "forward") {
			horizontalPosition += distance;
		} else if (direction == "down") {
			depth += distance;
		} else if (direction == "up") {
			depth -= distance;
		}
	}

	std::cout << horizontalPosition * depth << std::endl;
}