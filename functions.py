import matplotlib.pyplot as plt
from parameters import *

def weightCalc(results):
    results.w1 = results.w0 * W1W0
    results.w2 = results.w0 * W2W1 * W1W0
    results.w3 = results.w0 * results.wcruise * W2W1 * W1W0
    results.wf = results.w0 * results.wfw0
    results.we = results.w0 * results.wew0

"""
def plotSensibility(AR_list):
    leg = ["Wf/W0", "Wcruise/W0", "We/W0"]
    figSize = (10, 6)

    plt.figure(figsize=figSize)
    for idx, list in enumerate([wfw0_list, wcruise_list, wew0_list]):
        plt.plot(AR_list, list, "o", label = leg[idx])

    plt.xlabel("AR")
    plt.legend(loc = "best", fontsize = 11)
    plt.savefig("fuelFracs.png")
    ##################################33
    plt.figure(figsize=figSize)
    plt.plot(AR_list, ldmax_list, "o")

    plt.ylabel("L/Dmax")
    plt.xlabel("AR")
    plt.savefig("LDmax.png")
    ##################################33
    plt.figure(figsize=figSize)
    plt.plot(AR_list, w0_list, "o")

    plt.ylabel("W0")
    plt.xlabel("AR")
    plt.savefig("W0.png")
"""