import matplotlib.pyplot as plt

def run(value,value2,fig,a=None,b=None):
    fig.clf()
    fig.tight_layout()
    fig.suptitle("Test: "+str(value+value2))
    fig.canvas.draw()

if __name__ == '__main__':
    run(10,0,plt.figure())
    plt.show()
    