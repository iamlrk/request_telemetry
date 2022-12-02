from analyse_data import get_data


file_loc = "logs/thermal_1129.txt"

_, _, EXP_df, _ = get_data(file_loc, debug=False)

print(EXP_df)