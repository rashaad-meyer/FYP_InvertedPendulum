# FYP_InvertedPendulum
Source code from my final year project of controlling inverted pendulum with both MPC and classical control

## Generate_simulink_plot.m
Gets data from System_model_PID_attemp_01.slx and plots it

## MPC_tuning_simulation.m
Simulates linear inverted pendulum system with a Model Predictive Controller that uses GPC

## PID_Controller_attemp.ino
PD controller implemented using arduino

## find_values.py
Calculates the frequency and damping factor from a .csv file.

## get_plot_values.py
Uses find_values.py to calculate the frequencies and damping factors for multipe .csv files. It displays these values and also plots the system response.

## motor_tf_plot.py
Calculates time constants and final values from multiple .csv files and plots the responses.

## unstable_itegrate_theta.m
Plot validating that the inverted pendulum system is unstable
