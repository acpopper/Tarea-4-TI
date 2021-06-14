import pandas as pd
import requests
import gspread
from gspread_dataframe import set_with_dataframe
import xml.etree.ElementTree as ET

# variables
paises = ['USA', 'EST', 'LVA', 'IRL', 'FRA', 'GBR']
indicadores = ["Number of deaths", "Number of infant deaths", "Number of under-five deaths", 
           "Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)",
          "Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)",
           "Estimates of number of homicides",
           "Crude suicide rates (per 100 000 population)",
           "Mortality rate attributed to unintentional poisoning (per 100 000 population)",
           "Number of deaths attributed to non-communicable diseases, by type of disease and sex",
           "Estimated road traffic death rate (per 100 000 population)",
           "Estimated number of road traffic deaths",
           "Mean BMI (kg/m&#xb2;) (crude estimate)",
           "Mean BMI (kg/m&#xb2;) (age-standardized estimate)",
           "Prevalence of obesity among adults, BMI &GreaterEqual; 30 (crude estimate) (%)",
           "Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)",
           "Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)",
           "Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)",
           "Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)",
           "Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)",
           "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)",
           "Estimate of daily cigarette smoking prevalence (%)",
           "Estimate of daily tobacco smoking prevalence (%)",
           "Estimate of current cigarette smoking prevalence (%)",
           "Estimate of current tobacco smoking prevalence (%)",
           "Mean systolic blood pressure (crude estimate)",
           "Mean fasting blood glucose (mmol/l) (crude estimate)",
           "Mean Total Cholesterol (crude estimate)"
          ]

df_cols = ['GHO', 'COUNTRY', 'SEX', 'YEAR', 'GHECAUSES', 'AGEGROUP', 'Display', 'Numeric', 'Low', 'High']

# requests
r0 = requests.get(f'https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_{paises[0]}.xml')
r1 = requests.get(f'https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_{paises[1]}.xml')
r2 = requests.get(f'https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_{paises[2]}.xml')
r3 = requests.get(f'https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_{paises[3]}.xml')
r4 = requests.get(f'https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_{paises[4]}.xml')
r5 = requests.get(f'https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_{paises[5]}.xml')

# roots
root0 = ET.fromstring(r0.content)
root1 = ET.fromstring(r1.content)
root2 = ET.fromstring(r2.content)
root3 = ET.fromstring(r3.content)
root4 = ET.fromstring(r4.content)
root5 = ET.fromstring(r5.content)

# poblar dataframe
roots = [root0, root1, root2, root3, root4, root5]
rows = []
for r in roots:
    for f in r.findall('Fact'):
        values = []
        for i in df_cols:
            if f.find(i) is not None:
                values.append(f.find(i).text)

        rows.append(dict(zip(df_cols, values)))

out_df = pd.DataFrame(rows, columns = df_cols)


# Escribir dataframe a google sheet
# ACCESS GOOGLE SHEET
gc = gspread.service_account(filename='client_secret.json')
sh = gc.open_by_key('1ipwc0LpqudF7K24ZYslLVTW_ejeJ9FmcSOk12d19EFQ')
worksheet = sh.get_worksheet(0) #-> 0 - first sheet, 1 - second sheet etc. 


# APPEND DATA TO SHEET
your_dataframe = pd.DataFrame()
set_with_dataframe(worksheet, out_df) #-> THIS EXPORTS YOUR DATAFRAME TO THE GOOGLE SHEET