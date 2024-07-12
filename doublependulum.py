import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
m1=1
m2=1
l1=1
l2=1
g=9.8 
def df(t,variables):
    th1,th2,om1,om2=variables
    A=np.zeros((2,2))
    b=np.zeros(2)
    A[0,0]=l1*(m1+m2)
    A[0,1]=m2*l2*np.cos(th1-th2)
    A[1,0]=l1*np.cos(th1-th2)
    A[1,1]=l2
    b[0]=(m1+m2)*g*np.cos(th1)-m2*l2*np.sin(th1-th2)*om2**2
    b[1]=l1*np.sin(th1-th2)*om1**2+g*np.cos(th2)
    dom1,dom2=np.linalg.solve(A,b)
    return np.array([om1,om2,dom1,dom2])
sol=solve_ivp(df, [0,10],[0,-np.pi/6,0,0],t_eval=np.linspace(0,10,500),method='RK45')
t=sol.t
th1=sol.y[0]
th2=sol.y[1]
om1=sol.y[2]
om2=sol.y[3]
x1=l1*np.cos(th1)
y1=-l1*np.sin(th1)
x2=x1+l2*np.cos(th2)
y2=y1-l2*np.sin(th2)
fig=plt.figure(dpi=144)
ax=fig.gca()
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_aspect("equal")
ax.grid()
pendulum,=ax.plot([],[],"-o",lw=2)
time_mark=ax.text(0.05,0.9, '',transform=ax.transAxes)
def init():
    x=[0.0,x1[0],x2[0]]
    y=[0.0,y1[0],y2[0]]
    pendulum.set_data(x,y)
    time_mark.set_text('')
    return pendulum,time_mark
def update(num):
    x=[0.0,x1[num],x2[num]]
    y=[0.0,y1[num],y2[num]]
    pendulum.set_data(x,y)
    time_mark.set_text('time = %.1fs'%(num*0.02))
    return pendulum,time_mark
ani=FuncAnimation(fig,update,frames=range(len(y1)),interval=20,blit=True,init_func=init)
ani.save('双摆.mp4',writer='ffmpeg')
plt.show()