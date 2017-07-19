# baxter_alvar
This package is used to localize an RGB-D camera looking at Baxter, by using ar_track_alvar and displaying a marker on Baxter's display. It is very preliminary.
It uses a fork of ar_track_alvar, which publishes the TF transform from the marker to the camera (instead of the other way around).
It is also currently hard-coded as hell.
