import pandas as pd
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import collections

from analyse_data import get_data


# Subsystem Columns
# 'CDH' - 'Time', 'Subsystems', 'GPS', 'SEP'
# 'ADC' - 'Time', 'Subsystems', 'SOL', 'ANG', 'MAG', 'WHL', 'MPU_ACC', 'MPU_GYR', 'MPU_MAG'
# 'EXP' - 'Time', 'Subsystems', 'THERM_P1', 'THERM_P2', 'I1', 'I2', 'P1A', 'P1B', 'P1C', 'P2A', 'P2B', 'P2C'
# 'EPS' - 'Time', 'Subsystems', 'IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISV2_5V', 'ISV3_5V', 'ICharger', 'I_E', 'DA', 'DB', 'DC', 'C'
# x_vals = []
# y_vals = []

    

SIGMA = 5.670374419e-8

def plot_plots(file_loc,subsystem, instrument, debug=True,view_plot = False, save_plot = False, animate = False):
    plt_graphs = {}
    
    CDH_df, ADC_df, EXP_df, EPS_df = get_data(file_loc, debug)
    # print(ADC_df)
    
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
        
        if instrument == 'VIP':
            # print(EXP_df['I1'].str[1])
            # VI = EPS_df['I1'].str[1]*EPS_df['I2'].str[2]
            fig,ax = plt.subplots()
            ax.plot(EXP_df['I1'].str[1]*EXP_df['I2'].str[2], SIGMA*((EXP_df['P1A']+EXP_df['P1B']+EXP_df['P1C'])/3)**4)
            plt_graphs[f'{subsystem}_{instrument}'] = plt
            
            
        
        
    
    elif subsystem =='ADC':
        if instrument in ['MPU_ACC', 'MPU_GYR', 'MPU_MAG']:
            # print(x, y1, y2, y3)
            
            if animate:
                def animate_me(i):
                    x = ADC_df['Time']
                    y1 = ADC_df[instrument].str[0]
                    y2 = ADC_df[instrument].str[1]
                    y3 = ADC_df[instrument].str[2]
                    
                    plt.cla()
                    
                    plt.plot(x,y1, label = f'x{instrument}')
                    plt.plot(x,y2, label = f'y{instrument}')
                    plt.plot(x,y3, label = f'z{instrument}')
                    
                    plt.legend(loc='upper left')
                    plt.title(f'{instrument}')
                    plt.tight_layout()
                    
                ani = FuncAnimation(plt.gcf(), animate_me, interval=1000)
                plt.show()
                
            else:
                x = ADC_df['Time']
                y1 = ADC_df[instrument].str[0]
                y2 = ADC_df[instrument].str[1]
                y3 = ADC_df[instrument].str[2]
                plt.plot(x,y1, label = f'x{instrument}')
                plt.plot(x,y2, label = f'y{instrument}')
                plt.plot(x,y3, label = f'z{instrument}')
                plt.title(f'{instrument}')
                plt.xlabel("Time - s") # , fontsize = 14)
                plt.ylabel("Acceleration - $mm/s^2$") # , fontsize = 14)
                
                plt.legend(loc='upper left')
                plt.tight_layout()
        elif instrument == 'ANG':
            
            plt.plot(ADC_df['Time'], ADC_df['ANG'].str[0])
                    
    
    if view_plot:
        plt.tight_layout()
        plt.grid()
        plt.show()
    
    if save_plot:
        plt.tight_layout()
        plt.grid()
        fig.savefig(f'plots\{subsystem}_{instrument}.png',
            format='png',
            dpi=200,
            bbox_inches='tight')
    
    return plt_graphs



if __name__ == '__main__':
    
    # file_loc = 'logs\ADC-SolarSensor_WithAmbient-02-Dec-2022-15-56-30.txt'
    file_loc = "logs\CDH-6-3-Seperation-Switch-21-Nov-2022-15-14-53.txt"
    # subsystem = 'ADC'
    subsystem = 'EPS'
    
    instruments = ['IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISW2_5V', 'ICharger', 'I_E', 'DB', 'DC', 'C']
    # instrument = 'ANG' # ['MPU_ACC', 'MPU_GYR', 'MPU_MAG']
    for instrument in instruments:
        plt_values = plot_plots(file_loc,subsystem, instrument, debug=True,animate=False,view_plot=False, save_plot=True)
        # plt_values[f'{subsystem}_{instrument}'].show()
    
    # file_loc = 'logs\thermal_1129.txt'
    
    
    # CDH_df, ADC_df, EXP_df, EPS_df = get_data(file_loc)
    
    

