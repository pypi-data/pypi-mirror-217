# Bakta reordering script: "bact_order.py"
This is a simple tool that takes the bakta output fna file and tsv file with annotations as input, and reorders the genome based on the origin of replication.
The origin of replication (In my limited experience!) is where initiation starts and so it makes sense we standardise our annotations based on this.

Simply put, it sets this to base '1' of your genome. 
Also, it will ONLY reorder the first contig.

# Install
```sh
pip install bact-order==0.0.1
```

# Usage
```sh
bact_order.py -i1 <bakta.tsv> -i2 <bakta.fna> 
```

# Third party software
This package has currently been tested with biopython version 1.81, and pandas 1.5.3
