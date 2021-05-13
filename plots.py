from functions import *

def gen_y(f,l):
    return [f(y) for y in l]

def create_reliability_plot():
    x = np.arange(0, 5000, 200)
    plt.figure(1)
    plt.plot(x, gen_y(reliability(1,1),x),label='1 out of 1',marker="o")
    plt.plot(x, gen_y(reliability(1,3),x),label='1 out of 3',marker="v") 
    plt.plot(x, gen_y(reliability(1,5),x),label='1 out of 5',marker="x") 
    plt.plot(x, gen_y(reliability(2,3),x),label='2 out of 3',marker="s") 
    plt.plot(x, gen_y(reliability(3,5),x),label='3 out of 5',marker="*")
    plt.yticks(np.linspace(0,1,11))
    plt.grid(color='lightgrey')
    plt.ylabel("Reliability")
    plt.xlabel("Time [h]")
    plt.legend()
    plt.savefig('Reliability.png')
    #plt.show()

def create_availability_plot(benchmark_m=2, benchmark_n=3):
    x=np.arange(MINN,MAXN+STEP,STEP)
    plt.figure(2)
    plt.plot(x, gen_y(log_availability(lambda n:1),x),label='1 out of n',marker="o")
    plt.plot(x, gen_y(log_availability(lambda n:math.floor(n/2)+1),x),label='n/2+1 out of n',marker="v")
    plt.plot(x, gen_y(log_availability(find_linear(benchmark_m=benchmark_m,benchmark_n=benchmark_n)),x),label=f'{benchmark_m} out of {benchmark_n} level',marker="x") #Approximately n-log(n)
    plt.xlim([np.min(x)-1,np.max(x)+1])
    plt.ylim(bottom=0)
    plt.grid(color='lightgrey')
    plt.ylabel("Steady state availability [nines]")
    plt.xlabel("Number of nodes")
    plt.legend()
    plt.savefig('Steady state availability.png')
    plt.show() 

if __name__=="__main__":
    print("Started\n")
    create_reliability_plot()
    create_availability_plot()
    print("Done\n")
