clear all;
close all;

% read data from the file
A = load("data.dat");
x = A(:,1);
y = A(:,2);
[row,column] = size(A);
n = row;
lr = 0.01;
plot(x,y,'ro');
hold on;
grid on;
m_old = 1;
c_old = 0;

k =1;

while (k < 300)

diffm = 0;
diffc = 0;
for j = 1:n
  diffc = diffc -2*(y(j) - 1*(c_old + m_old*x(j)));
  diffm = diffm -2*x(j)*(y(j) - 1*(c_old + m_old*x(j)));
  end;
  m_new = m_old -lr*diffm
  c_new = c_old -lr*diffc
  m_old = m_new;
  c_old = c_new;
  k = k + 1;
end;


