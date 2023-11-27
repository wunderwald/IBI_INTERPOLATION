# IBI_INTERPOLATION

by [Moritz Wunderwald](mailto:code@moritzwunderwald.de)

## About

Transform a discrete list ob inter-beat intervals (IBIs) to a continuous function using cubic spline interpolation. The continuous function is sampled at a fixed sampling interval. The newly obtained samples are then scaled so that their sum matches the sum of the original IBIs.