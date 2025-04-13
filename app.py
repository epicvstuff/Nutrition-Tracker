import pandas as pd
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session

# --- Configuration ---
FOOD_DATA_FILE = 'food.csv'
# --- End Configuration ---

app = Flask(__name__)
# Secret key is needed for session management (to store the meal)
# Use a strong, random key in a real application
app.secret_key = 'your secret key' # Replace with a real secret key

# --- Global Variables ---
# Load data once when the app starts
food_df = None
nutrient_cols = []

def load_food_data(filepath):
    """Loads food data from the CSV file into a pandas DataFrame."""
    global food_df, nutrient_cols  # Use global variables
    try:
        df = pd.read_csv(filepath)
        print(f"Successfully loaded data from {filepath}")

        # Create a lowercase version for lookup
        df['lookup_description'] = df['Description'].str.lower().str.strip()

        # Identify nutrient columns
        nutrient_cols = [col for col in df.columns if col not in ['Description', 'Category', 'lookup_description']]

        # Ensure nutrient columns are numeric
        for col in nutrient_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Fill potential NaN values in nutrient columns with 0 after conversion attempt
        # Alternatively, you might want to keep them NaN depending on how you sum
        # df[nutrient_cols] = df[nutrient_cols].fillna(0) # Optional: fill NaN with 0

        print(f"Found {len(df)} food items.")
        food_df = df # Assign to global variable
        return True # Indicate success
    except FileNotFoundError:
        print(f"ERROR: The file '{filepath}' was not found.", file=sys.stderr)
        flash(f"ERROR: Data file '{filepath}' not found. Cannot start application.", "error")
        return False
    except Exception as e:
        print(f"An error occurred while loading data: {e}", file=sys.stderr)
        flash(f"An error occurred while loading data: {e}", "error")
        return False

# --- Routes ---

@app.route('/', methods=['GET'])
def index():
    """Renders the main page."""
    # Initialize meal list in session if it doesn't exist
    session.setdefault('meal_items', [])
    session.setdefault('meal_totals', None)

    return render_template(
        'index.html',
        meal_items=session['meal_items'],
        totals=session.get('meal_totals') # Use .get() in case it's not set
    )

@app.route('/add_food', methods=['POST'])
def add_food():
    """Adds a food item to the meal list in the session."""
    if food_df is None:
         flash("Food database not loaded. Cannot add food.", "error")
         return redirect(url_for('index'))

    food_name_input = request.form.get('food_name', '').strip()
    if not food_name_input:
        flash("Please enter a food name.", "warning")
        return redirect(url_for('index'))

    # Initialize meal list if it doesn't exist
    session.setdefault('meal_items', [])

    # Search (case-insensitive, exact match first)
    search_term = food_name_input.lower()
    found_food = food_df[food_df['lookup_description'] == search_term]

    if not found_food.empty:
        food_description = found_food.iloc[0]['Description']
        # Avoid adding duplicates directly
        if food_description not in session['meal_items']:
             session['meal_items'].append(food_description)
             flash(f"Added: {food_description}", "success")
             session.modified = True # Mark session as modified
             # Clear previous totals when adding new item
             session['meal_totals'] = None
        else:
             flash(f"'{food_description}' is already in the meal.", "info")

    else:
        # Try partial match if exact fails
        partial_matches = food_df[food_df['lookup_description'].str.contains(search_term, case=False, na=False)]
        if not partial_matches.empty:
            suggestions = partial_matches['Description'].head(5).tolist()
            flash(f"Food '{food_name_input}' not found exactly. Did you mean one of these? {suggestions}", "warning")
        else:
            flash(f"Food item '{food_name_input}' not found in the database.", "error")

    return redirect(url_for('index'))

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculates the total nutrition for the meal."""
    if food_df is None or not nutrient_cols:
         flash("Food database not loaded. Cannot calculate.", "error")
         return redirect(url_for('index'))

    meal_items_desc = session.get('meal_items', [])
    if not meal_items_desc:
        flash("No food items in the meal to calculate.", "warning")
        session['meal_totals'] = None # Clear any previous totals
        return redirect(url_for('index'))

    # Get the rows from the main DataFrame corresponding to the meal items
    meal_df_rows = food_df[food_df['Description'].isin(meal_items_desc)]

    if not meal_df_rows.empty:
        # Calculate the sum for each nutrient column, skipping NaN values
        total_nutrition = meal_df_rows[nutrient_cols].sum(skipna=True)
        # Convert Series to dictionary for easier handling in template/session
        session['meal_totals'] = total_nutrition.to_dict()
        flash("Nutrition calculated successfully.", "success")
    else:
        flash("Could not find data for the items in the meal. Calculation failed.", "error")
        session['meal_totals'] = None

    session.modified = True
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_meal():
    """Clears the meal list and totals from the session."""
    session['meal_items'] = []
    session['meal_totals'] = None
    session.modified = True
    flash("Meal cleared.", "info")
    return redirect(url_for('index'))


# --- Main Execution ---
if __name__ == '__main__':
    # Load the data before starting the server
    if load_food_data(FOOD_DATA_FILE):
        # Run the Flask app
        # host='0.0.0.0' makes it accessible on your network
        # debug=True automatically reloads on code changes (DON'T use in production)
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        print("Failed to load food data. Exiting.", file=sys.stderr)
        sys.exit(1)