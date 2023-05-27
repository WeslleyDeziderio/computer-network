import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

df = pd.read_csv('../assets/amouranth2.csv')
print(df.head())

df_min_time = df[df['Time'] <= 300]
print(df_min_time.head())