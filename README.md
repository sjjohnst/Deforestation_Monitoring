## Deforestation_Monitoring
September 2022 - December 2022
Author: Sam Johnston

Building an application to monitor user-specified area(s) of interest for deforestation.
Work is building towards allowing conservationists to detect rapidly when illegal harvesting of forest occurs, and intervene accordingly.
The Earth Observation data is from the Sentinel-1 satellite, and I am using GRD images.

Rough Outline:
  1. A GUI to set areas of interest for monitoring + to load old data for comparison
  2. Retrieve most recent satellite observations intersecting the specific area, and compare to a baseline observation:
      2.1 If we do not detect change, we discard the new observation (we are only concerned with change occuring)
      2.2 If we do detect change, we save this observation, and it becomes the new baseline (to compare future observations to)
