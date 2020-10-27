# Q3 Student Proposal

We may choose one of the following:

1. Find out the malfunctioning meter
     - Base on the decreasing value
     - Base on the stagnant frequency

2. Leakage detection
Base on the forecast value, we can set a threshold to determine the possibility of gas leakage.

3. Set a reasonable report reading value.
Currently the meter report a reading when the last marginal 2 cubic foot (or higher) of natural gas passes through the meter.
We could
     - set a larger meter report reading during peak hour (maybe 4 cubic foot) to reduce the processing and bandwidth requirements.
     - set a smaller mater report reading during off-peak hour (maybe 1 cubic foot). If the meter is keep reporting the reading during the night off-peak hour(especially 11pm to 5am), then there is a possibility of gas leakage.