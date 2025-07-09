##still need to account for stock prefix discrepancies, need more real data examples
##from power it could have leading zeros?
##from CDK it might have "NU" or something?

#validations that could be added: year, model #, list price, msrp, accounting cost, duplicate stocks or duplicate vins
#validations for trim, color, or model description could be added but may not be useful if the descrepancy comes from abbreviation variations

#if the program does anything weird or makes mistakes please reach out to me so I can troubleshoot and fix it! Aimee_Brewer@reyrey.com

import csv



# all of the file opening condensed into one function that takes a file path and input list reference
# need to change to just create list in function and return that created list
def populate_list(file_path):
    output_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            output_list.append(line)
    return output_list

#open all the files to look at and save them to the empty lists above ^


#defining function that checks if every stock from the old system has made it into the new one
def validate_stock_exists(old_inv,ignite_inv):
    ignite_stocks = []
    missing_stock = []
    stock_missing_count = 0
    for i in range(1, len(ignite_inv)):
        ignite_stocks.append(ignite_inv[i][0])
    for i in range(1, len(old_inv)):
        try:
            index = ignite_stocks.index(old_inv[i][0])
        except:
            stock_missing_count += 1
            missing_stock.append(old_inv[i][0])
    return stock_missing_count, missing_stock

#defining function that checks stock numbers to see if any of their VINs changed in conversion
def vin_stock_matches(missing_stock,old_inv,ignite_inv):
    old_cars = []
    ignite_cars = []
    vin_error_cars = []
    vin_errors_found = 0
    for i in range(1, len(old_inv)):
        car = (old_inv[i][0],old_inv[i][1])
        old_cars.append(car)
    for i in range(1, len(ignite_inv)):
        car = (ignite_inv[i][0],ignite_inv[i][1])
        ignite_cars.append(car)
    for car in old_cars:
        if car[0] in missing_stock:
            continue
        else:
            try:
                index = ignite_cars.index(car)           
            except:
                vin_errors_found += 1
                vin_error_cars.append(car)
    
    return vin_errors_found, vin_error_cars
            
#defining function to check if each stock number has the correct associated odometer reading post conversion
def odom_matches(missing_stock, old_inv,ignite_inv):
    old_cars = []
    ignite_cars = []
    odom_error_cars = []
    odom_errors_found = 0
    for i in range(1, len(old_inv)):
        odom1 = (old_inv[i][2]).replace(",","")
        car = (old_inv[i][0],odom1)
        old_cars.append(car)
    for i in range(1, len(ignite_inv)):
            odom2 = (ignite_inv[i][2]).replace(",","")
            car = (ignite_inv[i][0],odom2)
            ignite_cars.append(car)
    for car in old_cars:
        if car[0] in missing_stock:
            continue
        else:
            try:
                index = ignite_cars.index(car)
            except:
                odom_errors_found += 1
                odom_error_cars.append(car) 
    
    return odom_errors_found, odom_error_cars
            
