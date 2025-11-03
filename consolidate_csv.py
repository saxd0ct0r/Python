import csv
import sys

def consolidate_csvs(output_path, input_paths):
    if not input_paths:
        print("No input files provided.")
        return

    with open(output_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)

        for i, input_path in enumerate(input_paths):
            with open(input_path, 'r', newline='') as input_file:
                reader = csv.reader(input_file)
                if i == 0:
                    # Write header and all rows from first file
                    for row in reader:
                        writer.writerow(row)
                else:
                    # Skip header for subsequent files
                    next(reader, None)  # Skip the header row
                    for row in reader:
                        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python consolidate_csv.py output.csv input1.csv input2.csv ...")
        sys.exit(1)

    output_path = sys.argv[1]
    input_paths = sys.argv[2:]
    consolidate_csvs(output_path, input_paths)
    print(f"Consolidated CSV saved to {output_path}")