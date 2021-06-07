'''
This program should scrape the webpage "https://www.worldometers.info/coronavirus/"
and saves the table of the Corona statistics in a dataframe which is saved as csv file.
Then the program asks the user whether it should show the real-time Covid-19 statistics,
in particular "Total Cases" and "Active Cases", of the Top 10 countries or of the 6 continents.
The statistics are plotted as pie charts next to each other.
'''

# load libraries
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt


def main():
    webpage_content = load_page()
    soup = convert_to_bs(webpage_content)
    user_input = ask_user()
    corona_stats = scrap_table_into_csv(soup, user_input)
    plot_corona_stats(corona_stats, user_input)


def load_page():
    my_url = 'https://www.worldometers.info/coronavirus/'
    webpage_content = requests.get(my_url)
    return webpage_content


def convert_to_bs(webpage_content):
    soup = bs(webpage_content.content, 'html.parser')
    return soup


def ask_user():
    user_input = ''
    while user_input != 'Countries' and user_input != 'Continents':
        user_input = input("Please enter 'Countries' or 'Continents': ")
    return user_input


def scrap_table_into_csv(soup, user_input):
    table = soup.select('table#main_table_countries_today')[0]
    columns = table.find('thead').find_all('th')
    column_names = [x.text for x in columns]
    table_rows = table.find('tbody').find_all('tr')
    l = []
    i = 0
    for tr in table_rows:
        td = tr.find_all('td')
        if user_input == 'Continents':
            if i < 6:
                row = [tr.text.replace(',', '') for tr in td]
                l.append(row)
            i += 1
        elif user_input == 'Countries':
            if 7 < i < 18:
                row = [tr.text.replace(',', '') for tr in td]
                l.append(row)
            i += 1

    df = pd.DataFrame(l, columns=column_names)
    df[['TotalCases', 'ActiveCases']] = df[['TotalCases', 'ActiveCases']].astype(float)
    df['TotalCases'] = df['TotalCases'] / 1000000  # Show Total Cases in millions
    df['ActiveCases'] = df['ActiveCases'] / 1000000  # Show Active Cases in millions
    df.to_csv("final_project.csv")
    return df


def plot_corona_stats(corona_stats, user_input):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    if user_input == 'Continents':
        ax1.pie(corona_stats['TotalCases'], labels=corona_stats['Country,Other'], autopct='%1.1f%%')
        ax1.set_title("Share of Total Cases by Continent")
        ax2.pie(corona_stats['ActiveCases'], labels=corona_stats['Country,Other'], autopct='%1.1f%%')
        ax2.set_title("Share of Active Cases by Continent")
    elif user_input == 'Countries':
        ax1.bar(corona_stats['Country,Other'], corona_stats['TotalCases'],
                color=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan'])
        ax1.set_title("Top 10 Countries - Total Cases")
        ax1.set_ylabel('Total Cases in Millions')
        ax1.tick_params(labelrotation=35)
        ax1.yaxis.set_tick_params(pad=10)
        ax2.bar(corona_stats['Country,Other'], corona_stats['ActiveCases'],
                color=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan'])
        ax2.set_title("Top 10 Countries - Active Cases")
        ax2.set_ylabel('Active Cases in Millions')
        ax2.tick_params(labelrotation=35)
        ax2.yaxis.set_tick_params(pad=10)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()