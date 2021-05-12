from functions import *

def gen_y(f,l):
    return [f(y) for y in l]

def create_reliability_plot():
    x = np.linspace(0.0, 5000.0, 1000)
    plt.figure(1)
    plt.plot(x, gen_y(reliability(1,1),x),label='1 out of 1')
    plt.plot(x, gen_y(reliability(1,3),x),label='1 out of 3') 
    plt.plot(x, gen_y(reliability(1,5),x),label='1 out of 5') 
    plt.plot(x, gen_y(reliability(2,3),x),label='2 out of 3') 
    plt.plot(x, gen_y(reliability(3,5),x),label='3 out of 5')
    plt.ylabel("Reliability")
    plt.xlabel("Time (h)")
    plt.legend()
    plt.savefig('Reliability.png')
    #plt.show() 

def create_availability_plot():
    x=np.arange(MINN,MAXN+1)
    plt.figure(2)
    #plt.plot(x, gen_y(log_availability(lambda n:1),x),label='1 out of n')
    #plt.plot(x, gen_y(log_availability(lambda n:math.floor(n/2)+1),x),label='n/2+1 out of n')
    plt.plot(x, gen_y(log_availability(lambda n:n),x),label='n out of n')
    fun,lab=find_linear()
    plt.plot(x, gen_y(log_availability(fun),x),label=lab)
    plt.xlim([MINN,MAXN+1])
    plt.ylabel("Nines")
    plt.xlabel("Number of nodes")
    plt.legend()
    #plt.savefig('Availability.png')
    plt.show() 

if __name__=="__main__":
    print("Started\n")
    #create_reliability_plot()
    create_availability_plot()
    print("Done\n")




'''def gen_exp_y(f,l):
    return np.exp([f(y) for y in l])

def gen_large_y(f,l):
    return [100*f(y) for y in l]

def gen_log10_y(f,l):
    return np.negative(np.log10([1-f(y) for y in l]))'''