"""Simulated training dataset generation framework. 

We generate datasets of two kinds: 

 - full simulations : 
     simulated dataset from a simulated cadence and models of the photometric / spectroscopic instruments. 
 - hybrid simulations : 
     emulated datasets from real observing logs, and recycling the real SNR of the measurements. 

The module provides a generic interface for data generation, from
which all generators should derive.




"""
