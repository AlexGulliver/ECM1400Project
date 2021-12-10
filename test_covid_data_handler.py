from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 638
    #Should require 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data ('nation_2021-10-28.csv' ) )
    assert int(last7days_cases) == int(240299)
    assert int(current_hospital_cases) == int(7019)
    assert int(total_deaths) == int(141_544)
