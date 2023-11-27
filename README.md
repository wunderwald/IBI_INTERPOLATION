# IBI_INTERPOLATION

by [Moritz Wunderwald](mailto:code@moritzwunderwald.de)

## About

Transform a discrete list of inter-beat intervals (IBIs) to a continuous function using cubic spline interpolation. The continuous function is sampled at a fixed sampling interval. The newly obtained samples are then scaled so that their sum matches the length of the original recording.
The interpolated and scaled sampled values that are the result of these operations must be interpreted differently from the discrete input values. The magnitude of single new values does not represent the measured inter-beat intervals anymore but the dynamics and the changes between values represents the changes in the "real" IBIs.