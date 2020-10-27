# Notebook descriptions #
    
1. **Energy_trajectory** 
    - Returns surrogate(orange) and target function(green) results and compares them to results of using only the target function (blue dots)
    - Specific trajectories and entire ranges can be plotted, i.e. all results for UQ 0.2
  
2. **MAE vs Interval**
    - Compares results of MAE with interval use. Results are mainly used to find best interval for a simple surrogate as Proxima consistently does not
     use a predetermined retrain interval

3. **Scatter_plot_method_comparison**
    - Compares the methods against each other by looking at the MAE and Time (uses average hf runtime as upper limit lines)
  
4.  **Speedup_bar_chart**
    - Compares times and speedups between different methodologies
  
### Experiments that can be compared and found in proxima_data ###

**Proxima Experiments**

    "NORT-Proxima_dynamicalpha", #Proxima - dynamic alpha with no retrain interval
    "NORT-Proxima_static-alpha", #Proxima - precalcualted alpha, no retrain interval
    "DA_RT50", ## Proxima - dynamica alpha, testing single RT interval of 50 
    "DAallUQ_TEMP1000", ## Proxima - testing different retrain intervals and UQ's

**Simple Surrogate Experiments**

    "surrogate_only", ## Simple surrogate implementation
    "SS-UQ02-NORT_staticalpha", # Simple surrogate, uq:0.2, no retrain interval   
    "SST1000_bestparameters", ## Simple surrogate - with different Retrain intervals tested
    "SS_RI300", ## Simple Surrogate with RI 300
    "SS-UQ02_I50", ## Simple surrogate, uq: 0.2, RI: 50
