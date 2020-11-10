import os
import csv
from prettytable import PrettyTable
import numpy as np
import math
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.io import export_png

def read_csv(file_name):
    
    file_reader = csv.reader(open(file_name))
    temp = list(file_reader)[2:]

    data = {'time':[], 'output':[], 'input':[], 'velocity':[]}

    for i in temp:
        data['time'].append(float(i[0]))
        data['output'].append(float(i[1])-6.085)
        data['input'].append(float(i[2]))

    return data

def find_peaks(data):
	peaks = {'time':[],'output':[]}
	for i in range(1,len(data['time'])-1):
		if(abs(data['output'][i])>abs(data['output'][i+1]) and abs(data['output'][i])>abs(data['output'][i-1])):
			peaks['time'].append(data['time'][i])
			peaks['output'].append(abs(data['output'][i]))
		if(i<len(data['time'])-2):
			if(abs(data['output'][i])==abs(data['output'][i+1]) and abs(data['output'][i])>abs(data['output'][i-1]) and abs(data['output'][i+1])>abs(data['output'][i+2])):
				peaks['time'].append(data['time'][i])
				peaks['output'].append(abs(data['output'][i]))

	return peaks

def get_tau(data):
	
	tau = 0
	peaks = find_peaks(data)
	max_peak = np.max(peaks['output'])
	tau_val = max_peak/math.e

	n = 0
	while peaks['output'][n]!=max_peak and n < len(peaks['output']):
		n+=1
	m = n
	while peaks['output'][n]>tau_val and n < len(peaks['output']):
		n+=1

	m = (peaks['output'][n]-peaks['output'][n-1])/(peaks['time'][n]-peaks['time'][n-1])
	c = peaks['output'][n-1]-m*peaks['time'][n-1]
	tau = (tau_val-c)/m

	return tau

def get_omega(data):
	tau = 0
	peaks = []
	peaks = find_peaks(data)
	max_peak = np.max(data['output'])

	n = 0
	if peaks != []:

		while peaks['output'][n]!=max_peak and n < len(peaks['output']):
			n+=1
		m = n
		zeros = []
	
		for i in range(n, len(data['output'])-1):
			down = data['output'][i]>0 and data['output'][i+1]<0
			up = data['output'][i]<0 and data['output'][i+1]>0
			t0 = 0.0
			if up or down:
				m = (data['output'][i+1]-data['output'][i])/(data['time'][i+1]-data['time'][i])
				t0 = ((-data['output'][i])/m)+data['time'][i]
				zeros.append(t0)
		
		T_list = []
		for i in range(len(zeros)-1):
			T = zeros[i+1]-zeros[i]
			if T>0.1 and T<0.4:
				T_list.append(T)
		average = sum(T_list)/(len(T_list))
		print(T_list)
		
		return average
	else:
		return -1

def get_max(data):
	peaks = find_peaks(data)
	max_peak = np.max(data['output'])
	i = data['output'].index(max(data['output']))
	return [max_peak,data['time'][i]]

def imp_size(data):
	c = 0
	amp = 0
	t0 = 0.0
	flag = True
	for i in range(len(data['input'])):
		if data['input'][i]!=0:
			amp = data['input'][i]
			
			c += 1
			if flag:
				t0 = data['time'][i]
				flag = False

	T = data['time'][1]-data['time'][0]

	return [c*T,amp, t0]

def plot_param(tau,w,t0,y0):
	t = np.linspace(t0, t0+30, num=1000)
	print(t0)
	e = np.exp(np.divide(t-t0,-tau))
	sine = np.cos(np.multiply(w,t-t0))
	y = np.multiply(np.multiply(e,sine),y0)
	return [y,t]


if __name__ == '__main__':
	
	base_path = 'F:\\Thesis Data\\Arduino Impulse data\\'
	file_names = os.listdir(base_path)
	#file_names = ["Data8.CSV"]
	data = []
	#data = read_csv("F:\\Thesis Data\\Impulse response\\Data3.CSV")
	for i in file_names:
		file_path = base_path + i
		data.append(read_csv(file_path))

	tau = []
	T = []

	imp_T = []
	imp_A = []

	max_peak = []
	max_time = []

	t0 = []
	omega = []

	gen_data = []
	gen_time = []

	c=0

	for i in data:
		print(file_names[c],end=' ')
		c+=1
		tau.append(get_tau(i))
		T.append(get_omega(i))
		omega.append(math.pi/T[-1])
		imp = imp_size(i)
		imp_T.append(round(imp[0],2))
		imp_A.append(round(imp[1],2))
		t0.append(round(imp[2],2))
		max_peak.append(get_max(i)[0])
		max_time.append(get_max(i)[1])
		#gen_data.append(plot_param(tau[-1],omega[-1],max_time[-1],max_peak[-1])[0])
		#gen_time.append(plot_param(tau[-1],omega[-1],max_time[-1],max_peak[-1])[1])
		gen_data.append(plot_param(17.9,9.513,max_time[-1],max_peak[-1])[0])
		gen_time.append(plot_param(17.9,9.513,max_time[-1],max_peak[-1])[1])

	print()
	x = PrettyTable()
	x.field_names = ['Filename','Tau', 'Period', 'Omega', 'Imp T', 'Imp A','Imp Start','Max peak']
	
	for i in range(len(tau)):
		x.add_row([file_names[i],str(round(tau[i],1)), str(round(T[i],3)), str(round(omega[i],3)), str(imp_T[i]), str(imp_A[i]),str(t0[i]),round(max_peak[i],3)])

	print(x)

	output_file("model_validation.html")
	
	TOOLTIPS = [
    ("index", "$index"),
    ("(t,y)", "($x, $y)"),
    ("desc", "@desc"),]
	export_path = "C:\\Users\\Viibrem\\Documents\\UCT Mechatronics\\4TH YEAR\\2nd Semester\\EEE4022S Thesis\\Figures\\Bokeh\\"
	p = []
	tab = []
	for i in range(len(tau)):
		#export_file = export_path + "ImpRes_"+file_names[i][:-4] + ".png"
		
		p.append(figure(plot_width=700, plot_height=400,x_axis_label='time(s)', y_axis_label='Pendulum Angle(rad)', tooltips=TOOLTIPS))
		p[i].line(data[i]['time'],data[i]['output'], color = 'blue',legend_label = 'Real system',line_width = 2)

		#export_png(Panel(child=p[i], title=file_names[i]), filename="export_file.png")
		p[i].line(gen_time[i],gen_data[i], color = 'red', legend_label = 'Simulated system',line_width = 2)
		#p[i].line(data[i]['time'],data[i]['input'], color = 'yellow', legend_label = 'input')
		p[i].legend.location = "top_right"
		p[i].legend.click_policy="hide"
		tab.append(Panel(child=p[i], title=file_names[i]))
	tabs = Tabs(tabs=tab)
	show(tabs)

