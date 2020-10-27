import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import mean_absolute_error
import json
import glob

def make_name(items, sep="_"):
    return sep.join(items)

def process_times(path,hf_times=None):
    lfa_runs = {}
    lfa_time = {}
    uq_time = {}
    train_time = {}
    target_runs = {}
    target_time = {}
    total_time = {}
    speed_up = {}
    #path = glob.glob("/home/yzamora/proxima/examples/tests_runs/surrogate_only/*Aug*")
    for f in path:
        #Getting HF times and finding speedup
        if hf_times is not None:
            hf_temp = int(os.path.basename(f).split('_')[6])
            hf_time = float(hf_times.set_index('Temp[K]').loc[hf_temp])
            #print(hf_time)
        uq_thresh = f.split('_')[6]
        interval = f.split('_')[10]
        temp = f.split('_')[8]
        input_name = make_name([uq_thresh, interval,temp])
         
        lfa_stats_name = open(f + "/" + 'lfa_stats.json', 'r')
        lfa_stats_results = json.load(lfa_stats_name)
        lfa_runs[input_name] = lfa_stats_results['lfa_runs']
        lfa_time[input_name] = lfa_stats_results['lfa_time']
        uq_time[input_name] = lfa_stats_results['uq_time']
        train_time[input_name] = lfa_stats_results['train_time']
        target_runs[input_name] = lfa_stats_results['target_runs']
        target_time[input_name] = lfa_stats_results['target_time']
        total_time[input_name] = lfa_stats_results['lfa_time'] + lfa_stats_results['uq_time']+ lfa_stats_results['train_time'] + lfa_stats_results['target_time']
        ##calculating spedup
        if hf_times is not None:
            speed_up[input_name] = hf_time/total_time[input_name]
        

    uq_thresholds = list(lfa_runs.keys())
    uq_list = []
    int_list = []
    for u in uq_thresholds:
        uq_list.append(u.split('_')[0])
        int_list.append(u.split('_')[1])
    lfa_time = list(lfa_time.values())
    uq_time = list(uq_time.values())
    train_time = list(train_time.values())
    target_time = list(target_time.values())
    total_time = list(total_time.values())
    if hf_times is not None:
        speed_up = list(speed_up.values())
    if hf_times is not None:              
        zipped_total_time = zip(uq_thresholds,int_list,total_time,speed_up)
    else:
        zipped_total_time = zip(uq_thresholds,int_list,total_time)
    res = sorted(zipped_total_time,key=lambda x:x[0])
    
    if hf_times is not None:
        uq_thresholds, int_list, total_time, speed_up_v = map(list,zip(*res))
    else:
        uq_thresholds, int_list, total_time = map(list,zip(*res))
    
    uq_time = {}
    speed_up = {}
    count = 0
    for u in uq_thresholds:
        uq_time[u] = format(total_time[count],'.3f')
        if hf_times is not None:
            speed_up[u] = format(speed_up_v[count],'.3f')
        count +=1
    if hf_times is not None:
        return uq_thresholds, int_list, total_time, uq_time, speed_up
    else:
        return uq_thresholds, int_list, total_time, uq_time
        

def get_true_run(true_energy, surrogate_energy_true, surrogate_energy_values):
    e_true = np.array(true_energy[0:])
    e_used = np.array(true_energy[0:])
    for s, e in zip(surrogate_energy_true['step'], surrogate_energy_values):
        e_used[s-1] = e

    #e_diff = np.abs(e_used - e_true)
    #e_diff
    #plt.plot(e_diff, '.')
    return e_used

def process_mae(path):
    ct = {}
    for count, f in enumerate(path):
        file = f + "/tests_run_data.csv"
        results = pd.read_csv(file)
        #import pdb; pdb.set_trace()
        uq_thresh = file.split('_')[6]
        surrogate_energy_true = results[results['surrogate'] == True]
        surrogate_energy_values = surrogate_energy_true['surrogate_energy']
        new_energy = results[results['surrogate']== False]
        new_energy_val = new_energy['new_energy']
        true_energy = results['true_new_energy']
        e_used = get_true_run(true_energy, surrogate_energy_true, surrogate_energy_values)
        mae = format(mean_absolute_error(true_energy,e_used),'.6f')
        #mae = mean_absolute_error(true_energy,results['surrogate_energy'])

        uq_value = f.split('_')[6]
        temp = f.split('_')[8]
        interval = f.split('_')[10]

        input_name = make_name([uq_value, interval, temp])
        uq_thresh_fl = float(uq_thresh)
        if uq_thresh_fl not in ct:
            ct[input_name]=[]
        ct[input_name].append({interval: mae})
      
    return ct

def process_mae_ct(path):
    ct = {}
    for count, f in enumerate(path):
        file = f + "/tests_run_data.csv"
        results = pd.read_csv(file)
        #import pdb; pdb.set_trace()
        uq_thresh = file.split('_')[6]
        surrogate_energy_true = results[results['surrogate'] == True]
        surrogate_energy_values = surrogate_energy_true['surrogate_energy']
        new_energy = results[results['surrogate']== False]
        new_energy_val = new_energy['new_energy']
        true_energy = results['true_new_energy']
        e_used = get_true_run(true_energy, surrogate_energy_true, surrogate_energy_values)
        mae = format(mean_absolute_error(true_energy,e_used),'.6f')
        #mae = mean_absolute_error(true_energy,results['surrogate_energy'])

        uq_value = f.split('_')[6]
        temp = f.split('_')[8]
        interval = f.split('_')[10]

        uq_thresh_fl = float(uq_thresh)
        if uq_thresh_fl not in ct:
            ct[uq_thresh_fl]=[]
        ct[uq_thresh_fl].append({interval: mae})
      
    return ct

## Converting and combine MAE Data
def mae_to_df(mae_values):
    d_mae = {
            "uq": [],
            "interval": [],
            "mae": [],
            "temperature": [],
            }

    for uq, val in mae_values.items():
        for v in val:
            interval = list(v.keys())[0]
            mae = list(v.values())[0]
            d_mae["uq"].append(float(uq.split('_')[0]))
            d_mae["interval"].append(int(interval))
            d_mae["mae"].append(float(mae))
            d_mae["temperature"].append(int(uq.split('_')[2]))
    return pd.DataFrame(d_mae)


def time_to_df(uq_time):
    d_time = {
        "uq": [],
        "interval": [],
        "time": [],
        "temperature":[],
    }
    for key,time in uq_time.items():
        uq, interval,temperature = key.split('_')
        d_time["uq"].append(float(uq))
        d_time["interval"].append(int(interval))
        d_time["time"].append(float(time))
        d_time["temperature"].append(int(temperature))
    return pd.DataFrame(d_time)

def speedup_to_df(speed_up):
    d_time = {
        "uq": [],
        "interval": [],
        "temperature":[],
        "speed_up":[],
    }
    for key,speedup in speed_up.items():
        uq, interval,temperature = key.split('_')
        d_time["uq"].append(float(uq))
        d_time["interval"].append(int(interval))
        #d_time["time"].append(float(time))
        d_time["temperature"].append(int(temperature))
        d_time["speed_up"].append(float(speedup))
    return pd.DataFrame(d_time)


