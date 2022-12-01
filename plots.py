import pandas as pd
import matplotlib.pyplot as plt
from analyse_data import get_data

# Subsystem Columns
# 'CDH' - 'Time', 'Subsystems', 'GPS', 'SEP'
# 'ADC' - 'Time', 'Subsystems', 'SOL', 'ANG', 'MAG', 'WHL', 'MPU_ACC', 'MPU_GYR', 'MPU_MAG'
# 'EXP' - 'Time', 'Subsystems', 'THERM_P1', 'THERM_P2', 'I1', 'I2', 'P1A', 'P1B', 'P1C', 'P2A', 'P2B', 'P2C'
# 'EPS' - 'Time', 'Subsystems', 'THERM_P1', 'THERM_P2', 'I1', 'I2', 'P1A', 'P1B', 'P1C', 'P2A', 'P2B', 'P2C'


def EPS_plots():
    pass


CDH_df, ADC_df, EXP_df, EPS_df = get_data('logs\CDH-6-3-Seperation-Switch-21-Nov-2022-15-14-53.txt')
pd.set_option('max_row', None)

ax = plt.gca()

# df.plot(kind='line',x='name',y='num_children',ax=ax)
# df.plot(kind='line',x='name',y='num_pets', color='red', ax=ax)

# plt.show()

# df.groupby('state')['name'].nunique().plot(kind='bar')
# plt.show()



pressed_indices = []
# print(CDH_df['SEP'])
# print((CDH_df['SEP'].str[0]))

# for i in CDH_df['SEP']:
#     if i[0] == 1:
unpressed_indices = (list(CDH_df.loc[CDH_df['SEP'].str[0] == 1,'Time']))
pressed_indices = (list(CDH_df.loc[CDH_df['SEP'].str[0] == 2,'Time']))
        # unpressed_indices.append(CDH_df['Time'])
    # elif i[0] == 2:
        # pressed_indices.append(CDH_df['Time'])



# EPS_df.to_csv('EPS_Seperation_Switch_Exerice.csv')


print(unpressed_indices)
print(pressed_indices)

 