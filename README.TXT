Made by: John Mai
Date: 8/23/2020
Project Prompt: https://users.soe.ucsc.edu/~pang/30/s20/prog2/index2.html
This project is from my Programming Abstractions class at UC Santa Cruz

Project Description: Created a simulation using pygame to model the spread of
COVID 19 under certain assumptions in a hypothetical situation.

Quick run down of what each color means:

Unexposed (BLUE): The people who haven't encountered the virus at all so far.

Infected ((ORANGE): People who have the virus but have no symptoms of the disease.
An unexposed person has an 80% chance of getting infected on coming in contact with
a person carrying the virus. An infected person may either get sick with symptoms in
5 days, or stay infected (contagious) for a period of 15 days and thereafter develop
immunity to the disease.


Sick ((RED): People who have the virus and are sick with symptoms. Sick dots do not move
and become stationary until they recover and become immune, or until they die. Of those
infected, 50% get sick with the disease. In 10 days, a sick person may either recover
completely (98%) and develop lifelong immunity, or die (2%).

Dead ((BLACK) : People who die from the disease. 2% of the sick die. Dead dots do not move
 and do not infect other dots anymore.


Immune ((GREEN): There are three ways of getting to this state: 1) People who got
sick with COVID-19, and recovered and thereby, have developed lifelong immunity.
2) People who were infected but didn't develop symptoms, and became immune once they
stopped being contagious. 3) We assume that 5% of the entire population was naturally
immune to the disease to begin with, and can't be affected by the virus at all.