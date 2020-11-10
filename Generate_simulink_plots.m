simOut = sim('System_model_PID_attempt_01','ReturnWorkspaceOutputs','on');

x = simOut.get('x');
theta = simOut.get('theta');

dx = simOut.get('dx');
dtheta = simOut.get('dtheta');

u = simOut.get('u');

plot(x,'LineWidth',2)
hold on
plot(dx,'LineWidth',2)
hold on
plot(theta,'LineWidth',2);
hold on
plot(dtheta,'LineWidth',2)

% title('Simulated Response of Inverted Pendulum with PD Controller')
title('Response of Pendulum Angle (Kp=-100)')
ylabel('Output')
xlabel('Time(s)')


% ylim([-1 4])
% hold off
hold on
grid on

% [th_os, th_t, th_p] = get_plot_values(theta.data(:),theta.time(:));
% [dth_os, dth_t, dth_p] = get_plot_values(dtheta.data(:),dtheta.time(:));
% 
% disp('theta values:')
% disp(['Peak: ',num2str(th_p),'; %OS: ',num2str(th_os),'; Tau: ',num2str(th_t)])
% disp('dtheta values:')
% disp(['Peak: ',num2str(dth_p),'; %OS: ',num2str(dth_os),'; Tau: ',num2str(dth_t)])

plot(u,'LineWidth',2)
hold off

legend({'x(m)','theta(rad)','dx(m/s)','dtheta(rad/s)','control action(V)'}, 'Location', 'southeast')
% legend({'x(m)','theta(rad)','dx(m/s)','dtheta(rad/s)'}, 'Location', 'southeast')