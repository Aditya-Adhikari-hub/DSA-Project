import csv
from typing import List, Dict, Callable, Optional

"""Class for managing car data and ranking"""
class CarRankingSystem:
    def __init__(self, csv_file_path: str = "USA_cars_datasets_DSA_1 (1).csv"):
        self.csv_file_path = csv_file_path
        self.cars_data: List[Dict] = []
        self.cars_by_brand: Dict[str, List[Dict]] = {}
        self.ranking_methods = {
            '1': ('price', 'Price (Low to High)', self._get_price, False),
            '2': ('year', 'Year (Newest First)', self._get_year, True),
            '3': ('mileage', 'Mileage (Low to High)', self._get_mileage, False),
            '4': ('value', 'Best Value (Price/Year ratio)', self._get_value_score, False)
        }
        
    """Load and parse CSV data with better error handling"""
    def load_data(self) -> bool:
        try:
            with open(self.csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                skipped_rows = 0
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Clean and validate data
                        cleaned_row = self._clean_row_data(row)
                        if cleaned_row:
                            self.cars_data.append(cleaned_row)
                        else:
                            skipped_rows += 1
                    except ValueError:
                        skipped_rows += 1
                        continue
                
                if skipped_rows > 0:
                    print(f"Note: Skipped {skipped_rows} rows due to invalid data")
                
                if not self.cars_data:
                    print("Error: No valid data found in the CSV file.")
                    return False
                
                self._organize_by_brand()
                print(f"Successfully loaded {len(self.cars_data)} cars from {len(self.cars_by_brand)} brands")
                return True
                
        except FileNotFoundError:
            print(f"Error: Could not find the file '{self.csv_file_path}'.")
            print("Please make sure the file exists in the correct location.")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    """Clean and validate row data"""
    def _clean_row_data(self, row: Dict) -> Optional[Dict]:
        try:
            # Convert numeric fields
            price = float(row.get('price', 0))
            mileage = float(row.get('mileage', 0))
            year = int(row.get('year', 0))
            
            # Skip invalid records
            if price < 0 or mileage < 0 or year < 1900 or year > 2025:
                return None
            
            # Clean text fields
            brand = str(row.get('brand', '')).strip().lower()
            model = str(row.get('model', '')).strip()
            color = str(row.get('color', 'unknown')).strip()
            title_status = str(row.get('title_status', '')).strip().lower()
            
            if not brand or not model:
                return None
            
            return {
                'price': int(price),
                'brand': brand,
                'model': model,
                'year': year,
                'title_status': title_status,
                'mileage': int(mileage),
                'color': color
            }
        except (ValueError, TypeError):
            return None
    
    """Organize cars by brand"""
    def _organize_by_brand(self) -> None:
        self.cars_by_brand = {}
        for car in self.cars_data:
            brand = car['brand']
            if brand not in self.cars_by_brand:
                self.cars_by_brand[brand] = []
            self.cars_by_brand[brand].append(car)
    
    """Get user's brand selection with improved interface"""
    def get_user_brand(self) -> Optional[str]:
        if not self.cars_by_brand:
            print("No car data available.")
            return None
        brands = sorted(self.cars_by_brand.keys())
        print(f"\nAvailable brands ({len(brands)} total):")
        print("-" * 40)
        for i, brand in enumerate(brands, 1):
            count = len(self.cars_by_brand[brand])
            print(f"{i:2d}. {brand.title():<15} ({count} cars)")
        print(f"{len(brands) + 1:2d}. Show all brands statistics")
        
        while True:
            try:
                choice = input(f"\nSelect a brand (1-{len(brands)}) or 'q' to quit: ").strip()
                if choice.lower() == 'q':
                    return None
                choice_num = int(choice)
                if choice_num == len(brands) + 1:
                    self._show_brand_statistics()
                    continue
                elif 1 <= choice_num <= len(brands):
                    return brands[choice_num - 1]
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(brands)}.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")
    
    def _show_brand_statistics(self) -> None:
        """Show statistics for all brands"""
        print("\nBrand Statistics:")
        print("-" * 60)
        print(f"{'Brand':<15} {'Cars':<6} {'Avg Price':<12} {'Price Range'}")
        print("-" * 60)
        for brand in sorted(self.cars_by_brand.keys()):
            cars = self.cars_by_brand[brand]
            clean_cars = [car for car in cars if car['title_status'] == 'clean vehicle']
            if clean_cars:
                prices = [car['price'] for car in clean_cars]
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
                print(f"{brand.title():<15} {len(clean_cars):<6} ${avg_price:>8,.0f}   ${min_price:,} - ${max_price:,}")
        print()
    
    def get_ranking_method(self) -> Optional[tuple]:
        """Get user's ranking preference with more options"""
        print("\nHow would you like to rank the cars?")
        print("-" * 40)
        for key, (_, description, _, _) in self.ranking_methods.items():
            print(f"{key}. {description}")
        
        while True:
            try:
                choice = input(f"\nSelect a ranking method (1-{len(self.ranking_methods)}) or 'q' to quit: ").strip()
                if choice.lower() == 'q':
                    return None
                if choice in self.ranking_methods:
                    return self.ranking_methods[choice]
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(self.ranking_methods)}.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")
    
    # Key functions for sorting
    def _get_price(self, car: Dict) -> float:
        return car['price']
    
    def _get_year(self, car: Dict) -> int:
        return car['year']
    
    def _get_mileage(self, car: Dict) -> int:
        return car['mileage']
    
    def _get_value_score(self, car: Dict) -> float:
        """Calculate value score (lower is better)"""
        current_year = 2025
        car_age = max(1, current_year - car['year'])
        return car['price'] / (car_age ** 0.5)  # Square root to moderate age impact
    
    def quicksort(self, arr: List[Dict], key_func: Callable, reverse: bool = False) -> List[Dict]:
        """Improved quicksort with reverse option"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        pivot_value = key_func(pivot)
        if reverse:
            left = [x for x in arr if key_func(x) > pivot_value]
            middle = [x for x in arr if key_func(x) == pivot_value]
            right = [x for x in arr if key_func(x) < pivot_value]
        else:
            left = [x for x in arr if key_func(x) < pivot_value]
            middle = [x for x in arr if key_func(x) == pivot_value]
            right = [x for x in arr if key_func(x) > pivot_value]
            
        return self.quicksort(left, key_func, reverse) + middle + self.quicksort(right, key_func, reverse)
    
    def filter_cars(self, brand: str) -> List[Dict]:
        """Filter cars by brand and status with additional options"""
        cars_available = [car for car in self.cars_by_brand.get(brand, []) 
                         if car['title_status'] == 'clean vehicle']
        if not cars_available:
            return []
        
        # Ask for additional filters
        print(f"\nFound {len(cars_available)} clean vehicles for {brand.title()}")
        
        # Price filter
        prices = [car['price'] for car in cars_available]
        min_price, max_price = min(prices), max(prices)
        
        print(f"Price range: ${min_price:,} - ${max_price:,}")
        price_filter = input("Enter maximum price (or press Enter to skip): ").strip()
        
        if price_filter:
            try:
                max_price_filter = float(price_filter)
                cars_available = [car for car in cars_available if car['price'] <= max_price_filter]
                print(f"Filtered to {len(cars_available)} cars under ${max_price_filter:,.0f}")
            except ValueError:
                print("Invalid price entered, skipping price filter")
        
        # Year filter
        if cars_available:
            years = [car['year'] for car in cars_available]
            min_year, max_year = min(years), max(years)
            
            print(f"Year range: {min_year} - {max_year}")
            year_filter = input("Enter minimum year (or press Enter to skip): ").strip()
            
            if year_filter:
                try:
                    min_year_filter = int(year_filter)
                    cars_available = [car for car in cars_available if car['year'] >= min_year_filter]
                    print(f"Filtered to {len(cars_available)} cars from {min_year_filter} or newer")
                except ValueError:
                    print("Invalid year entered, skipping year filter")
        
        return cars_available
    
    def display_results(self, cars: List[Dict], brand: str, sort_method: str, limit: int = 10) -> None:
        """Display results with improved formatting"""
        if not cars:
            print(f"No cars found matching your criteria for {brand.title()}.")
            return
        
        total_cars = len(cars)
        display_count = min(limit, total_cars)
        
        print(f"\nTop {display_count} cars from '{brand.title()}' ranked by {sort_method}:")
        print("=" * 80)
        
        for idx, car in enumerate(cars[:display_count], start=1):
            print(f"{idx:2d}. {car['model'].title()} ({car['year']})")
            print(f" Price: ${car['price']:,}")
            print(f" Year: {car['year']}")
            print(f" Mileage: {car['mileage']:,} miles")
            print(f" Color: {car['color'].title()}")
            
            # Calculate additional metrics
            current_year = 2025
            age = current_year - car['year']
            if age > 0:
                price_per_year = car['price'] / age
                print(f"Value Score: ${price_per_year:,.0f}/year")
            
            print()
        
        if total_cars > display_count:
            print(f"... and {total_cars - display_count} more cars available")
        
        # Summary statistics
        if len(cars) > 1:
            prices = [car['price'] for car in cars]
            avg_price = sum(prices) / len(prices)
            print(f"\nSummary: {len(cars)} cars, Average price: ${avg_price:,.0f}")
    
    def run(self) -> None:
        """Main application loop"""
        print("Car Ranking System")
        print("=" * 50)
        
        if not self.load_data():
            return
        
        while True:
            print("\n" + "=" * 50)
            
            # Get user preferences
            selected_brand = self.get_user_brand()
            if not selected_brand:
                break
            
            cars_available = self.filter_cars(selected_brand)
            if not cars_available:
                print(f"No cars available for the brand '{selected_brand}' with your criteria.")
                continue
            
            ranking_info = self.get_ranking_method()
            if not ranking_info:
                break
            
            sort_key, description, key_func, reverse = ranking_info
            
            # Sort cars
            sorted_cars = self.quicksort(cars_available, key_func, reverse)
            
            # Display results
            self.display_results(sorted_cars, selected_brand, description)
            
            # Ask if user wants to continue
            continue_choice = input("\nWould you like to search again? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                break
        
        print("\nThank you for using the Car Ranking System!")

def main():
    """Entry point"""
    system = CarRankingSystem()
    system.run()

if __name__ == "__main__":
    main()
    
    
    