import math
from typing import Callable, List, Tuple


NumberPair = Tuple[float, float]


def add(operands: NumberPair) -> float:
	left, right = operands
	return left + right


def subtract(operands: NumberPair) -> float:
	left, right = operands
	return left - right


def multiply(operands: NumberPair) -> float:
	left, right = operands
	return left * right


def divide(operands: NumberPair) -> float:
	left, right = operands
	if right == 0:
		raise ZeroDivisionError("Cannot divide by zero")
	return left / right


def power(operands: NumberPair) -> float:
	left, right = operands
	return left ** right


def modulo(operands: NumberPair) -> float:
	left, right = operands
	if right == 0:
		raise ZeroDivisionError("Cannot modulo by zero")
	return left % right


def square_root(value: float) -> float:
	if value < 0:
		raise ValueError("Cannot take the square root of a negative number")
	return math.sqrt(value)


def parse_float(prompt_text: str) -> float:
	while True:
		text = input(prompt_text)
		try:
			return float(text)
		except ValueError:
			print("Invalid number. Please try again.")


def compute_binary_operation(
	name: str,
	func: Callable[[NumberPair], float],
	history: List[str],
) -> None:
	left = parse_float("Enter first number: ")
	right = parse_float("Enter second number: ")
	try:
		result = func((left, right))
		entry = f"{name}: {left} and {right} = {result}"
		history.append(entry)
		print(entry)
	except Exception as error:
		print(f"Error: {error}")


def compute_square_root(history: List[str]) -> None:
	value = parse_float("Enter number: ")
	try:
		result = square_root(value)
		entry = f"sqrt: √{value} = {result}"
		history.append(entry)
		print(entry)
	except Exception as error:
		print(f"Error: {error}")


def print_menu() -> None:
	print("\nEnhanced Calculator")
	print("1) Add")
	print("2) Subtract")
	print("3) Multiply")
	print("4) Divide")
	print("5) Power (x^y)")
	print("6) Modulo (x % y)")
	print("7) Square Root")
	print("8) Show History")
	print("9) Clear History")
	print("0) Exit")


def main() -> None:
	history: List[str] = []
	operations: dict[str, Tuple[str, Callable[..., None]]] = {
		"1": ("add", lambda h=history: compute_binary_operation("add", add, h)),
		"2": ("subtract", lambda h=history: compute_binary_operation("subtract", subtract, h)),
		"3": ("multiply", lambda h=history: compute_binary_operation("multiply", multiply, h)),
		"4": ("divide", lambda h=history: compute_binary_operation("divide", divide, h)),
		"5": ("power", lambda h=history: compute_binary_operation("power", power, h)),
		"6": ("modulo", lambda h=history: compute_binary_operation("modulo", modulo, h)),
		"7": ("sqrt", compute_square_root),
	}

	while True:
		print_menu()
		choice = input("Choose an option: ").strip()
		if choice == "0":
			print("Goodbye!")
			break
		elif choice == "8":
			if not history:
				print("History is empty.")
			else:
				print("\nHistory:")
				for index, entry in enumerate(history, start=1):
					print(f"{index}. {entry}")
		elif choice == "9":
			history.clear()
			print("History cleared.")
		elif choice in operations:
			_, action = operations[choice]
			action(history)
		else:
			print("Invalid choice. Please try again.")


if __name__ == "__main__":
	main()


