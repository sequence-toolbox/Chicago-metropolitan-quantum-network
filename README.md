This repository is used to reproduce simulations described in [SeQUeNCe paper](https://arxiv.org/abs/2009.12000). 

# Requirements

Python version >= 3.7

# Installation

## SeQUeNCe

Follow install intstruction in SeQUeNCe to install library

## Matplotlib

pip install matplotlib

## pandas

pip install pandas

# Run

## Reproduce results in section 5.2 

Run simulation 

    expect execution time (12 processes): around 15 hours

    command:

        cd sec5.2-comparsion-of-quantum-memory-parameters
        python3 run.py

Plot graph

    command:

        python3 plot.py


## Reproduce results in section 5.3 

Run simulation with regular delay

    expect execution time (3 processes): around 8 hours

    command:

        python3 run1.py

Run simulation with low delay

    expect execution time (3 processes): around 73 hours

    command:
        python3 run2.py

## Reproduce results in section 5.4 

Run simulation

    expect execution time (20 processes): around 15 hours

    command:

        python3 run.py

Plot graph

    command:

        python3 plot.py
