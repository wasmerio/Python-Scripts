import math


def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI from weight in kilograms and height in centimeters."""
    if not math.isfinite(weight_kg) or weight_kg <= 0:
        raise ValueError("Weight must be a finite number greater than zero.")
    if not math.isfinite(height_cm) or height_cm <= 0:
        raise ValueError("Height must be a finite number greater than zero.")

    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    """Return the standard adult BMI category for a BMI value."""
    if not math.isfinite(bmi) or bmi <= 0:
        raise ValueError("BMI must be a finite number greater than zero.")

    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"


def get_positive_number(prompt):
    """Prompt until the user enters a finite, positive number."""
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not math.isfinite(value) or value <= 0:
            print("Please enter a number greater than zero.")
            continue

        return value


def main():
    print("BMI Calculator (adults)")
    weight_kg = get_positive_number("Weight in kilograms: ")
    height_cm = get_positive_number("Height in centimeters: ")

    bmi = calculate_bmi(weight_kg, height_cm)
    category = get_bmi_category(bmi)
    print(f"Your BMI is {bmi:.1f} ({category}).")
    print("BMI is a screening measure, not a medical diagnosis.")


if __name__ == "__main__":
    main()
