% Written by Venki om 12-03-2023

clear all;
close all;
x = -12:0.02:12;
y = (x.^2.*cos(x) - x)/10;
plot(x,y,'b-');
grid on
hold
a(1) = 7;
b(1) = (a(1)^2 * cos(a(1)) - a(1))/10;
alpha = 0.1;
n = 1000;

for j = 2:n
  a(j) = a(j-1) -alpha*(2*a(j-1)*cos(a(j-1)) - a(j-1)*a(j-1)*sin(a(j-1)) -1)/10;
  b(j) = (a(j-1)^2 * cos(a(j-1)) - a(j-1))/10;
end;
plot(a,b,'r*-');


