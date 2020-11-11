# WoxBot

## Introduction
Our goal is to obtain virtual creatures capable of performing specific tasks in their environment by exploring certain strategies and adapting those whenever necessary.


The ARENA robot - called WOXBOT has a vision system consisting of a simulated camera and an image processing algorithm that classify the visual patterns to provide input to a motor system controlled by a deterministic finite state machine (FSM).


This FSM is an automaton obtained from an optimization procedure implemented with a genetic algorithm, and applied through generations of robots.


## Implementation
<img width="1356" alt="Implementation" src="https://raw.githubusercontent.com/Kartik-715/WoxBot/main/docs/images/Implementation.png">

<img width="1358" alt="Arena" src="https://raw.githubusercontent.com/Kartik-715/WoxBot/main/docs/images/Arena.png">


One of the tasks that WOXBOT has to perform in this first project is to be aware of nutrients (yellow pyramids) and hurting entities (red cubes) that are present in ARENA.

The visual information is gathered from the 3D surrounding scene by projecting it to a view port with 3 color channels, namely R (red), G (green) and B (blue).


To differentiate and spatially locate these entities, we have designed an algorithm that takes input the visual feed taken from the robot and outputs the location of target colour in the view according to the intensities of the color in various regions.


<img width="1359" alt="Processing Workflow" src="https://raw.githubusercontent.com/Kartik-715/WoxBot/main/docs/images/ProcessingWorkflow.png">

<img width="1358" alt="Evolutionary Process" src="https://raw.githubusercontent.com/Kartik-715/WoxBot/main/docs/images/EvolutionProcess.png">


## Technical Workflow

<img width="1272" alt="Technical Workflow" src="https://raw.githubusercontent.com/Kartik-715/WoxBot/main/docs/images/Technical_Workflow.png">

## Results

<img width="1361" alt="Expanded Result" src="https://raw.githubusercontent.com/Kartik-715/WoxBot/main/docs/images/Screenshot%202020-11-12%20at%202.01.03%20AM.png">
