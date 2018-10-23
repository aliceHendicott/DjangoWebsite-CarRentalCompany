import csv

def export_csv(response, fields):
    writer = csv.DictWriter(response, fieldnames=fields, lineterminator = '\n')
    writer.writeheader()
    for x in range(5):
        writer.writerow({fields[0]: str(x), 
                         fields[1]: str(x)})