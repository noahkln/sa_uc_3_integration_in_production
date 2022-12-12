import csv
import numpy as np
from matplotlib import pyplot as plt
import os

def main():
  with open("./Overview.csv") as f:
    r = csv.reader(f)
    
    data = []
    
    for line in r:
      data.append(line)
    
    data = np.array(data)
    
    header = data[0]
    values = data[1:]
    
    instances = values[:, 0]
    cpus = values[:, 1].astype(np.int16)
    prices = values[:, 3:]
    prices[prices == ""] = "-1."
    prices = prices.astype(np.float16)
    
    header_clouds = header[3:]
    colors = {"HostedDolt": "blue", "AWS": "orange", "Azure": "lightblue", "GoogleCloud": "yellow"}
    
    for instance in set(instances):
      mask = instances == instance
      
      print(instance)
      cpus_i = cpus[mask]
      prices_i = prices[mask]
      
      for idx, h in enumerate(header_clouds):
        x = cpus_i[prices_i[:, idx].flatten() != -1]
        y = prices_i[:, idx][prices_i[:, idx].flatten() != -1]
        
        x = np.concatenate([[0], x], 0)
        y = np.concatenate([[0], y], 0)
        
        plt.scatter(x, y, marker="x", c=colors[h])
        plt.plot(x, y, label=h, c=colors[h])

      plt.title(instance)
      plt.legend()
      plt.xlabel("vCPUs")
      plt.ylabel("$ / h")
      
      if not os.path.exists("./plots"):
        os.mkdir("./plots")
        
      plt.savefig(f"./plots/{instance}.png")
      plt.show()

if __name__ == "__main__":
  main()