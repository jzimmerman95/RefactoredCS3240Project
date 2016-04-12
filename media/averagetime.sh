#!/bin/bash
#Colleen McCarthy, clm5uz, 3-19-15, section 104
#averagetime.sh
#Define i for the for loop
i=1
#Define variable to hold "quit"
q=quit
#Define variable for sum of time
sum=0
#Define max of loop
max=5
#Define iteration number
itr=1
#Request exponent value
echo "enter the exponent for counter.cpp: " 
#Read in exponent value to variable e
read e
#Check if the var e is quit or a number
#Run the program five times and get the time
if [[ "$e" = "$q" ]] ; then
    exit 1
else
    for i in {1..5} ; do
	echo "Running iteration $itr..."
	RUNNING_TIME_1=`./a.out $e | tail -1`
	echo "time taken: $RUNNING_TIME_1 ms"
	sum=`expr $sum + $RUNNING_TIME_1`
	i=`expr $i + 1`
	itr=`expr $itr + 1`
    done
fi
#Compute average
AVERAGE=`expr $sum / $max`
#Output average
echo "$max iterations took $sum ms"
echo "Average time was $AVERAGE ms"




