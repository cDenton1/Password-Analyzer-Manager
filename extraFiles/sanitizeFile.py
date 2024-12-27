def sanitize_file(input_file, output_file):
    with open(input_file, 'r', encoding="utf-8", errors='ignore') as infile, open(output_file, 'w', encoding="ascii", errors='ignore') as outfile:
        for line in infile:
            cleaned_line = ''.join([char if ord(char) < 128 else '' for char in line])  # Only keep ASCII characters
            outfile.write(cleaned_line)

# Example usage
sanitize_file('places.txt', 'places_sanitized.txt')
