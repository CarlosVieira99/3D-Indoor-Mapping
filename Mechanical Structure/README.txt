                   .:                     :,                                          
,:::::::: ::`      :::                   :::                                          
,:::::::: ::`      :::                   :::                                          
.,,:::,,, ::`.:,   ... .. .:,     .:. ..`... ..`   ..   .:,    .. ::  .::,     .:,`   
   ,::    :::::::  ::, :::::::  `:::::::.,:: :::  ::: .::::::  ::::: ::::::  .::::::  
   ,::    :::::::: ::, :::::::: ::::::::.,:: :::  ::: :::,:::, ::::: ::::::, :::::::: 
   ,::    :::  ::: ::, :::  :::`::.  :::.,::  ::,`::`:::   ::: :::  `::,`   :::   ::: 
   ,::    ::.  ::: ::, ::`  :::.::    ::.,::  :::::: ::::::::: ::`   :::::: ::::::::: 
   ,::    ::.  ::: ::, ::`  :::.::    ::.,::  .::::: ::::::::: ::`    ::::::::::::::: 
   ,::    ::.  ::: ::, ::`  ::: ::: `:::.,::   ::::  :::`  ,,, ::`  .::  :::.::.  ,,, 
   ,::    ::.  ::: ::, ::`  ::: ::::::::.,::   ::::   :::::::` ::`   ::::::: :::::::. 
   ,::    ::.  ::: ::, ::`  :::  :::::::`,::    ::.    :::::`  ::`   ::::::   :::::.  
                                ::,  ,::                               ``             
                                ::::::::                                              
                                 ::::::                                               
                                  `,,`


http://www.thingiverse.com/thing:3179502
3D scanner (lidar, ultrasonic) v2 by mochr is licensed under the Creative Commons - Attribution license.
http://creativecommons.org/licenses/by/3.0/

# Summary

This is concept of cheap 3D scanner with lidar ( http://www.benewake.com/en/tfmini.html ).
I use Arduino Nano with CNC shield + A4988 driver for stepper motor. 
Scanner write position (x,y,z) to SD card.

buttons for home H(orizontal), for home V(ertical), scan and stop(not working yet).

v1

https://www.youtube.com/watch?v=Q2yE-5H5z7s&feature=youtu.be

v2
https://www.youtube.com/watch?v=YJjjC-yB83Y

for now:
this is first test build. 
NOT work microstep, so 1 step is 1,8° (not good for scanner-working on)
lidar accuracy is not acceptable - see video

UPDATE:
modify for change lidar or ultrasonic senor.
enabled multistep on driver(shield has wrong wiring...)
In archive scannerv2.zip are all files



more info. http://mochr.cz/3d-scanner/