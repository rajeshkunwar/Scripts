#!/bin/bash

#Author: Rajesh
#Veresion: 1.2 (Version 1.1 did not have square and square root options)


# This script will perform simple arithematic operations including decimal numbers.

echo -e "Choose Option: \n 1: For Addition, Subtraction, Multiplication and Division of TWO numbers. \n 2: For Square and Square Root of A number"

read OPTION

if [ "$OPTION" -eq 1 ]                  # Start of the outer loop. The main LOOP.

then

    echo "Enter First Number. Decimals are accepted"

    read FIRST_NUM

    sleep 1

    echo "Enter Second Number. Decimals are accepted"

    read SECOND_NUM

    sleep 2

    echo -e "What operation would you like to perform.\n Enter A OR a for Addition, S OR s for Substraction, M OR m for multiplication,  D OR d for division."

    read INPUT

    sleep 2

    CHOICE=${INPUT^^}           # This converts the input to uppercase so you only have to compare one letter.


      if [ "$CHOICE" = "A" ]    # Start of the first inner loop

      then

        SUM=$(echo "scale=2; $FIRST_NUM+$SECOND_NUM" | bc)      # Since bash is weak with floating numbers, tools like bc have to used to get decimal values.
                                                        # Hopefully its installed on your system.
        echo -e "The sum of numbers you entered is:\n $SUM"

      elif [ "$CHOICE" = "S" ]

      then

        SUB=$(echo "scale=2; $FIRST_NUM-$SECOND_NUM" | bc)

        echo -e "The difference of numbers you entered is:\n $SUB"

      elif [ "$CHOICE" = "M" ]

      then

        MUL=$(echo "scale=2; $FIRST_NUM*$SECOND_NUM" | bc)

        echo -e "The product of numbers you entered is:\n $MUL"

         elif [ "$CHOICE" = "D" ]

      then

         DIV=$(echo "scale=2; $FIRST_NUM/$SECOND_NUM" | bc)

        echo -e "The division of numbers you entered is:\n $DIV"

      else

        echo -e "You did not choose a right option.\n `sleep 1` Exiting the program ......."

        sleep 1

      fi                        # The first inner loop finishes here

elif [ "$OPTION" = 2 ]          # The outer loop continues

then

   echo "Enter SQ or sq for Square, SR or sr for Square Root"

   read INPUT2

   sleep 1

   echo "Enter a number"

   read NUM

   CHOICE2=${INPUT2^^}

     if [ "$CHOICE2" = "SQ" ]      # Start of the second inner loop

     then

        SQUARE=$(echo "scale=2; $NUM*$NUM" | bc)

        echo -e "The square of the number you entered is:\n $SQUARE"

     elif [ "$CHOICE2" = "SR" ]

     then

        SQROOT=$(echo "scale=2; sqrt($NUM)" | bc)

        echo -e "The square root of the number you entered is:\n $SQROOT"

     else

        echo -e "You did not choose a right option.\n `sleep 1` Exiting the program ......."

     fi                   # The second inner loop finishes here

else

   echo -e "You did not choose a right option.\n `sleep 1` Exiting the program ......."

   fi                      # The main loop finally ends