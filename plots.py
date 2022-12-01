import pandas as pd
import matplotlib.pyplot as plt
from analyse_data import get_data

# Subsystem Columns
# 'CDH' - 'Time', 'Subsystems', 'GPS', 'SEP'
# 'ADC' - 'Time', 'Subsystems', 'SOL', 'ANG', 'MAG', 'WHL', 'MPU_ACC', 'MPU_GYR', 'MPU_MAG'
# 'EXP' - 'Time', 'Subsystems', 'THERM_P1', 'THERM_P2', 'I1', 'I2', 'P1A', 'P1B', 'P1C', 'P2A', 'P2B', 'P2C'
# 'EPS' - 'Time', 'Subsystems', 'IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISV2_5V', 'ISV3_5V', 'ICharger', 'I_E', 'DA', 'DB', 'DC', 'C'


def plot_plots(file_loc, subsystem, instrument, view_plot = False, save_plot = False):
    plt_graphs = {}
    
    CDH_df, ADC_df, EXP_df, EPS_df = get_data(file_loc)
    
    
    if subsystem == 'EPS':    
        if instrument in ['IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISW2_5V', 'ISW3_5V', 'ICharger']:
            fig,ax = plt.subplots()
            ax.plot(EPS_df['Time'],
                    EPS_df[instrument].str[0],
                    color="red")
            ax.set_xlabel("Time - s") # , fontsize = 14)
            ax.set_ylabel("Voltage",
                        color="red")


            
            ax2=ax.twinx()
            ax2.plot(EPS_df['Time'], 
                    EPS_df[instrument].str[1],
                    color="blue")
            ax2.set_ylabel("Current",color="blue") # ,fontsize=14)
            plt.title(f"{subsystem}-{instrument}")
            plt_graphs[f'{subsystem}_{instrument}'] = plt
        
        elif instrument == 'I_E':
            fig,ax = plt.subplots()
            for i in range(len(EPS_df[instrument])):
                ax.plot(EPS_df['Time'], EPS_df[instrument].str[i])
                ax.set_xlabel("Time - s") # , fontsize = 14)
                ax.set_ylabel("Voltage",
                        color="red")
            plt.title(f"{subsystem}-{instrument}")
            plt_graphs[f'{subsystem}_{instrument}'] = plt
        
        elif instrument in ['DB', 'DC', 'C']:
            fig,ax = plt.subplots()
            # print(EPS_df[instrument])
            ax.plot(EPS_df['Time'], EPS_df[instrument].str[0])
            ax.set_xlabel("Time - s") # , fontsize = 14)
            plt.title(f"{subsystem}-{instrument}")
            plt_graphs[f'{subsystem}_{instrument}'] = plt
        
        elif instrument == 'DA':
            #todo : plot it
            pass
            
    elif subsystem == 'EXP':
        if instrument in ['THERM_P1', 'THERM_P2']:
            fig,ax = plt.subplots()
            # print(EPS_df[instrument])
            ax.plot(EPS_df['Time'], EPS_df[instrument].str[0])
            ax.set_xlabel("Time - s") # , fontsize = 14)
            plt.title(f"{subsystem}-{instrument}")
            plt_graphs[f'{subsystem}_{instrument}'] = plt
                       
    
    
    if view_plot:
        plt.show()
    
    if save_plot:
        fig.savefig(f'plots\{subsystem}_{instrument}.png',
            format='png',
            dpi=200,
            bbox_inches='tight')
    
    return plt_graphs


if __name__ == '__main__':
    
    file_loc = 'logs\CDH-6-3-Seperation-Switch-21-Nov-2022-15-14-53.txt'

    subsystem = 'EPS'
    instruments = ['IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISW2_5V', 'ICharger', 'I_E', 'DB', 'DC', 'C']

    for instrument in instruments:
        plt_values = plot_plots(file_loc,subsystem, instrument, view_plot=False)
        plt_values[f'{subsystem}_{instrument}'].show()

