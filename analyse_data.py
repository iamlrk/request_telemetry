import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time


def select_line(line):
    # this would work always in this scenerio because if it's not a debug file, then the 1st return would fail. 
    # As there is no \t in debug filee, there will be one value in the array so it will fail the try
    try:
        return line.split("\t")[1].startswith("T"), False # first value checks for telemetry and second is checking for debug
    except:
        return line.strip().startswith("T"), True
        
def get_data(file_loc):
    CDH_df = ADC_df = EXP_df = pd.DataFrame()
    create_df = []
    epoch_time = {'CDH':0, 'ADC':0, 'EXP':0, 'EPS': 0} #setting epoch time 0 for the subsystems
    with open(file_loc, 'r') as log:
        for line in log:
            if select_line(line)[0]:
                # print(select_line(line))
                if select_line(line)[1]:
                    is_telemetry, subsystem, instruments_readings = split_data(line, select_line(line)[1])
                    epoch_time[subsystem] += 1
                else:
                    epoch_time, is_telemetry, subsystem, instruments_readings = split_data(line, select_line(line)[1])
                    
                if subsystem == 'CDH':
                    if 'CDH' not in create_df:
                        CDH_df = ref_dataframes('CDH')
                        create_df.append('CDH')                    
                    CDH_df = CDH_Subsystem(epoch_time[subsystem], instruments_readings, CDH_df)    
                if subsystem == 'ADC':  
                    if 'ADC' not in create_df:
                        ADC_df = ref_dataframes('ADC')
                        create_df.append('ADC') 
                    ADC_df = ADC_Subsystem(epoch_time[subsystem], instruments_readings, ADC_df)
                if subsystem == 'EXP':
                    if 'EXP' not in create_df:
                        EXP_df = ref_dataframes('EXP')
                        create_df.append('EXP') 
                    EXP_df = EXP_Subsystem(epoch_time[subsystem], instruments_readings, EXP_df)
                if subsystem == 'EPS':
                    if 'EPS' not in create_df:
                        EPS_df = ref_dataframes('EPS')
                        create_df.append('EPS') 
                    EPS_df = EPS_Subsystem(epoch_time[subsystem], instruments_readings, EPS_df)
                
    return CDH_df, ADC_df, EXP_df, EPS_df

def split_data(line, debug = True):
    if debug:
        telemetry_subsystems_readings = line.strip().split("|")
        is_telemetry = telemetry_subsystems_readings[0]
        subsystem = telemetry_subsystems_readings[1]
        instruments_readings = telemetry_subsystems_readings[2:]
        return is_telemetry, subsystem, instruments_readings

    elif not debug:
        time_telemetry_details = line.split("\t")
        epoch_time = time_telemetry_details[0]
        telemetry_subsystems_readings = time_telemetry_details[1].split('|')
        is_telemetry = telemetry_subsystems_readings[0]
        subsystem = telemetry_subsystems_readings[1]
        instruments_readings = telemetry_subsystems_readings[2:]
        return epoch_time, is_telemetry, subsystem, instruments_readings
                
def CDH_Subsystem(epoch_time, data, df):
    _df = ref_dataframes('CDH')
    _ins_dict = {'Time':epoch_time,'Subsystems': 'CDH'}
    
    # print(data)
    for instrument in data:
        readings = instrument.split(",")
        if readings[0] == 'GPS':            
            num_readings = readings[2:]
        else: 
            num_readings = [eval(i) for i in readings[1:]]
        _ins_dict[f'{readings[0]}']= num_readings[0:]
        
        # print(num_readings)
    gps = data[0].split(",")[1:]
    gps[1:] = [float(i) for i in gps[2:]]
    sep = data[1].split(",")[1:]
    sep = [float(i) for i in sep[1:]]
    
    # _df = _df.append([{'Time':epoch_time,'Subsystems': 'CDH' ,'GPS':gps, 'SEP':sep}], ignore_index=True)
    _df = pd.DataFrame([_ins_dict])
    
    return pd.concat([df, _df])
    
def EPS_Subsystem(epoch_time, data, df):
    _df = ref_dataframes('EPS')
    _ids = {65 : 'Charger', 66: 'VBatt', 67: '+5V', 68:'Radio', 69: 'SW1-5V', 70: 'SW2-5V', 71: 'SW3-5V'}
    _ins_dict = {'Time':epoch_time,'Subsystems': 'EPS'}
    for instrument in data:
        readings = instrument.split(",")
        num_readings = [float(i) for i in readings[1:]]
        if readings[0] == 'I':
            _ins_dict[f'I{_ids[num_readings[0]]}'] = num_readings[1:]
        else:
            # print(num_readings[0:])
            _ins_dict[f'{readings[0]}']= num_readings[0:]
    
    _df = pd.DataFrame([_ins_dict])
    return pd.concat([df,_df])
    
    # for instrument 

def EXP_Subsystem(epoch_time, data, df):
    _df = ref_dataframes('EXP')
    _ins_dict = {'Time':epoch_time,'Subsystems': 'EXP'}
    for instrument in data:
        readings = instrument.split(",")
        num_readings = [float(i) for i in readings[1:]]
        if readings[0].startswith("I"):
            # print(num_readings)
            if num_readings[0] == 64:
                _ins_dict['I1'] = num_readings[1:]
            elif num_readings[0] == 67:
                _ins_dict['I2'] = num_readings[1:]
        else:
            # print(num_readings[0:])
            _ins_dict[f'{readings[0]}'] = (num_readings[0])
    
    _df = pd.DataFrame([_ins_dict])

    return pd.concat([df,_df])

def ADC_Subsystem(epoch_time, data, df):
    _df = ref_dataframes('ADC')
    _ins_dict = {'Time':epoch_time,'Subsystems': 'ADC'}
    for instrument in data:
        readings = instrument.split(',')
        if readings[0] == "MPU":
            num_readings = [float(i) for i in readings[2:]]
            _ins_dict[f'MPU_{readings[1]}'] = num_readings
        else:
            num_readings = [float(i) for i in readings[1:]]
            _ins_dict[f'{readings[0]}'] = num_readings
    # _df = _df.append(_ins_dict, ignore_index=True)
    _df = pd.DataFrame([_ins_dict])
    
    return pd.concat([df, _df])
    
    
    

def ref_dataframes(subsystem: str):
    if subsystem == 'CDH':
        return pd.DataFrame(columns=['Time', 'Subsystems', 'GPS', 'SEP'])
    if subsystem == 'ADC':
        return pd.DataFrame(columns=['Time', 'Subsystems', 'SOL', 'ANG', 'MAG', 'WHL', 'MPU_ACC', 'MPU_GYR', 'MPU_MAG'])
    if subsystem == 'EXP':
        return pd.DataFrame(columns=['Time', 'Subsystems', 'THERM_P1', 'THERM_P2', 'I1', 'I2', 'P1A', 'P1B', 'P1C', 'P2A', 'P2B', 'P2C'])
    if subsystem == 'EPS':
        return pd.DataFrame(columns=['Time', 'Subsystems', 'IVBatt', 'I+5V', 'IRadio', 'ISW1_5V', 'ISW2_5V', 'ISW3_5V', 'I7', 'ICharger', 'I_E', 'DA', 'DB', 'DC', 'C'])
    
        

def plot_me(values, Solar_Direction = True):
    pass

# A C B D    


def cal_sun_pos(light_int: list):
    light_int = np.array(light_int)
    A, C, B, D = light_int[0], light_int[1], light_int[2], light_int[3]
    return np.arctan((A-C)/(B-D))

if  __name__=='__main__':
    CDH_df, ADC_df, EXP_df, EPS_df = get_data('logs\CDH-6-3-Seperation-Switch-21-Nov-2022-15-14-53.txt')
    # CDH_df, ADC_df, EXP_df = get_data('logs\log.txt', debug=False)
    print(EPS_df)
    # ADC_df['SOL_ANG'] = ADC_df['SOL'].apply(cal_sun_pos)
    # print(CDH_df['GPS'])
    # plot_me([(ADC_df['Time']),ADC_df['SOL_ANG']])
    # print((ADC_df['SOL_ANG']),(ADC_df['ANG']))
    
    