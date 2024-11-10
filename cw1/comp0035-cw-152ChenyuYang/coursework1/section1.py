import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def load_and_clean_data(housing_supply_path, waiting_list_path):
    """
    Load and clean the Housing Supply and Waiting List data.

    Parameters:
        housing_supply_path (Path): File path for Housing Supply data
        waiting_list_path (Path): File path for Waiting List data

    Returns:
        tuple: Housing Supply DataFrame and Waiting List DataFrame
    """
    housing_supply_data = pd.read_excel(
        housing_supply_path, sheet_name='Data'
    ).dropna(how='all')

    waiting_list_data = pd.read_excel(
        waiting_list_path,
        sheet_name='Households on LA Waiting List',
        header=1
    ).dropna(how='all')

    waiting_list_data.columns = ['Code', 'Current Code', 'Area'] + \
        list(waiting_list_data.columns[3:])
    waiting_list_data = waiting_list_data.dropna()

    return housing_supply_data, waiting_list_data


def display_data_info(df, name):
    """
    Display basic information of the DataFrame.
    """
    print(f"--- {name} ---")
    print("Size:", df.shape)
    print("\nAttributes and Data Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nStatistics:")
    print(df.describe())
    print("\nFirst Few Rows:")
    print(df.head())
    print("\nFull Data:")
    print(df)
    print("\n" + "=" * 50 + "\n")


def plot_housing_supply_trends(housing_supply_data):
    """
    Plot annual trends for Housing Supply data.
    """
    plot_trends(
        housing_supply_data, (0, 33),
        'Housing Supply Region 1 (Rows 1-33)',
        'Housing Supply Quantity', 'Housing Supply'
    )
    plot_trends(
        housing_supply_data, (33, 42),
        'Housing Supply Region 2 (Rows 34-42)',
        'Housing Supply Quantity', 'Housing Supply'
    )
    plot_trends(
        housing_supply_data, (42, 43),
        'Housing Supply Region 3 (Rows 43)',
        'Housing Supply Quantity', 'Housing Supply'
    )


def plot_waiting_list_trends(waiting_list_data):
    """
    Plot annual trends for Waiting List data.
    """
    plot_trends(
        waiting_list_data, (0, 33),
        'Waiting List Region 1 (Rows 1-33)',
        'Number of Households on Waiting List', 'Waiting List'
    )
    plot_trends(
        waiting_list_data, (33, 42),
        'Waiting List Region 2 (Rows 34-42)',
        'Number of Households on Waiting List', 'Waiting List'
    )
    plot_trends(
        waiting_list_data, (42, 43),
        'Waiting List Region 3 (Rows 43)',
        'Number of Households on Waiting List', 'Waiting List'
    )


def plot_combined_total_trends_by_region(housing_supply_data, waiting_list_data):
    """
    Combine total annual quantities for Housing Supply and Waiting List data.
    """
    regions = [
        (0, 33, 'Region 1 (Rows 1-33)'),
        (33, 42, 'Region 2 (Rows 34-42)'),
        (42, 43, 'Region 3 (Rows 43)')
    ]

    for start, end, region_name in regions:
        housing_year_columns = housing_supply_data.columns[3:]
        housing_total = housing_supply_data.iloc[start:end][housing_year_columns] \
            .T.apply(pd.to_numeric, errors='coerce').sum(axis=1)
        housing_total.index = housing_year_columns.astype(str)

        waiting_year_columns = waiting_list_data.columns[3:]
        waiting_total = waiting_list_data.iloc[start:end][waiting_year_columns] \
            .T.apply(pd.to_numeric, errors='coerce').sum(axis=1)
        waiting_total.index = waiting_year_columns.astype(str)

        plt.figure(figsize=(12, 8))
        plt.plot(housing_total.index, housing_total.values,
                 label=f'Total Housing Supply - {region_name}', color='b')
        plt.plot(waiting_total.index, waiting_total.values,
                 label=f'Total Waiting List - {region_name}', color='r')

        plt.title(f'Combined Trends for {region_name}')
        plt.xlabel('Year')
        plt.ylabel('Total Quantity')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def plot_trends(data, area_range, title_prefix, ylabel, data_type):
    """
    Plot annual trends and histograms for specified regions.
    """
    selected_data = data.iloc[area_range[0]:area_range[1]]
    area_names = selected_data.iloc[:, 1]
    year_columns = selected_data.columns[3:]
    year_data = selected_data[year_columns].T.apply(pd.to_numeric, errors='coerce')

    if year_data.empty or year_data.isnull().all().all():
        print(f"{title_prefix} - No valid data available.")
        return

    year_data.columns = area_names
    year_data.index = year_columns.astype(str)

    plt.figure(figsize=(12, 8))
    for area in year_data.columns:
        plt.plot(year_data.index, year_data[area], label=area)

    plt.title(f'{title_prefix} - Annual {data_type} Trends')
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    total_per_year = year_data.sum(axis=1)
    plt.figure(figsize=(10, 6))
    plt.bar(total_per_year.index, total_per_year.values.astype(float))
    plt.title(f'{title_prefix} - Total Annual {data_type}')
    plt.xlabel('Year')
    plt.ylabel(f'Total {data_type}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    housing_supply_path = Path(
        r'C:\Users\YANG\Desktop\cw1\comp0035-cw-152ChenyuYang\dclg-affordable-housing-borough.xlsx'
    )
    waiting_list_path = Path(
        r'C:\Users\YANG\Desktop\cw1\comp0035-cw-152ChenyuYang\households-on-local-authority-waiting-list.xlsx'
    )

    housing_supply_data, waiting_list_data = load_and_clean_data(
        housing_supply_path, waiting_list_path
    )

    display_data_info(housing_supply_data, "Housing Supply Data")
    plot_housing_supply_trends(housing_supply_data)
    display_data_info(waiting_list_data, "Waiting List Data")
    plot_waiting_list_trends(waiting_list_data)
    plot_combined_total_trends_by_region(housing_supply_data, waiting_list_data)


if __name__ == "__main__":
    main()
