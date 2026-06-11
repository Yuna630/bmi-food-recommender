"""
BMI & Meal Recommender (with allergy handling)
- Inputs: gender, weight (kg), height (m or cm), allergy yes/no
- Outputs: BMI, body type, comparison to gender-average BMI,
           and allergen-aware meal recommendations for gain/loss/maintain.
"""

# 1) BMI calculation ----------------------------------------------------------
def calculate_bmi(weight, height):
    """
    Accepts weight (kg) and height (meters), returns BMI = weight / (height**2)
    """
    return weight / (height ** 2)


# 2) Allergy collector --------------------------------------------------------
def get_allergy():
    """
    Shows common allergens and asks the user to pick one.
    Loops until a valid selection is made.
    Returns one of {'peanuts','milk','eggs'}.
    """
    options = {
        "1": "peanuts",
        "2": "milk",
        "3": "eggs",
    }
    print("\nSelect your allergic food:")
    print("  (1) peanuts\n  (2) milk\n  (3) eggs")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


# Helpers ---------------------------------------------------------------------
def classify_body_type(bmi):
    """
    Returns WHO-style BMI category (“body type”).
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"


def round1(x):
    return round(x, 1)


def recommend_meals(goal, allergen=None):
    """
    goal: 'gain', 'lose', or 'maintain'
    allergen: None or one of {'peanuts','milk','eggs'}
    Returns a list of meal strings filtered to exclude the allergen.
    """

    # Each meal has a label and a set of allergens it contains.
    # Keep these simple, nutritious, and allergen-aware.
    base_meals = {
        "gain": [
            {"name": "Chicken, avocado & rice bowl", "allergens": set()},
            {"name": "Lentil & coconut milk curry with brown rice", "allergens": set()},  # coconut ≠ milk
            {"name": "Whole-grain pasta with tomato sauce & turkey meatballs", "allergens": set()},
            {"name": "Tofu–veggie stir-fry with sesame & olive oil", "allergens": set()},
            {"name": "Oatmeal cooked in oat drink with banana & chia", "allergens": set()},
            {"name": "Hummus, olive oil & roasted veg wrap", "allergens": set()},
            {"name": "Salmon, sweet potato & green beans", "allergens": set()},
            # Avoid explicit peanuts / dairy / eggs in gain list
            {"name": "Greek-style bean salad (olive oil, lemon, herbs)", "allergens": set()},
            {"name": "Ground turkey chili with beans & brown rice", "allergens": set()},
            {"name": "Quinoa bowl with black beans, corn & avocado", "allergens": set()},
            # Examples that WOULD contain allergens if we enabled them:
            # {"name": "PB banana smoothie", "allergens": {"peanuts"}},
            # {"name": "Yogurt parfait", "allergens": {"milk"}},
            # {"name": "Egg fried rice", "allergens": {"eggs"}},
        ],
        "lose": [
            {"name": "Grilled salmon with quinoa & roasted veggies", "allergens": set()},
            {"name": "Chickpea salad (cucumber, tomato, herbs, lemon)", "allergens": set()},
            {"name": "Turkey lettuce wraps with salsa", "allergens": set()},
            {"name": "Baked chicken breast, broccoli & cauliflower mash", "allergens": set()},
            {"name": "Tofu & vegetable sheet-pan dinner", "allergens": set()},
            {"name": "Zucchini ‘noodle’ bowl with tomato & lean turkey", "allergens": set()},
            {"name": "Black bean soup with side salad", "allergens": set()},
            {"name": "Roasted cod, asparagus & farro", "allergens": set()},
            {"name": "Stir-fried vegetables with edamame over cauliflower rice", "allergens": set()},
            {"name": "Mediterranean bowl (brown rice, beans, olives, veg)", "allergens": set()},
            # Potential allergen examples removed:
            # {"name": "Veggie omelet", "allergens": {"eggs"}},
            # {"name": "Cottage cheese & berries", "allergens": {"milk"}},
            # {"name": "Peanut slaw chicken", "allergens": {"peanuts"}},
        ],
        "maintain": [
            {"name": "Grilled chicken, quinoa & mixed greens", "allergens": set()},
            {"name": "Brown rice sushi bowl with tofu & veggies", "allergens": set()},
            {"name": "Whole-grain pita stuffed with falafel & veg", "allergens": set()},
            {"name": "Baked salmon, wild rice & salad", "allergens": set()},
            {"name": "Lentil & vegetable stew with crusty whole-grain bread", "allergens": set()},
            {"name": "Stuffed bell peppers (lean beef or turkey, rice, tomato)", "allergens": set()},
            {"name": "Pasta e fagioli (beans & tomatoes) with side salad", "allergens": set()},
            {"name": "Warm barley bowl with chickpeas & roasted veg", "allergens": set()},
        ],
    }

    meals = base_meals[goal]
    if allergen is None:
        return [m["name"] for m in meals]

    filtered = [m["name"] for m in meals if allergen not in m["allergens"]]
    # In this design most meals already avoid the three allergens.
    # If everything filtered out (unlikely), fall back to a few safe generics:
    if not filtered:
        safe_defaults = [
            "Rice bowl with grilled chicken and vegetables",
            "Quinoa, black beans, salsa & avocado",
            "Lentil stew with tomatoes and herbs",
        ]
        return safe_defaults
    return filtered


def ask_float(prompt):
    while True:
        try:
            val = float(input(prompt).strip())
            return val
        except ValueError:
            print("Please enter a number (e.g., 72.5).")


def main():
    print("=== BMI Calculator & Food Recommender ===")

    # 3) User input and BMI calculation --------------------------------------
    # gender
    while True:
        gender = input("Enter your gender (male/female): ").strip().lower()
        if gender in {"male", "female"}:
            break
        print("Please enter 'male' or 'female'.")

    # weight (kg)
    weight = ask_float("Enter your weight in kilograms (e.g., 68.0): ")
    while weight <= 0:
        print("Weight must be positive.")
        weight = ask_float("Enter your weight in kilograms (e.g., 68.0): ")

    # height; accept meters or centimeters
    height = ask_float("Enter your height (meters; if you enter >3, I'll treat it as centimeters): ")
    if height > 3:  # probably centimeters
        height = height / 100.0
        print(f"Interpreted as centimeters. Converted height: {round(height, 3)} m")

    while height <= 0:
        print("Height must be positive.")
        height = ask_float("Enter your height in meters: ")

    bmi = calculate_bmi(weight, height)

    # allergy yes/no
    allergy_answer = input("Do you have a food allergy among peanuts, milk, or eggs? (yes/no): ").strip().lower()
    has_allergy = allergy_answer.startswith("y")
    selected_allergen = None
    if has_allergy:
        # 5) Food allergy -> get_allergy loop
        selected_allergen = get_allergy()

    # 4) BMI comparison vs gender average ------------------------------------
    gender_avg = {"male": 26.6, "female": 26.5}[gender]
    body_type = classify_body_type(bmi)
    diff = bmi - gender_avg

    print("\n--- Results ---")
    print(f"Your BMI: {round1(bmi)}")
    print(f"Body type: {body_type}")
    if diff > 0:
        print(f"Compared to the average BMI for {gender} ({gender_avg}), you are {round1(diff)} higher.")
    elif diff < 0:
        print(f"Compared to the average BMI for {gender} ({gender_avg}), you are {round1(abs(diff))} lower.")
    else:
        print(f"Your BMI is exactly the average for {gender} ({gender_avg}).")

    # Goal for recommendations based on BMI vs gender average
    if diff > 0:
        goal = "lose"
    elif diff < 0:
        goal = "gain"
    else:
        goal = "maintain"

    # 5) Food allergy–aware recommendations ----------------------------------
    print("\n--- Meal Recommendations ---")
    if selected_allergen:
        print(f"Allergen to avoid: {selected_allergen}")
    meals = recommend_meals(goal, allergen=selected_allergen)

    if goal == "gain":
        print("Focus: Calorie-dense, protein-forward meals to support healthy weight gain.")
    elif goal == "lose":
        print("Focus: Higher protein, fiber-rich, moderate-carb meals to support weight loss.")
    else:
        print("Focus: Balanced meals to maintain your current weight.")

    for i, meal in enumerate(meals[:6], start=1):  # show top 6
        print(f"{i}. {meal}")

    print("\nTips:")
    if goal == "gain":
        print("- Add an extra snack (nuts/seed mixes if allowed, hummus with whole-grain crackers, olive-oil drizzle).")
        print("- Include a protein source each meal (poultry, fish, tofu, legumes).")
        print("- Use healthy fats (olive oil, avocado) to increase calories.")
    elif goal == "lose":
        print("- Fill half your plate with vegetables; prioritize lean proteins.")
        print("- Choose whole grains and watch liquid calories.")
        print("- Stay hydrated; aim for steady activity most days.")
    else:
        print("- Keep a balanced plate: protein + complex carbs + veggies + healthy fats.")
        print("- Stay consistent with meals and movement.")

    print("\n(Always tailor to your medical needs; consult a healthcare professional for personalized advice.)")


if __name__ == "__main__":
    main()
