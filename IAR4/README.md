## Task 4 - Line Following

authors: Benedict Finsterwalder and Venkata Asodi

In this task we had to implement a simple line following behaviour. 
Additionally we implemented a collision avoidance and random walk.
The robot's collision avoidance is always active.
The random walk is active as long as no line has been found.
If the line is found, the line following behaviour starts.
In our case this is just:
if right sensor detects the line, turn left
if left sensor detects the line, turn right
if both detect the line, go straight

Also, if it loses the line, it will go back to the random walk behaviour which is first 5 seconds of walking straight.
This is enough to time to walk across the gap in case the robot is at the intersection.

This of course is not enough to correctly follow the line. 
The robot will turn away from the line if the robot is outside the circle.
If it is inside one of the circles, it will follow that circle but as soon as it crosses over to the other side, it will walk away.
