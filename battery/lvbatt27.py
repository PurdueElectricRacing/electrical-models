"""
First-order rough LV batt sizing calcs.

Author: Irving Wang (irvingw@purdue.edu)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pint import UnitRegistry

u = UnitRegistry()
ROOT = Path(__file__).resolve().parent.parent

# RS60 cell parameters
RS60_CAPACITY = 6000 * u.mA * u.hour
RS60_NOMINAL_VOLTAGE = 3.6 * u.V
RS60_DCIR = 10 * u.milliohm  # assumed

# LV Battery parameters
P_COUNT = 3
S_COUNT = 7
DEPTH_OF_CHARGE_COEFF = 4.5 / 5  # roughly the usable capacity before a cell drops below 3.0V

# Calc pack constants
batt_usable_capacity = RS60_CAPACITY * P_COUNT * DEPTH_OF_CHARGE_COEFF
batt_voltage = RS60_NOMINAL_VOLTAGE * S_COUNT
batt_energy = batt_usable_capacity * batt_voltage
batt_internal_R = (S_COUNT * RS60_DCIR) / P_COUNT

# Board loads
SINGLE_LV_BOARD_POWER = 2 * u.W # generous
TV_POWER = 15 * u.W
NUM_LV_BOARDS = 9
lv_boards_power = SINGLE_LV_BOARD_POWER * NUM_LV_BOARDS

# Cooling loads at 100% PWM from Mason
BATTERY_FANS_PACK_POWER = 200 * u.W
HEAT_EXCHANGER_FANS_PACK_POWER = 120 * u.W
PUMPS_PACK_POWER = 90 * u.W

# AMK inverter LV
INVERTERS_PACK_POWER = 45 * u.W  # measured on benchtop

# Bullet Radio
# https://dl.ubnt.com/datasheets/bullet_ac/Bullet_AC_DS.pdf pg.7
BULLET_RADIO_POWER = 7 * u.W

# TSAL
TSAL_POWER = 30 * u.W # estimated average

# Add up active loads
total_active_power = lv_boards_power + BATTERY_FANS_PACK_POWER + HEAT_EXCHANGER_FANS_PACK_POWER + PUMPS_PACK_POWER + INVERTERS_PACK_POWER + BULLET_RADIO_POWER + TSAL_POWER + TV_POWER

# Add loss due to internal resistance @ nominal voltage
# I_nominal = P_active / V_nominal
active_pack_current_nominal = total_active_power / batt_voltage
internal_power_loss = active_pack_current_nominal**2 * batt_internal_R
total_pack_power = total_active_power + internal_power_loss

# Calc runtime
runtime = (batt_energy / total_pack_power).to(u.minute)
print(f"Runtime: {runtime.magnitude:.2f} minute")
print(f"Sustained Total Power: {total_pack_power.to(u.W).magnitude:.2f} W")

# Endurance factor of safety based on Michigan 2025
ENDURANCE_RUN_TIME = (1617 / 60) * u.minute
ENDURANCE_WAIT_TIME = 10 * u.minute
total_endurance_time = ENDURANCE_RUN_TIME + ENDURANCE_WAIT_TIME
endurance_fos = (runtime / total_endurance_time).to(u.dimensionless)
print(f"Endurance factor of safety: {endurance_fos.magnitude:.2f}")

# Plot the load pie chart
labels = ["Boards", "Battery Fans", "Heat Exchanger Fans", "Pumps", "Inverter LV", "Bullet Radio", "TSAL", "TV", "Internal Loss"]
values = np.array([
    lv_boards_power.to(u.W).magnitude,
    BATTERY_FANS_PACK_POWER.to(u.W).magnitude,
    HEAT_EXCHANGER_FANS_PACK_POWER.to(u.W).magnitude,
    PUMPS_PACK_POWER.to(u.W).magnitude,
    INVERTERS_PACK_POWER.to(u.W).magnitude,
    BULLET_RADIO_POWER.to(u.W).magnitude,
    TSAL_POWER.to(u.W).magnitude,
    TV_POWER.to(u.W).magnitude,
    internal_power_loss.to(u.W).magnitude,
])
percentages = values / sum(values) * 100
labels_with_pct = [
    f"{labels[i]} ({percentages[i]:.1f}%)"
    for i in range(len(labels))
]
fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
fig.subplots_adjust(left=0.18, right=0.82, bottom=0.15, top=0.93)
ax.pie(values, labels=labels_with_pct)
ax.set_title(f"PER27 LV Power Loads")

summary = (
    f"RS60 {S_COUNT}s{P_COUNT}p pack | "
    f"Total average power: {total_pack_power.to(u.W).magnitude:.2f} W | "
    f"Runtime: {runtime.magnitude:.2f} min | "
    f"Endurance FoS: {endurance_fos.magnitude:.2f}"
)
fig.text(0.5, 0.05, summary, ha="center", va="bottom", fontsize=11)

fig.savefig(ROOT / "figures/per27_lv_loads.png")
