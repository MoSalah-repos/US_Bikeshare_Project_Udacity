import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some bikeshare data in three US major cities during a specific period!')
    
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs.
    # Note that the input data are case insensitive (user can provide any set of characters for city, month or day).
    while True:
        city = input("Please, choose one of the following US cities to filter your data? (Chicago - New York City - Washington)\n").lower()
        if city not in CITY_DATA.keys():
            # printing  a message to user informing him that his input data are invalid
          print("Sorry, invalid input. Please type a valid city name")
          continue
        else:
          break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input("\nPlease, choose a month from the following list to filter by: \n(January - February - March - April - May - June)\n or you can type 'all' if you do not want to filter your data.\n").lower()
        if month not in months:
          print("\nSorry, invalid input. Please type a valid month name or all.")
          continue
        else:
          break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
        day = input("\nPlease choose one or all of the following list to filter by: \n(Sunday - Monday - Tuesday - Wednesday - Thursday - Friday - Saturday or  'all')\n").lower()
        if day not in days:
          print("\nSorry, invalid input. Please type a valid day name or all.")
          continue
        else:
          break

    print('-'*60)
    return city, month, day


def load_data(city, month, day):
    """ 
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Use pandas library to load csv data files into dataframes (df)
    df = pd.read_csv(CITY_DATA[city])

    # Use pandas library to convert the argument of "Start Time" to datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Separate the month, day of week, and hour of day from Start Time column to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()    # Note that the old version of (dt.day_name()) function is (dt.weekday_name)
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1         # We have to consider the zero-based indexing by adding 1

        # A new datafrome after filtering by month
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # A new datafrome after filtering by day of week
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nDisplaying statistics on the most frequent times of travel\n')
    start_time = time.time()

    # TO DO: display the most common month
    Most_common_month= df['month'].mode()[0]
    print('Most Common Month:', Most_common_month)

    # TO DO: display the most common day of week
    Most_common_day_of_week= df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', Most_common_day_of_week)

    # TO DO: display the most common start hour
    Most_common_hour_of_day = df['start_hour'].mode()[0]
    print('Most Common Hour of Day:', Most_common_hour_of_day)

    print("\nSuch requirement took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nDisplays statistics on the most popular stations and trip:\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    Most_Common_Start_Station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", Most_Common_Start_Station)

    # TO DO: display most commonly used end station
    Most_Common_End_Station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", Most_Common_End_Station)

    # TO DO: display most frequent combination of start station and end station trip
    Most_Common_Trip_from_Start_to_End = df.groupby(['Start Station', 'End Station']).count()
    print('The most frequent combination of start station and end station:', Most_Common_Start_Station, " to ", Most_Common_End_Station)

    print("\nSuch requirement took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nDisplaying statistics on the total and average trip duration:\n')
    start_time = time.time()

    # TO DO: display total travel time
    Seconds_in_Minute = 60
    Minites_in_Hour = 60
    Hours_in_Day = 24
    
    Total_Travel_Time = df['Trip Duration'].sum()
    Minutes, Seconds = divmod(Total_Travel_Time, Seconds_in_Minute)
    Hours, Minutes = divmod(Minutes, Minites_in_Hour)
    Days, Hours = divmod(Hours, Hours_in_Day)
    print('Total travel time: %d Days, %d Hours, %d Minutes, and %d Seconds' %(Days, Hours, Minutes, Seconds))

    # TO DO: display mean travel time
    #Seconds_in_Minute = 60
    Mean_Travel_Time = df['Trip Duration'].mean()
    Minutes, Seconds = divmod(Mean_Travel_Time, Seconds_in_Minute)
    print('Mean travel time: %d Minutes and %d Seconds' % (Minutes, Seconds))

    print("\nSuch requirement took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nDisplaying statistics on bikeshare users:\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts().to_frame()
    print('Counts of each user type:\n', user_type)
    print("\nSuch requirement took %s seconds." % (time.time() - start_time))
    print('-'*60)
    
    # TO DO: Display counts of gender
    try:
       """Displaying statistics on the most frequent times of travel:"""
       print('\nDisplaying statistics on Bike riders gender')
       gender_count = df['Gender'].value_counts().to_frame()
       print('Counts of Bike riders gender:\n' ,gender_count)
    except KeyError:
       print("\nSorry, no data avaiballe on gender types for such city")
    
    print("\nSuch requirement took %s seconds." % (time.time() - start_time))
    print('-'*60)

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
       """Displays statistics on the earliest, most recent, and most common years:"""
       print('\nDisplaying statistics on the earliest, most recent, and most common years:')
       Earliest_Year = df['Birth Year'].min()
       Most_Recent_Year = df['Birth Year'].max()
       Most_Common_Year1 = df['Birth Year'].mode()[0]
       Most_Common_Year2 = df['Birth Year'].value_counts().idxmax()
       print('\nEarliest Year:', Earliest_Year)
       print('\nMost Recent Year:', Most_Recent_Year)
       print('\nMost Common Year Method1:', Most_Common_Year1)
       print('\nMost Common Year Method2:', Most_Common_Year2)
    except KeyError:
       print("\nSorry, no data available for such city.")

    print("\nSuch requirement took %s seconds." % (time.time() - start_time))
    print('-'*60)

            
def raw_data(df):

    current_raw = 0
    next_raw = 5

    decision_1 = input("Would you like to show a sample of raw data?\nPlease type 'Yes' if you wish or 'No' if you don't wish\n").lower()

    if decision_1 == 'yes':
        while next_raw <= df.shape[0] - 1:

            print(df.iloc[current_raw:next_raw,:])
            current_raw += 5
            next_raw += 5

            decision_2 = input("Would you like to show more raw data? Type 'Yes' or 'No'\n").lower()
            if decision_2 == 'no':
                break
            print('-'*60)
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank you for your time in exploring the presented data')
            break

            
if __name__ == "__main__":
	main()
