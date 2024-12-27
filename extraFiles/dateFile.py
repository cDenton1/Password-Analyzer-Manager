year = 1950
date = 1
file = "dates.txt"
with open(file, 'w') as file: 
    while year < 2025:
        strYear = str(year)
        file.write(f"{strYear}\n")
        year += 1
    while date < 32:
        strDate = str(date)
        if date == 1 or date == 21 or date == 31:
            file.write(f"{strDate}st\n")
        elif date == 2 or date == 22:
            file.write(f"{strDate}nd\n")
        elif date == 3 or date == 23:
            file.write(f"{strDate}rd\n")
        else:
            file.write(f"{strDate}th\n")
        date += 1