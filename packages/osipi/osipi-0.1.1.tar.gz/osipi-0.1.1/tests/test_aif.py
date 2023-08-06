import numpy as np
import matplotlib.pyplot as plt
import osipi.dc.models.concentration.aif as aif

def test_parker():
    t = np.arange(0, 6*60, 1)
    ca = aif.parker(t)
    plt.plot(t, ca)

if __name__ == "__main__":
    test_parker()