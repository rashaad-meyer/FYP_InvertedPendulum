function [overshoot,tau,peak] = get_plot_values(data,time)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    data = [0; data];
    [pks,n] = findpeaks(abs(data));
    peak = pks(1);
    overshoot = pks(2)*100/peak;
    tau = -1;
    c = 0;
    for i = 1:length(pks)
        if pks(i)<0.05*peak
            c = i;
            break
        end
    end
    m = (pks(c)-pks(c-1))/(time(n(c))-time(n(c-1)));
    tau = (pks(c)-pks(c-1))/m+time(n(c-1));

end

