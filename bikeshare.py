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
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nPlease enter the city you would like to explore (Chicago, New York City, Washington):\n')
        city = city.lower()
        if city in cities:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nPlease enter the month you would like to filter by (All, January, February, ... , June):\n')
        month = month.lower()
        if month in months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nPlease enter the day you would like to filter by (All, Monday, Tuesday, ... , Sunday):\n')
        day = day.lower()
        if day in days:
            break

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0]
    print('Most common month: {}'.format(month))

    # display the most common day of week
    dow = df['day_of_week'].mode()[0]
    print('Most common day of week: {}'.format(dow))

    # display the most common start hour
    hour = df['hour'].mode()[0]
    print('Most common hour: {}'.format(hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df['Start Station'].value_counts().index[0]
    print('Most commonly used start station: {}'.format(start))

    # display most commonly used end station
    end = df['End Station'].value_counts().index[0]
    print('Most commonly used end station: {}'.format(end))

    # display most frequent combination of start station and end station trip
    start_end = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().reset_index(name='Count')
    start_end = start_end.sort_values(by='Count', ascending=False).iloc[0]
    print('Most frequent combination of start and end stations: \n{}'.format(start_end[['Start Station', 'End Station']]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = int(df['Trip Duration'].sum())
    minutes = total_duration // 60
    hours = minutes // 60
    days = hours // 24
    print('Total travel time: {}:{}:{}:{}'.format(days, hours % 24, minutes % 60, total_duration % 60))

    # display mean travel time
    mean_duration = int(df['Trip Duration'].mean())
    minutes = mean_duration // 60
    print('Mean travel time: {}:{}'.format(minutes % 60, mean_duration % 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\n{}'.format(gender))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('\nEarliest birth year: {}'.format(earliest))
        print('Most recent birth year: {}'.format(most_recent))
        print('Most common birth year: {}'.format(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # TODO Raw data request

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
