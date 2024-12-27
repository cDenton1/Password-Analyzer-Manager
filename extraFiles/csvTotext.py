import csv

file_path = "C:\\Users\\chloe\\OneDrive\\Desktop\\program\\python\\cities.csv"
output = "C:\\Users\\chloe\\OneDrive\\Desktop\\program\\python\\places.txt"

# Open the CSV file for reading with UTF-8 encoding and handle errors
with open(file_path, "r", encoding="utf-8", errors="replace") as file:
    csv_reader = csv.reader(file)  # Read the CSV file using csv.reader
    
    # Open the output file for writing with UTF-8 encoding and error handling
    with open(output, "a", encoding="utf-8", errors="replace") as output_file:
        for row in csv_reader:
            try:
                # Assuming the country name is in the second column (index 1)
                country = row[1].strip()  # Adjust index if necessary
                
                # Write the country to the output file
                output_file.write(country + "\n")
            except IndexError:
                # Handle cases where a row might not have enough columns
                print(f"Skipping a row due to missing columns: {row}")
                
print(f"Data has been written to {output}")
