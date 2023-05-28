import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../assets/cbolao.csv')
# print(df.head())

df_min_time = df[df['Time'] <= 240]
# print(df_min_time.head())

# print(df_min_time['Protocol'].value_counts())

client_length_pkgs = list(df_min_time[df_min_time['Source'] == '192.168.10.14']['Length'])
client_time_pkgs = list(df_min_time[df_min_time['Source'] == '192.168.10.14']['Time'])

server_to_client_length_pkgs = list(df_min_time[df_min_time['Destination'] == '192.168.10.14']['Length'])
server_to_client_time_pkgs = list(df_min_time[df_min_time['Destination'] == '192.168.10.14']['Time'])

print("Unidade de packets do cliente:", len(client_length_pkgs))

fig_1, ax_1 = plt.subplots()

ax_1.set(ylabel = 'Packet Length', xlabel = 'Time')
ax_1.set_title('Client Packets: Length vs. Time')
ax_1.plot(client_time_pkgs, client_length_pkgs)

fig_2, ax_2 = plt.subplots()
ax_2.set(ylabel = 'Packet Lenght', xlabel = 'Time')
ax_2.set_title('Server to Client Packets: Length vs. Time')
ax_2.plot(server_to_client_time_pkgs, server_to_client_length_pkgs)

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

x_final, y_final = linear_space_transformer(server_to_client_time_pkgs, server_to_client_length_pkgs, 1)

fig3, ax3 = plt.subplots()
ax3.plot(x_final, y_final, color = 'b', label = 'upload')
ax3.plot(x_final, y_final, '-.', color = "orange", label="download")
ax3.set(xlabel = 'seconds', ylabel = 'bytes')
ax3.set_title('Output in time', fontdict={'fontsize': 14})
ax3.legend(loc="upper left")


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

fig4, ax4 = plt.subplots()
# fig5, ax5 = plt.subplots()

ax4.plot(x_download, y_download, color = "orange", label="download")
ax4.plot(x_upload, y_upload, color = "blue", label="upload")

ax4.set_title("Packages sizes distribution",  fontdict={'fontsize': 14})
# ax5.set_title("Packages sizes distribution",  fontdict={'fontsize': 14})

ax4.set(xlabel = "bytes", ylabel = "ECDF")
# ax5.set(xlabel = "bytes", ylabel = "ECDF")

ax4.legend(loc="lower right")
# ax5.legend(loc="lower right")

plt.show()

df_min_time[df_min_time['Protocol'] == 'UDP'].plot(kind='scatter', x='Time', y='Length', title='UDP over time')