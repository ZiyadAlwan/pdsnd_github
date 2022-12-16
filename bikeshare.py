import time
import datetime
import pandas as pd
import os
import click

CITY_INFO = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
agreed = ['y', 'n']


def get_city():
    """
    Get City information and return it

    Returns:
        city(str)
    """
    city = input("Enter the city you want see data for 'Chicago' , 'New York City' or 'Washington' : ").lower()
    # force user to input correct city in loop
    while True:
        if city not in CITY_INFO:
            city = input("Incorrect City. Try Again...\n"
                         "Enter the city you want see data for 'Chicago' , 'New York City' or 'Washington' : ").lower()
        else:
            break
    return city


def get_month():
    """
    Get Month information and return it

    Returns:
        Month(str)
    """
    month = input("Enter 'all' to disable month filter or any month "
                  "between January and June including to apply filter : ").lower()
    # force user to input correct month in loop or 'all'
    while True:
        if month not in MONTHS and month != 'all':
            month = input("Invalid month. Try Again...\n"
                          "Enter 'all' to disable month filter or any month "
                          "between January and June including to apply filter : ").lower()
        else:
            break
    return month


def get_day():
    """
    Get Day information and return it

    Returns:
        Day(str)
    """
    day = input("Enter 'all' to disable filtering or any day from Monday to Sunday: ").lower()
    # force user to input correct day in loop or 'all'
    while True:
        if day not in DAYS and day != 'all':
            day = input("Invalid day name. Try Again...\n"
                        "Enter 'all' to disable filtering or any day from Monday to Sunday: ").lower()
        else:
            break
    return day


def load_data(city, month, day):
    """
    Loads data based on city and filter by month and day if it's needed

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    fileN = CITY_INFO[city]
    #check whether there is correct file
    if os.path.exists(fileN):
        #load csv
        df = pd.read_csv(fileN)
        #update columns values to be able use them in future for statistics
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['hour'] = df['Start Time'].dt.hour
        df['day_of_week'] = df['Start Time'].dt.strftime("%A").apply(lambda x: x.lower())
        # Month filter if needed
        if month != 'all':
            df = df[df['month'] == (MONTHS.index(month) + 1)]
        # Day filter if needed
        if day != 'all':
            df = df[df['day_of_week'] == day]

        return df


def get_statistics_time(df):
    """Shows The Most popular Times of Travel """

    print_title(f"The Most popular Times of Travel...")
    start_time = time.time()
    #gets and displays statistics for Most Frequent Month,Day Start Hour to Travel
    print(f"Month: { MONTHS[df['month'].mode()[0] - 1].capitalize()}")
    print(f"Day: { df['day_of_week'].mode()[0].capitalize()}")
    print(f"Start Hour: {df['hour'].mode()[0]}")
    calculate_execution(start_time)


def get_statistics_station(df):
    """Shows the most common stations and trip combinations."""
    print_title('The Most Popular Stations and Trip...')
    start_time = time.time()
    # gets and shows the most common stations and trip combinations
    print(f"The most common Start Station: { df['Start Station'].mode()[0]}")
    print(f"The most common End Station: { df['End Station'].mode()[0]}")
    #to display combination groupby was used, then arrange by reaping values and get the first the biggest
    print(f"The most common combination of Start and End Station Trips:"
          f" {df.groupby(['Start Station', 'End Station']).size().nlargest(1).to_string(header=False)[:-5]}")
    calculate_execution(start_time)


def get_statistics_duration_trip(df):
    """Shows the total and average travel durations."""
    print_title('Trip Duration...')
    start_time = time.time()
    # get and discply the total and average travel durations
    print(f"Total duration trip time: {datetime.timedelta(seconds=(int(df['Trip Duration'].sum())))}")
    print(f"Mean Trip Duration: {datetime.timedelta(seconds=(int(df['Trip Duration'].mean())))}")
    calculate_execution(start_time)


def get_user_statistics(df):
    """Shows the information about users from filtering data."""

    print_title('User Stats...')
    start_time = time.time()
    #gets stats for users
    print(f"{df['User Type'].value_counts().to_string()}")
    #gets stats by gender if it exists
    try:
        print(f"{df['Gender'].value_counts().to_string()}")
    except:
        pass
    #gets stats for Birth year if it exists
    try:
        print(f"Min Birth year: {int(df['Birth Year'].min())}")
        print(f"Max Birth year: {int(df['Birth Year'].max())}")
        print(f"Common Birth year: {int(df['Birth Year'].mode()[0])}")
    except:
        pass
    calculate_execution(start_time)


def show_raw_data(df):
    """Displays raw panda data"""
    # To prompt the user whether they would like want to see the raw data
    user_input = input('Load raw data? (Enter:Y/N).\n').lower()
    while True:
        if user_input.lower() not in agreed:
            user_input = input('Please Enter Y or N:\n').lower()
        else:
            break
    n = 0
    while True:
        if user_input == 'y':
            print(df.iloc[n: n + 5])
            n += 5
            user_input = input('\nLoad more data? (Enter:Y/N).\n').lower()
            while True:
                if user_input not in agreed:
                    user_input = input('Please Enter Y or N:\n').lower()
                else:
                    break
        else:
            break


def check_for_restart():
    """Checks wether the script should be colled one more time without interaption"""

    restart = input('\nShould we start from begining? (Enter:Y/N).\n').lower()
    while True:
        if restart not in agreed:
            restart = input('Please Enter Y or N:\n').lower()
        else:
            break
    if restart != 'y':
        print('BYE!')
        return False
    return True

def print_title(title):
    """Displays nice title"""
    click.secho(title, fg="red")

def calculate_execution(start_time):
    """Calculates execution and shows in nice view"""
    total = str(datetime.timedelta(seconds=(time.time() - start_time)))
    print(f"\nCalculated for {total} seconds.")
    click.secho(f"{'=' * 50}", fg="blue")

def main():
    click.secho("Hello. Let's begin", fg="blue")

    while True:
        city = get_city()
        month = get_month()
        day = get_day()
        print('=' * 40)
        df = load_data(city, month, day)

        get_statistics_time(df)
        get_statistics_station(df)

        get_statistics_duration_trip(df)
        get_user_statistics(df)
        show_raw_data(df)
        if not check_for_restart():
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye")
