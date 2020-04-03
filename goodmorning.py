# Script to run in the morning to update me on the websites and information
# that interest me.
import time


# Generate the time in a user friendly format.
seconds = time.time()
local_time = time.ctime(seconds)

# Some simple graphics to frame the update.
x = "|||"
y = "-"


print(x + y*169 + x)
print(x + y*169 + x)

# Print the time
print(local_time)
print(" ")

# Greeting
print("Greetings Robert")


# RNZ headlines

# Quanta stories

# BitCoin prices

# NZX prices


print(" ")
print(x + y*169 + x)
print(x + y*169 + x)
