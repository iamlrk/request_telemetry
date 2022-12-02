import pandas as pd
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from analyse_data import get_data


# Subsystem Columns
# 'CDH' - 'Time', 'Subsystems', 'GPS', 'SEP'
# 'ADC' - 'Time', 'Subsystems', 'SOL', 'ANG', 'MAG', 'WHL', 'MPU_ACC', 'MPU_GYR', 'MPU_MAG'
# 'EXP' - 'Time', 'Subsystems', 'THERM_P1', 'THERM_P2', 'I1', 'I2', 'P1A', 'P1B', 'P1C', 'P2A', 'P2B', 'P2C'
# 'EPS' - 'Time', 'Subsystems', 'IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISV2_5V', 'ISV3_5V', 'ICharger', 'I_E', 'DA', 'DB', 'DC', 'C'
# x_vals = []
# y_vals = []

    



def plot_plots(file_loc, subsystem, instrument, view_plot = False, save_plot = False, animate = False):
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
        
        
    
    elif subsystem =='ADC':
        if instrument in ['MPU_ACC', 'MPU_GYR', 'MPU_MAG']:
            x = ADC_df['Time']
            y1 = ADC_df[instrument].str[0]
            y2 = ADC_df[instrument].str[1]
            y3 = ADC_df[instrument].str[2]
            # print(x, y1, y2, y3)
            
            if animate:
                def animate_me():
                    plt.cla()
                    plt.plot(x,y1, label = 'x-acc')
                    plt.plot(x,y2, label = 'y-acc')
                    plt.plot(x,y3, label = 'z-acc')
                    
                    plt.legend(loc='upper left')
                    plt.title(f'{instrument}')
                    plt.tight_layout()
                ani = FuncAnimation(plt.gcf(), animate_me, interval=1000)
            else:
                    plt.plot(x,y1, label = 'x-acc')
                    plt.plot(x,y2, label = 'y-acc')
                    plt.plot(x,y3, label = 'z-acc')
                    plt.title(f'{instrument}')
                    plt.legend(loc='upper left')
                    plt.tight_layout()
    
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

    subsystem = 'ADC'
    instruments = ['MPU_ACC', 'MPU_GYR', 'MPU_MAG'] # ['IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISW2_5V', 'ICharger', 'I_E', 'DB', 'DC', 'C']

    for instrument in instruments:
        plt_values = plot_plots(file_loc,subsystem, instrument, view_plot=True)
        # plt_values[f'{subsystem}_{instrument}'].show()
    
    # file_loc = 'logs\thermal_1129.txt'
    
    
    # CDH_df, ADC_df, EXP_df, EPS_df = get_data(file_loc)
    
    

