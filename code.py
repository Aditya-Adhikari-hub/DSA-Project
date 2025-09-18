import csv

# Global variables
cars_data = []
cars_by_brand = {}

def load_data():
    """Load and parse CSV data"""
    global cars_data, cars_by_brand
    cars_data = []
    csv_file_path = "USA_cars_datasets_DSA_1 (1).csv"  
    
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row['price'] = int(float(row['price']))
                    row['mileage'] = int(float(row['mileage']))
                    cars_data.append(row)
                except ValueError as e:
                    print(f"Skipping row due to invalid data: {row}")
                    continue
    except FileNotFoundError:
        print(f"Error: Could not find the file '{csv_file_path}'. Please make sure the file exists in the correct location.")
        exit(1)
    
    # Organize cars by brand
    for car in cars_data:
        brand = car['brand']
        if brand not in cars_by_brand:
            cars_by_brand[brand] = []
        cars_by_brand[brand].append(car)

def get_user_brand():
    """Get user's brand selection"""
    brands = list(cars_by_brand.keys())
    print("\nAvailable brands:")
    for idx, brand in enumerate(brands):
        print(f"{idx + 1}. {brand.title()}")
    
    while True:
        try:
            choice = int(input("\nSelect a brand by number: "))
            if 1 <= choice <= len(brands):
                return brands[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_ranking_method():
    """Get user's ranking preference"""
    print("\nHow would you like to rank the cars?")
    print("1. By Price (Low to High)")
    print("2. By Year (Newest First)")
    print("3. By Mileage (Low to High)")
    
    while True:
        try:
            choice = int(input("Select a ranking method by number: "))
            if choice == 1:
                return 'price'
            elif choice == 2:
                return 'year'
            elif choice == 3:
                return 'mileage'
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_price(car):
    """Key function for price sorting"""
    return car['price']

def get_year(car):
    """Key function for year sorting (newest first)"""
    return -car['year']

def get_mileage(car):
    """Key function for mileage sorting"""
    return car['mileage']

def quicksort(arr, key_func):
    """Quick sort implementation"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if key_func(x) < key_func(pivot)]
    middle = [x for x in arr if key_func(x) == key_func(pivot)]
    right = [x for x in arr if key_func(x) > key_func(pivot)]
    
    return quicksort(left, key_func) + middle + quicksort(right, key_func)

def main():
    """Main function"""
    # Load data
    load_data()
    
    # Get user preferences
    selected_brand = get_user_brand()
    cars_available = [car for car in cars_by_brand.get(selected_brand, []) 
                     if car['title_status'] == 'clean vehicle']
    
    if not cars_available:
        print(f"No clean vehicles available for the brand '{selected_brand}'.")
        return
    
    rank_by = get_ranking_method()
    
    # Select appropriate key function
    if rank_by == 'price':
        key_func = get_price
    elif rank_by == 'year':
        key_func = get_year
    elif rank_by == 'mileage':
        key_func = get_mileage
    
    # Sort cars
    sorted_cars = quicksort(cars_available, key_func)
    
    # Display results
    print(f"\nCars from '{selected_brand.title()}' ranked by {rank_by.capitalize()}:")
    print("-" * 50)
    
    for idx, car in enumerate(sorted_cars[:10], start=1):
        print(f"{idx}. Model: {car['model'].title()}")
        print(f"   Price: ${car['price']:,}")
        print(f"   Year: {car['year']}")
        print(f"   Mileage: {car['mileage']:,} miles")
        print(f"   Color: {car['color'].title()}")
        print()

if __name__ == "__main__":
    main()
