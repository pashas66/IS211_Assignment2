from urllib.request import urlopen 
import logging
import argparse
import datetime


def downloadData(url): #create a function called downloadData
        #A function to download the contents located at the url and return to the caller.
        get_url = urlopen(url)  #urlopen(url)
        return get_url.read().decode()
    #url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'

def processData(contents, logger): #create a function called processData
        #A function that retrieves the content of the file as the first parameter. Then, processes the file line by line and returns a dictionary that maps a person's ID to a tuple of the form in a date format of dd/mm/yyyy.

    my_dictionary = {}
        
#creating a datatime object process the birthday, which has a format of dd/mm/yyyy
    for line, row in enumerate(contents.splitlines(), start=1):
        number, name, date = row.rstrip().split(",")
        try:
            date = datetime.datetime.strptime(date, "%d/%m/%Y").date() #row variable is a list that represents a row in csv
            my_dictionary[int(number)] = (name, date)
        except ValueError:

            logger.error("Error processing line#{} for ID #{}.".format(line, number)) #The log message should be sent to the ERROR level
    return my_dictionary

def displayPerson(id, personData): #create a function called displayPerson
    #A function given the id, it will display the personData index 0 as name, and personData index 1 as the birthday

    try:
        response = "Person ID #{id} is {name} with a birthday of {date}"
        print(response.format(id=id, name=personData[id][0], date=personData[id][1]))
    except KeyError: #If there is no entry with the given id, then print No user found with that id instead. 
        print("No user found with that id")
 
def createlogger(filename="errors.log"):
    logging.basicConfig(filename=filename, level=logging.ERROR)
    return logging.getLogger("Assignment2")

def main():
    
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="URL to csv file.")
    args = parser.parse_args()
    logger = createlogger()

    #asking the user for an ID to lookup.
   
    csvData = downloadData(args.url)
    personData = processData(csvData, logger)
    msg = "Please Enter ID number. To exit press 0 or a negative number."

    while True:
        try:
            user = int(input(msg))
        except ValueError:
            print("Please try a different ID number or press 0 or a negative number to exit.")
            continue
        if user > 0:
            print(f"You have entered: {user}")
            displayPerson(user, personData)
        else:
            print(f"You have entered: {user}")
            print("Program will now exit.")
            break
    
if __name__ == "__main__":
    main()
    
    #end of the program