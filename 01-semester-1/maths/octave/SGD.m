clear all;
close all;

% read data from the file
A = load("data.dat");
x = A(:,1);
[minx,idx_minx] = min(x);
[maxx,idx_maxx] = max(x);

xx = linspace(minx,maxx);


y = A(:,2);
[row,column] = size(A);
n = row;
lr = 0.01;
plot(x,y,'r*');
hold on;
grid on;
m_old = 1;
c_old = 0;

linear_n = (1:1:n);
B = perms(linear_n);


k =1;
while (k < 200)

q = ceil(rand(1,1)*factorial(n));
diffm = 0;
diffc = 0;
for j = 1:n
  diffc = diffc -2*(y(B(q,j)) - 1*(c_old + m_old*x(B(q,j))));
  diffm = diffm -2*x(B(q,j))*(y(B(q,j)) - 1*(c_old + m_old*x(B(q,j))));
  end;
  m_new = m_old -lr*diffm;
  c_new = c_old -lr*diffc;
  zz = m_new*xx + c_new;
  plot(xx,zz,'b-');
  drawnow;
  m_old = m_new;
  c_old = c_new;
  k = k + 1;
end;
slope = m_new
intercept = c_new



