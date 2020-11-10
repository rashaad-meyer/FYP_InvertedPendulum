theta = [0];
dtheta = [0.5];
t = [0];
dt = 0.01;
u = 0;
t_final = 0.5;
i = 1;

while t_final>t(i)
    ddtheta = -0.112*dtheta(i)+90.25*theta(i)-4.06*u;
    dtheta(i+1) = ddtheta*dt + dtheta(i);
    theta(i+1) = dtheta(i)*dt + theta(i);
    t(i+1) = dt*i;
    i  = i+1;
end

plot(t,theta);
ylabel('Pendulum Angle(rad)')
xlabel('Time(s)')
