import os
import numpy as np
import csv
from prettytable import PrettyTable
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import magma
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
import math
from prettytable import PrettyTable

def read_csv(file_name):
    
    file_reader = csv.reader(open(file_name))
    temp = list(file_reader)

    data = {'time':[], 'output':[]}

    for i in temp:
        data['time'].append(float(i[1])/1000)
        data['output'].append(float(i[0]))

    return data

def get_tf(speed, time):
	
	y_inf = sum(speed[-20:])/len(speed[-20:])
	y_tau = (1-math.exp(-1))*y_inf
	n = 0

	while(speed[n]<y_tau):
		n+=1
	n-=1

	t0_n = 0
	while (speed[t0_n] == 0):
		t0_n += 1

	t0 = time[t0_n-1]

	m = (speed[n+1]-speed[n])/((time[n+1]-time[n]))
	tau = (y_tau - speed[n])/m+time[n]-t0

	return [y_inf, tau, t0]

def plot_param(tau,y_inf,t0):
	t = np.linspace(t0, t0+0.9, num=900)
	e = np.exp(np.divide(t-t0,-tau))
	
	y = np.multiply(y_inf, 1 - e)
	return [t,y]

if __name__ == '__main__':

	base_path = 'F:\\Thesis Data\\Motor Force Data\\'
	file_names = os.listdir(base_path)
	data = []
	#data = read_csv("F:\\Thesis Data\\Impulse response\\Data3.CSV")
	for i in file_names:
		file_path = base_path + i
		data.append(read_csv(file_path))

	speed = []
	for i in range(len(data)):
		temp = []
		for j in range(len(data[i]['time'])-1):
			rad_s = 0.4*(data[i]['output'][j]-(data[i]['output'][j+1]))/1065
			if rad_s == 0:
				temp.append(0.0)
			else:
				time_elapsed = data[i]['time'][j]-(data[i]['time'][j+1])
				temp.append(rad_s/time_elapsed)
		speed.append(temp)

	speed_filtered = []
	speed_time = []
	for i in range(len(speed)):

		temp = []
		temp_time = []
		for j in range (4,len(speed[i])-4):

			avg = speed[i][j-4]+speed[i][j-3]+speed[i][j-2]+speed[i][j-1]
			avg += speed[i][j+4]+speed[i][j+3]+speed[i][j+2]+speed[i][j+1]
			avg += speed[i][j]
			avg = avg/9
			
			temp.append(avg)
			temp_time.append(data[i]['time'][j])
			
		speed_filtered.append(temp)
		speed_time.append(temp_time)

	y_inf = []
	tau = []
	t0 = []
	gen_data = []

	for i in range(len(speed_time)):
		temp = get_tf(speed_filtered[i],speed_time[i])
		tau.append(temp[1])
		y_inf.append(temp[0])
		t0.append(temp[2])
		gen_data.append(plot_param(tau[-1],y_inf[-1],t0[-1]))


	x = PrettyTable()

	v_list = []
	A = []

	for i in file_names:
		v = float(i[-7:-4])*3.3/255
		v_list.append(round(v,1))

	for i in range(len(y_inf)):
		A.append(y_inf[i]/v_list[i])

	x.field_names = ["Filename","Y_inf","Tau","Input","A"]
	for i in range(len(file_names)):
		x.add_row([file_names[i],round(y_inf[i],2),round(tau[i],4),v_list[i],round(A[i],2)])



	print(x)
	output_file("motor_tf.html")
	
	TOOLTIPS = [
    ("index", "$index"),
    ("(t,y)", "($x, $y)"),
    ("desc", "@desc"),]

	p = []
	tab = []
	for i in range(len(data)):
		#export_file = export_path + "ImpRes_"+file_names[i][:-4] + ".png"
		
		p.append(figure(plot_width=650, plot_height=300,x_axis_label='Time(seconds)', y_axis_label='Cart Veclocity(m/s)', tooltips=TOOLTIPS))
		#p[i].line(data[i]['time'],data[i]['output'], color = 'blue',legend_label = 'raw data')
		#export_png(Panel(child=p[i], title=file_names[i]), filename="export_file.png")
		#p[i].line(gen_time[i],gen_data[i], color = 'red', legend_label = 'sim')
		#p[i].line(data[i]['time'][:-1], speed[i], color = 'red', legend_label = 'Recorded')
		p[i].line(speed_time[i], speed_filtered[i], color = 'blue', legend_label = 'Real system',line_width = 2)
		p[i].line(gen_data[i][0], gen_data[i][1], color = 'red', legend_label = 'Simulated',line_width = 2)
		p[i].legend.location = "bottom_right"
		p[i].legend.click_policy = "hide"
		tab.append(Panel(child=p[i], title=file_names[i]))

	tabs = Tabs(tabs=tab)
	show(tabs)
