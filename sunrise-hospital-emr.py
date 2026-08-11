import pandas as pd
import matplotlib.pyplot as plt
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


SAMPLE_PATIENTS = [
    {"name": "Leanne Graham", "email": "Sincere@april.biz"},
    {"name": "Ervin Howell", "email": "Shanna@melissa.tv"},
    {"name": "Clementine Bauch", "email": "Nathan@yesenia.net"},
    {"name": "Patricia Lebsack", "email": "Julianne.OConner@kory.org"},
    {"name": "Chelsey Dietrich", "email": "Lucio_Hettinger@annie.ca"},
    {"name": "Dennis Schulist", "email": "Karley_Dach@jasper.info"},
    {"name": "Kurtis Weissnat", "email": "Telly.Hoeger@billy.biz"},
    {"name": "Nicholas Runolfsdottir", "email": "Sherwood@rosamond.me"},
    {"name": "Glenna Reichert", "email": "Chaim_McDermott@dana.io"},
    {"name": "Clementina DuBuque", "email": "Rey.Padberg@karina.biz"},
]

SAMPLE_AGES = [30, 45, 25, 50, 40, 35, 60, 28, 55, 32]
SAMPLE_CONDITIONS = [
    "Flu", "Hypertension", "Diabetes", "Hypertension", "Flu",
    "Hypertension", "Diabetes", "Flu", "Hypertension", "Hypertension"
]


# --------------------------------------------------
# Fetch and clean patient data from API
# --------------------------------------------------
def fetch_and_clean_data(url):
    """
    Fetch patient data from an API and clean it for analysis.
    If the API cannot be reached, use bundled demonstration data.
    """
    try:
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        if not isinstance(data, list) or not data:
            raise ValueError("The API returned no patient records.")

        print("Patient data downloaded from the API.")

    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as err:
        print(f"API unavailable ({err}). Using demonstration patient data.")
        data = SAMPLE_PATIENTS

    try:
        df = pd.DataFrame(data)

        if not {"name", "email"}.issubset(df.columns):
            raise ValueError("Patient records require name and email fields.")

        # Clean fields
        df["name"] = df["name"].astype(str).str.strip().str.title()
        df["email"] = df["email"].astype(str).str.strip().str.lower()

        # Demonstration fields because the source API does not provide them.
        df["age"] = [SAMPLE_AGES[i % len(SAMPLE_AGES)] for i in range(len(df))]
        df["condition"] = [
            SAMPLE_CONDITIONS[i % len(SAMPLE_CONDITIONS)]
            for i in range(len(df))
        ]

        return df

    except (KeyError, TypeError, ValueError) as err:
        print(f"Error preparing patient data: {err}")
        return pd.DataFrame()


# --------------------------------------------------
# Filter patients by age range
# --------------------------------------------------
def filter_by_age(patient_data, min_age, max_age):
    """
    Filter patients by a given age range.
    """
    try:
        return patient_data[
            (patient_data["age"] >= min_age) &
            (patient_data["age"] <= max_age)
        ]
    except KeyError:
        print("Error: Age column not found.")
        return pd.DataFrame()


# --------------------------------------------------
# Analyze patient data
# --------------------------------------------------
def analyze_data(df):
    """
    Analyze patient data and return summary statistics.
    """
    if df.empty:
        return {
            "total_patients": 0,
            "unique_domains": 0,
            "condition_counts": {},
            "mean_age": 0
        }

    condition_counts = df["condition"].value_counts().to_dict()

    return {
        "total_patients": len(df),
        "unique_domains": df["email"].str.split("@").str[1].nunique(),
        "condition_counts": condition_counts,
        "mean_age": df["age"].mean()
    }


# --------------------------------------------------
# Visualize analysis results
# --------------------------------------------------
def visualize_data(analysis, df, filtered=False):
    """
    Generate bar chart, pie chart, and age histogram.
    """
    if not analysis["condition_counts"]:
        print("No data available for visualization.")
        return

    # Bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(
        analysis["condition_counts"].keys(),
        analysis["condition_counts"].values(),
        color="skyblue"
    )
    plt.title("Condition Prevalence")
    plt.xlabel("Condition")
    plt.ylabel("Number of Patients")
    plt.savefig("conditions_plot.png")
    plt.close()

    # Pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(
        analysis["condition_counts"].values(),
        labels=analysis["condition_counts"].keys(),
        autopct="%1.1f%%"
    )
    plt.title("Condition Distribution")
    plt.savefig("conditions_pie.png")
    plt.close()

    # Age histogram
    plt.figure(figsize=(8, 6))
    df["age"].plot(kind="hist", bins=5, color="lightcoral")
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Number of Patients")
    plt.savefig(
        "filtered_age_distribution.png"
        if filtered else "age_distribution.png"
    )
    plt.close()


# --------------------------------------------------
# Save analysis summary to file
# --------------------------------------------------
def save_analysis(analysis, filename):
    """
    Save analysis results to a text file.
    """
    with open(filename, "w") as file:
        file.write("Analysis Summary\n")
        file.write(f"Total Patients: {analysis['total_patients']}\n")
        file.write(f"Unique Email Domains: {analysis['unique_domains']}\n")
        file.write(f"Mean Age: {analysis['mean_age']:.2f}\n")
        file.write("Condition Frequencies:\n")

        for condition, count in analysis["condition_counts"].items():
            file.write(f"- {condition}: {count}\n")


# --------------------------------------------------
# Get age range with input validation
# --------------------------------------------------
def get_age_range():
    """
    Prompt user for valid age range.
    """
    while True:
        try:
            min_age = int(input("Enter minimum age: "))
            max_age = int(input("Enter maximum age: "))

            if min_age < 0 or max_age < min_age:
                print("Invalid age range. Try again.")
                continue

            return min_age, max_age

        except ValueError:
            print("Please enter valid numeric values.")


# --------------------------------------------------
# Main program (DATA PRELOADED ON STARTUP)
# --------------------------------------------------
def main():
    url = "https://jsonplaceholder.typicode.com/users"

    print("\nWelcome to the Sunrise Hospital EMR System")
    print("Loading patient data...")

    # PRELOAD DATA
    patient_data = fetch_and_clean_data(url)
    filtered_data = pd.DataFrame()

    if patient_data.empty:
        print("Warning: Patient data could not be loaded.")
    else:
        print("Patient data preloaded successfully.")

    while True:
        print("\nOptions:")
        print("1. Fetch new patient data")
        print("2. Filter patients by age range")
        print("3. View analysis and visualizations")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            patient_data = fetch_and_clean_data(url)
            filtered_data = pd.DataFrame()
            print("Patient data refreshed.")

        elif choice == "2":
            if patient_data.empty:
                print("No data available.")
                continue

            min_age, max_age = get_age_range()
            filtered_data = filter_by_age(patient_data, min_age, max_age)

            if filtered_data.empty:
                print("No patients found in this age range.")
            else:
                print(filtered_data[["name", "email", "age"]])

        elif choice == "3":
            if patient_data.empty:
                print("No data available.")
                continue

            analysis_df = filtered_data if not filtered_data.empty else patient_data
            analysis = analyze_data(analysis_df)

            visualize_data(
                analysis,
                analysis_df,
                filtered=not filtered_data.empty
            )

            save_analysis(
                analysis,
                "filtered_analysis_summary.txt"
                if not filtered_data.empty else "analysis_summary.txt"
            )

            print("\nAnalysis Results:")
            print(f"Total Patients: {analysis['total_patients']}")
            print(f"Unique Email Domains: {analysis['unique_domains']}")
            print(f"Mean Age: {analysis['mean_age']:.2f}")

        elif choice == "4":
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid selection. Please try again.")


# --------------------------------------------------
# Run program
# --------------------------------------------------
if __name__ == "__main__":
    main()
