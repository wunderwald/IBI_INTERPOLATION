# IBI_INTERPOLATION

by [Moritz Wunderwald](mailto:code@moritzwunderwald.de)

## About

Transform discrete inter-beat intervals (IBIs) to a continuous function using cubic spline interpolation. The continuous function is sampled at a fixed sampling interval. A filter is applied to remove out-of-range samples before the interpolation step.  Optionally, the interpolated time-series can be scaled so that its sum is equal to the length of the original recording if a redistribution of IBIs is needed instead of a pure interpolation.