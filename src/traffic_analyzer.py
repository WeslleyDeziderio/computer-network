import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../assets/cbolao.csv')
print(df.head())

df_min_time = df[df['Time'] <= 240]
print(df_min_time.head())

print(df_min_time['Protocol'].value_counts())

client_length_pkgs = list(df_min_time[df_min_time['Source'] == '192.168.10.14']['Length'])
client_time_pkgs = list(df_min_time[df_min_time['Source'] == '192.168.10.14']['Time'])

server_to_client_length_pkgs = list(df_min_time[df_min_time['Destination'] == '192.168.10.14']['Length'])
server_to_client_time_pkgs = list(df_min_time[df_min_time['Destination'] == '192.168.10.14']['Time'])

print("Unidade de packets do cliente:", len(client_length_pkgs))

plt.scatter(client_time_pkgs, client_length_pkgs)
plt.xlabel('Time')
plt.ylabel('Packet Length')
plt.title('Client Packets: Length vs. Time')
plt.show()

plt.scatter(server_to_client_time_pkgs, server_to_client_length_pkgs)
plt.xlabel('Time')
plt.ylabel('Packet Length')
plt.title('Server to Client Packets: Length vs. Time')
plt.show()

def linear_space_transformer(space_x, space_y, slide_win):
  acc_time = 0
  acc_length = 0
  slide_pointer = slide_win
  new_linear_time_space = []
  new_linear_length_space = []
  
  counter = 0
  for i in range(len(space_x)):
    if space_x[i] > slide_pointer:
      new_linear_time_space.append(acc_time / counter)
      new_linear_length_space.append(acc_length / counter)
      slide_pointer = space_x[i] + slide_win
      acc_time = 0
      acc_length = 0
      counter = 0

    acc_time += space_x[i]
    acc_length += space_y[i]
    counter += 1
  
  new_linear_time_space.append(space_x[-1])
  new_linear_length_space.append(space_y[-1])
  
  return new_linear_time_space, new_linear_length_space

x_inicial, y_inicial = linear_space_transformer(client_time_pkgs, client_length_pkgs, 1)

plt.plot(x_inicial, y_inicial, color='b', label='upload')

x_final, y_final = linear_space_transformer(server_to_client_time_pkgs, server_to_client_length_pkgs, 1)

plt.plot(x_final, y_final, '-.', color = "orange", label="download")
plt.legend(loc="upper left")
plt.xlabel("seconds") 
plt.ylabel("bytes") 
plt.title('Output in time', fontdict={'fontsize': 14}) 
plt.show() 

def ecdf(data):
   
  """
  this function creates the x and y axis 
  for the Emperical Culmulative Distribution Function 
  """
  xaxis = np.sort(data)
  yaxis = np.arange(1, len(data) + 1) / len(data)
  
  return xaxis, yaxis

x_download, y_download = ecdf(df_min_time[df_min_time['Destination'] == '192.168.10.14']['Length'])
x_upload, y_upload = ecdf(df_min_time[df_min_time['Source'] == '192.168.10.14']['Length'])

plt.plot(x_download, y_download, linestyle="none", marker=".", color = "orange", label="download")
plt.plot(x_upload, y_upload, linestyle="none", marker=".", color = "blue", label="upload")
plt.title("Packages sizes distribution",  fontdict={'fontsize': 14})
plt.xlabel("bytes")
plt.ylabel("ECDF")
plt.legend(loc="lower right")
plt.show()

df_min_time[df_min_time['Protocol'] == 'UDP'].plot(kind='scatter', x='Time', y='Length', title='UDP over time')