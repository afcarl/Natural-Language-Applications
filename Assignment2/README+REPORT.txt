To run the program use the following command : 
    python emcoin <param-init-mode> <no-iters>

param-init-mode can be random or uniform

Observations:

For initialization mode uniform parameter values after 

1. 10 iterations: <0.5 , 0.648, 0.648>

2. 25 iterations: <0.5, 0.648, 0.648>

3. 50 iterations: <0.5, 0.648, 0.648>

For uniform initialization EM converges after 1 iteration only with converged
values mentioned as above

For intitialization mode random paramters values after

1. 10 iterations: <0.37052655, 0.86259337, 0.52168399>

2. 25 iterations: <0.41846599, 0.63207449, 0.65945983>

3. 50 iterations: <0.69947069, 0.86077339, 0.1527793>

For random initialization EM converges for paramters  p1 and p2 quickly but
gives different values for paramters p. 

Basically it converges to different local minima for each random
initialization. The hypothesis is that due to non-convex objective function
we see this behaviour. Each time parameters are initialized with random values
and as EM basically does coordinate ascent so each initialization is landed on
different point. 

For uniform initialization all paramters are initialized at same point so EM
converges to same point after convergence.




