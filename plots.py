import pandas as pd
from itertools import count
import numpy as np
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

def plot_plots(file_loc,subsystem, instrument, exp, power=False,debug=True,view_plot = False, save_plot = False, animate = False):
    plt_graphs = {}
    
    CDH_df, ADC_df, EXP_df, EPS_df = get_data(file_loc, debug)
    # print(ADC_df)
    
    if subsystem == 'EPS':    
        if instrument in ['IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISW2_5V', 'ISW3_5V', 'ICharger']:
            if not power:
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
                plt.title(f"{subsystem}-{instrument}-IV")
                plt_graphs[f'{subsystem}_{instrument}'] = plt
            elif power:
                fig, ax = plt.subplots()
                ax.plot(EPS_df['Time'], EPS_df[instrument].str[0]*EPS_df[instrument].str[1])
                ax.set_xlabel('Time')
                ax.set_ylabel('Power mWatts')
                ax.set_title(f"{subsystem}-{instrument}-Power")
                
                
        
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
            ax.set_xlim(20, 100)
            plt.title(f"{subsystem}-{instrument}")
            plt_graphs[f'{subsystem}_{instrument}'] = plt
        
        elif instrument == 'DA':
            #todo : plot it
            fig, axs = plt.subplots(1, sharex=True, sharey=True)
            # fig.suptitle('PS_DA')
            plt.plot(EPS_df['Time'], EPS_df['DA'].str[1]*EPS_df['DA'].str[2])
            plt.title('EPS-DA')
            plt.xlabel('Time - s')
            plt.ylabel('Power - mW')
            
            # axs[0].plot(EPS_df['Time'], EPS_df['DA'].str[0])
            # axs[1].plot(EPS_df['Time'], EPS_df['DA'].str[1])
            # axs[2].plot(EPS_df['Time'], EPS_df['DA'].str[2])
            
    elif subsystem == 'EXP':
        if instrument in ['THERM_P1', 'THERM_P2']:
            # fig,ax = plt.subplots()
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
                    
                    plt.legend(loc='lower left')
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
                # plt.ylabel("Acceleration - $mm/s^2$") # , fontsize = 14)
                # plt.ylabel("$^o$/s") # , fontsize = 14)
                plt.ylabel("milli Gauss") # , fontsize = 14)
                
                plt.legend(loc='lower left')
                plt.tight_layout()
        elif instrument == 'ANG':
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='polar')
            c = ax.scatter(ADC_df['ANG'].str[0]*np.pi/180, ADC_df['Time'],c='orange' ,s=40, cmap='hsv', alpha=0.75)
            d = ax.scatter([0, 275*np.pi/180, 180*np.pi/180, 275*np.pi/180, 0*np.pi/180, 90*np.pi/180, np.pi/4 ,225*np.pi/180], [0, 10, 20, 30, 40, 50, 52, 60], c='blue')
            
            # plt.polar(ADC_df['Time'], ADC_df['ANG'].str[0], color="green", marker='x')
            plt.title(f'Angle of Sun without Ambient Light')
            # plt.grid(True)
            
            # plt.xlabel("Time - s") # , fontsize = 14)
            # plt.ylabel("Light Intensity", color="green")
    if view_plot:
        plt.tight_layout()
        plt.grid(True)
        plt.show()
    
    if save_plot:
        plt.tight_layout()
        plt.grid()
        fig.savefig(f'plots\{subsystem}_{instrument}_{exp}.png',
            format='png',
            dpi=200,
            bbox_inches='tight')
    
    return plt_graphs



if __name__ == '__main__':
    
    file_loc = 'logs\ADC-SolarSensor_WithAmbient-02-Dec-2022-15-56-30.txt'
    # file_loc = 'logs\ADC-SolarSensor_WithoutAmbient-02-Dec-2022-16-02-59.txt'
    # file_loc = "logs\CDH-6-3-Seperation-Switch-21-Nov-2022-15-14-53.txt"
    # file_loc = "logs\ADC-MPU_ACC-02-Dec-2022-14-54-47.txt"
    # file_loc = "logs\ADC-MPU_ACC-02-Dec-2022-15-07-20.txt" #use this for gyro
    # file_loc = "logs\ADC-MPU_ACC_Diff_Pos-02-Dec-2022-17-13-18.txt"
    # file_loc = 'logs\CDH-Power-21-Nov-2022-14-51-32.txt'
    # file_loc = 'logs\ADC_MAGTORQ.dat'
    # file_loc = 'logs\EPS-standby.dat'
    # file_loc = 'logs\EPS_EXP_P1.dat'
    # file_loc = 'logs\EPS_ADC_magtorq.dat'
    # subsystem = 'ADC'
    # exp = 'without_ambient'
    # exp = 'with_ambient'
    # subsystem = 'EPS'
    subsystem = 'ADC'
    # exp = 'seperation_switch'
    exp = 'ANG_amb_with_ref'
    # instruments = ['IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISW2_5V', 'ISW3_5V','ICharger', 'I_E', 'DA','DB', 'DC', 'C']
    instruments = ['ANG'] #'ANG' # ['MPU_ACC', 'MPU_GYR', 'MPU_MAG']
    for instrument in instruments:
        plt_values = plot_plots(file_loc,subsystem, instrument, exp, power=True,debug=True,animate=False,view_plot=True, save_plot=True)
        # plt_values[f'{subsystem}_{instrument}'].show()
    
    # file_loc = 'logs\thermal_1129.txt'
    
    
    # CDH_df, ADC_df, EXP_df, EPS_df = get_data(file_loc)
    
    

