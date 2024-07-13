
clear all
close all
clc

x = -4:0.1:4.0;
y = x;
[X,Y]=meshgrid(x,y);
Z = X.^2 + 10*(Y.^2)+X.*Y-5*(X.^1)-3*(Y.^1);
surf(X,Y,Z)
hold on;


clear x; % Clears x and y from their prededined values
clear y;
epsilon = 10^(-8); % This the permissible difference between consecutive f values
N = 100; % Maximum number of iterations
x(1) = -3; y(1) = -1;
f(1) = x(1)^2 + 10*y(1)^2+(x(1))*y(1)-5*x(1)-3*y(1);
plot3(x(1),y(1), f(1), 'ko','Linewidth',[4]);
%first value of gamma
%gamma=0.1;
%2nd value of gamma
gamma=0.085;

disp(sprintf('j    x(j)       y(j)      f(x(j),y(j))'));
for j = 1:N
    
    x(j+1) = x(j) - gamma*(2*x(j)+y(j)-5);
    y(j+1) = y(j) - gamma*(x(j)+20*y(j)-3);
    f(j+1) = x(j+1)^2 + 10*y(j+1)^2+(x(j+1))*y(j+1)-5*x(j+1)-3*y(j+1);
    plot3(x(j+1),y(j+1),f(j+1),'ko-','Linewidth',[4])

    disp(sprintf('%d   %f   %f   %f',j, x(j), y(j), f(j))); 
    if(abs(f(j+1) - f(j)) < epsilon)
         disp(sprintf('The value of j is %d and x(%d) and y(%d) are %f and %f', j, j, j, x(j), y(j)));
         break;
     end;
    
end

figure; % This is for plotting the x and y values. 
plot(x,y,'ko-');
