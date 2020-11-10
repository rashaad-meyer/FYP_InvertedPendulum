n_y = 10;
n_u = 10;

A_c = [0      1       0     0;
       0    -20       0     0;
       0      0       0     1;
       0      0   90.25 -0.112];
B_c = [0; 24; 0; -4.06];

C = [0 0 1 0];    
D = 0;

ts = 0.05;
A = eye(4)+ts*A_c;
B = ts*A*B_c;


P_y = [];
H_y = [];

for i = 1:n_y
   P_y = [P_y; C*A^i];
end

for i = 1:n_y
    temp = [];
    for j = 1:n_u
        if j>i
            temp = [temp D];
        else
            temp = [temp C*A^(i-j)*B];
        end
    end
    H_y = [H_y; temp];
end

T = [];

ONE = ones(n_u,1);

for i = 1:n_u
    T = [T; ones(1,i) zeros(1,n_u - i)];
end

G = H_y;
disp(H_y)
disp(P_y)

R = 0.000001*eye(n_u);

K = inv(transpose(G)*G+R)*transpose(G);

x = [0;0;0;0.5];

u_last = 0;
y = [0];
u_list = [0];
t = [0];

x = [0];
dx = [0];
theta = [0];
dtheta = [0.5];

dt = 0.001;

for i = 1:10000
    f_k = P_y*[x(i);dx(i);theta(i);dtheta(i)];
    r = zeros(size(f_k));
    u = K*(r-f_k);
    
    u(1) = min(3.3, max(-3.3, u(1)));
    
    x(i+1) = dx(i)*dt+x(i);
    dx(i+1) = (-20*dx(i)+2.2*u(1))*dt+dx(i);
    
    theta(i+1) = dtheta(i)*dt+theta(i);
    dtheta(i+1) = (-0.112*dtheta(i)+90.25*theta(i)-4.06*u(1))*dt+dtheta(i);
    t(i+1) = dt*i;
    
    if t(i+1) == 0.2
        theta(i+1) = theta(i+1)+0;
    end
    
    u_list(i+1) = u(1);
    
end

plot(t,x,'LineWidth',2)
hold on
plot(t,dx,'LineWidth',2)
hold on
plot(t,theta,'LineWidth',2)
hold on
plot(t,dtheta,'LineWidth',2)
hold on
% stairs(t(2:length(t)),u_list(2:length(t)),'g','LineWidth',2)
hold off
% legend({'x(m)','dx(m/s)','theta(rad)','dtheta(rad/s)','control action(V)'})
legend({'x(m)','dx(m/s)','theta(rad)','dtheta(rad/s)'})
% legend({'x(m)','theta(rad)'},'Location','southeast')
xlim([0 1])

xlabel('Time(s)')
ylabel('Output')
title('MPC Tuning Simulation 4')
grid on

[th_os, th_t, th_p] = get_plot_values(theta.',t.');
[dth_os, dth_t, dth_p] = get_plot_values(dtheta.',t.');

disp('theta values:')
disp(['Peak: ',num2str(th_p),'; %OS: ',num2str(th_os),'; Tau: ',num2str(th_t)])
disp('dtheta values:')
disp(['Peak: ',num2str(dth_p),'; %OS: ',num2str(dth_os),'; Tau: ',num2str(dth_t)])
% y = P_y*x+H_y*u;
% plot(y)

























