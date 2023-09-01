% Gradient Descent Method for the function f(x,y) = x^2 + 3y^2
% Starting point is 2, 2

clear all
close all
clc

x = -4:0.1:4.0;
y = x;
[X,Y]=meshgrid(x,y);
Z = X.^2 + 3*Y.^2;
surf(X,Y,Z); hold on;


clear x; % Clears x and y from their prededined values
clear y;
epsilon = 10^(-8); % This the permissible difference between consecutive f values
N = 20; % Maximum number of iterations
x(1) = 2; y(1) = 2;
f(1) = x(1)^2 + 3*y(1)^2;
plot3(x(1),y(1), f(1), 'ko','Linewidth',[4]);
view(-75,50)

disp(sprintf('j    x(j)       y(j)      f(x(j),y(j))'));
for j = 1:N
    tau = (x(j)^2 + 9*y(j)^2)/(2*x(j)^2 + 54*y(j)^2);
    %tau=0.05;
    x(j+1) = x(j) - tau*2*x(j);
    y(j+1) = y(j) - tau*6*y(j);
    f(j+1) = x(j+1)^2 + 3*y(j+1)^2;
    plot3(x(j+1),y(j+1),f(j+1),'ko-','Linewidth',[4])

    disp(sprintf('%d   %f   %f   %f',j, x(j), y(j), f(j))); 
    if(abs(f(j+1) - f(j)) < epsilon)
         disp(sprintf('The value of j is %d and x(%d) and y(%d) are %f and %f', j, j, j, x(j), y(j)));
         break;
     end;
    
end

figure; % This is for plotting the x and y values. 
plot(x,y,'ko-');
