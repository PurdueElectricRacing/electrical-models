# PER Electrical Modeling

## Directory Structure
- `battery/`: Battery sizing and performance
- `circuits/`: Models of complete circuits
- `components/`: Data-driven or physics-based models of individual components/sensors
- `datasets/`: Raw data from bench testing and datasheets in xlsx/csv format
- `figures/`: Plots and images generated from the models
- `signals/`: Filtering and signal generation simulations

# Results
## SDC Simulation
RELAY_CTRL = LOW -> SDC open:
![spice](figures/SDC/SPICE.png)

No Faults:
![nominal](figures/SDC/no_fault.png)

Open Circuit:
![open_circuit](figures/SDC/open_circuit.png)

Single Fault:
![single_fault](figures/SDC/single_fault.png)

Multiple Faults:
![multiple_faults](figures/SDC/multi_fault.png)

## Signal Filtering
We used the isoSPI model to catch a bug in our filtering circuit:
![isoSPI](figures/isoSPI_bad_RC.png)

## Battery Sizing
LV battery sizing:
![per26_lv_loads](figures/per26_lv_loads.png)
Runtime: 53.70 minute
Sustained Total Power: 451.60 W
Endurance factor of safety: 1.68

## Sensor Modeling
Thermistor modeling:
![thermistor_plot](figures/B57861S0103_thermistor.png)

Oil temp sensor analysis:
![oil temp error](figures/oil_temp_error.png)

Shockpot sensor analysis:
![shock pot error](figures/shock_pot_error.png)
