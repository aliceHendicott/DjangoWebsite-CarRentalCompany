import csv

def export_csv():
    with open('names.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')

    writer.writeheader()
    for x in range(5):        
        writer.writerow({'first_name': str(x), 'last_name': str(x)})
