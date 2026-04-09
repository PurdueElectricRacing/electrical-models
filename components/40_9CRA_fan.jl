using XLSX, Interpolations, Unitful

# load fan data from xlsx and create a lut for power vs duty cycle
fan_data = XLSX.readxlsx(joinpath(@__DIR__, "../datasets/40_9CRA_fan.xlsx"))["Sheet1"][:]

# extract duty cycle and current vectors, convert to Float64
duty_vec    = Float64.(fan_data[2:end, 1]) ./ 100.0
current_vec = Float64.(fan_data[2:end, 2])
current_vec = current_vec .* 1u"A" # convert to amps

# create a lut from the data
const fan_interp = LinearInterpolation(duty_vec, current_vec, extrapolation_bc=Flat())

# 4. Single-line power function
duty2watts_40_9CRA(duty; V=24u"V") = fan_interp(duty) * V

