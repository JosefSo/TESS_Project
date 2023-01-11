import matplotlib.pyplot as plt
from lightkurve import search_targetpixelfile
# import matplotlib.pyplot as plt

pixelfile = search_targetpixelfile("KIC 8462852", quarter=16).download();
pixelfile.plot(frame=1)

plt.show()
