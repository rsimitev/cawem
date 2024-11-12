---
title: "Interactive cellular automaton for visualisation of waves in excitable media" 
author: Radostin D. Simitev
tags:
  - cellular automaton
  - cardiac excitation
  - autowaves
  - cardiac modelling
  - educational simulation
  - Python
authors:
  - name: Radostin D. Simitev
    orcid: 0000-0002-2207-5789
    affiliation: "1"
affiliations:
 - name: School of Mathematics and Statistics, University of Glasgow, Glasgow, UK
   index: 1
date: 2024-11-05
bibliography: paper.bib
---

# Summary

This paper presents a computer implementation of a cellular automaton
model demonstrating nonlinear dissipative wave behavior in excitable
media, such as cardiac tissue. The model is  implemented within a single lightweight Python
script with minimal software  dependencies. Designed with simplicity
and interactivity in mind, the script is suitable for use in publc
outreach and engament events, classroom demonstrations and educational
workshops.  Through a series of predefined scenarios with default
model parameters, users can observe 
plane waves, spiral waves, reentry and chaotic patterns that
illustrate fundamental properties of excitation waves. Additionally, users can specify 
custom parameter values, experiment and explore wave dynamics on
their own. This flexibility encourages audience engagement and
interaction.

# Statement of need

## Waves in excitable media

Many spatially-extended systems in nature exhibit self-sustained,
wavelike behaviour, often arising spontaneously and propagating
through the medium without an external, continuous driving
[@Cross2009] [@Sinha2014], [@Meron1992], [@Tyson1988]. Examples include oscillatory
chemical reactions such as the Belousov–Zhabotinsky and
Briggs–Rauscher reactions, the spread of fire, epidemic waves, bee colony shimmering, "Mexican waves" in
crowds, patterns on leaves and lichens, and biological signals such as
nerve impulses and cardiac electrical excitation. These phenomena are
all examples of nonlinear dissipative waves in *excitable*/*active*
media. The properties of nonlinear excitation waves are fundamentally
different from those of linear waves seen in nonactive media (e.g.,
water waves, sound waves, seismic waves, or electromagnetic waves in
radio and optical domains) as summarised in Table 1. 



| Property  | Linear waves | Nonlinear excitation waves |
|-----------------|-----------------|-----------------|
| Conservation of energy   | yes  | no   |
| Conservation of amplitude  | no   | yes   |
| Conservation of shape  | no   | yes   |
| Interference  | yes   | no   |
| Annihilation | no   | yes  |
| Reflection | yes  | no  |
| Diffraction | yes   | yes  |
| Descend into chaos | no | yes  |

*Table 1*: Comparison of properties of linear waves and nonlinear excitation waves.

## Educational context

Waves in excitable media are an important subject of scientific
research with numerous applications. Many researchers in the field
feel compelled to share this fascinating topic with the general public in
accessible, interactive and engaging format.

The software described here has been used, in conjunction with a brief
presentation, at Open Day events at the author's home institution, in
dialogue sessions with cardiac patients, and it will soon feature 
in a dedicated stall at the Glasgow Science  Festival
([`gla.ac.uk/events/sciencefestival`](https://www.gla.ac.uk/events/sciencefestival)). 

The software is well-suited to other similar outreach venues, including other
Science Festivals,
Pint of  Science ([`pintofscience.co.uk`](https://pintofscience.co.uk)),
TED talks ([`ted.com`](https://www.ted.com)), STEM for Britain
  events ([`stemforbritain.org.uk`](https://stemforbritain.org.uk)), Cafe
  Scientifique ([`cafescientifique.org`](http://cafescientifique.org)),
  Royal Institution Masterclasses
  ([`rigb.org/learning/ri-masterclasses`](https://www.rigb.org/learning/ri-masterclasses)),
  and local school visits. Each of these platforms offers unique opportunities to engage
diverse audiences with interactive demonstrations of wave behaviours in
excitable media. 

## Software need

There is a software need for engaging, interactive, and portable
demonstrations that can be used for introducing the dynamics
of excitable media to the general public effectively.

Nonlinear waves in spatially extended excitable systems
are best modeled with continuous partial differential equations (PDEs) of
the reaction-diffusion type [@@Cross2009]. These advanced PDE models, as
applied to phenomena like chemical reactions or cardiac
electrophysiology, require hundreds of coupled rate equations that
must be solved across multiple spatial and temporal scales. 
High-performance, parallelized research codes, such as 'Chaste'
[@Cooper2020] and 'openCARP' [@Plank2021] for cardiac
electrophysiology, are available to handle these complex equations in
tissue and organ simulations. However, these sophisticated codes are
not practical for public outreach due to their technical demands. 

Cellular automata, proposed as a model for
excitable media waves in the 1940s [@wiener1946], offer a simplified
alternative. While they do not fully capture the intricate structure
and properties of actual excitable tissues, cellular automata gained
popularity in the 1980s and 1990s, e.g. [@Gerhardt1990], for their
intuitive interpretation and simplicity. 
Although general-purpose cellular automata libraries e.g. [@Antunes2021]
and agent-based platforms like NetLogo [@wilensky1999] are available,
they often require numerous software dependencies and have complex
syntaxes that detract from the purpose at hand and limit their accessibility.


In order to bridge this gap, we present a Python script that
simulates one of the simplest models of waves in excitable media -
a cellular automaton that can be used to illustrate their basic
features and characteristic behaviour. The code
consists of a standalone script that can be run on any system with a
Python interpreter, requiring only two widely available libraries --
`NumPy` for numerical computation and `Matplotlib` for visualization.  


# Software description/documentation

## Cellular automaton

The cellular automaton model considered here takes the form of a
uniform 2D grid of cells and evolves the states of the cells in time.
The transition rules of the model are defined in function `update_grid()`.
At  any time step $k$ the cell at position $(i, j)$ can be in an
"excited", a "resting" or a "refractory" state $S_{i,j}^k$ given by
the values
$$
S_{i,j}^k =
\begin{cases}
\displaystyle
1 & \text{if "excited"}, \\[1mm]
0 & \text{if "resting"},  \\[1mm]
[-1,-R_{i,j}] & \text{if "refractory"}, R_{i,j}>0,
\end{cases},
$$
where $R_{i,j}$ is the "maximal refractory state" of the cell. The
state $S_{i,j}^k$ is then evolved according to the rules
$$
S_{i,j}^k = 
\begin{cases} 
\displaystyle
1 & \text{if } S_{i,j}^{k-1} = 0 \text{ and } \sum\limits_{m=-1}^{1} \sum\limits_{n=-1}^{1} \delta(S_{i+m,j+n}^{k-1}, 1) \geq n_{i,j}, \\[3mm]
\displaystyle -R_{i,j} & \text{if } S_{i,j}^{k-1} = 1, \\[3mm]
\displaystyle S_{i,j}^{k-1} + 1 & \text{if } S_{i,j}^{k-1} < 0, \\[3mm]
\displaystyle 0 & \text{if } S_{i,j}^{k-1} = -R_{i,j}. 
\end{cases}
$$
Here $n_{i,j}$ is the "threshold for excitation" of cell $(i, j)$
specifying the minimum number of excited neighbours required for a
resting cell to transition to excited state, and $\delta(S_{p,q}, 1)$ is
an indicator function equal to 1 if the neighbouring cell $(p,q)$ is
excited and 0 otherwise. In other words, at each time step, a cell
which is in a resting state becomes excited if the number of excited
neighbouring cells meets or exceeds the threshold of excitation
(excitation rule); a cell which is excited transitions to the maximal
refractory state (refractory rule); a cell in a refractory state
$S_{i,j}^{k-1} < 0$ increments by 1 each time step until returning to
the resting state (return-to-rest rule).  

To iterate the sequence, initial conditions $S^0_{i,j}$, along with
threshold for excitation values $n_{i,j}$, and maximal refractory
state values $R_{i,j}$ must be specified for each cell on the grid in
addition to the transition rules. This is done as described below. 

## Software usage and functionality 

### Predefined scenarios and code examples/tests

Users can choose from several scenarios with predefined initial
conditions, threshold for excitation values and maximal refractory
state values as follows.

- **Plane Wave:** Demonstrates a simple propagating wave.

- **Annihilation:** Demonstrates annihilation of excitation waves
upon collision. 

- **Spiral Wave:** Visualises a rotating wave pattern.

- **Pair of Spiral Waves:** Shows interaction between two rotating waves.

- **Defibrillation of a Spiral Wave:** Models the effect of an external stimulus on a spiral wave.

- **Reentry around an Obstacle:** Demonstrates the phenomenon of reentry, a key component in arrhythmias.

- **Chaos & Fibrillation:** Illustrates chaotic patterns, representing fibrillating states in cardiac tissue.

Each scenario emphasises a different aspect of excitation wave
dynamics. These predefined scenarios play the dual role of usage/test
examples. 

### Custom parameters

The script includes a command line input dialogue that allows 
users to specify parameter values for the threshold for excitation values
and maximal refractory states of the cells in all predefined scenarios
mentioned above. In this way, users can investigate on their own the
conditions leading to a specific outcome, search for intervention
strategies, and experiment more generally. 

Grid size, animation speed, number of time steps, color schemes and
other non-essential script parameters can be further configured within
the script.  

### Further modifications

Basic programming skills will suffice to implement other more
intricate behaviours. This can be done by setting initial
conditions, threshold for excitation values and maximal 
refractory state values within the script similarly to the predefined
scenarios. 

## Software installation

The code does not require installation. It comes as a plain text file
that can be invoked directly by

`$ python main_cawem.py`

from the shell command line. Alternatively, it can be opened and run within
any Python integrated development environment.


## Software dependences

- `NumPy`

- `Matplotlib`



## Community guidelines

Issues or problems with the software as well as requests for
modifications can be submitted via the `Github` repository of the code
by creating a pull request to include changes in the main branch.

# Acknowledgements
Support from the UK Engineering and Physical Sciences Research Council
[grant number EP/T017899/1] is gratefully acknowledged.


# References

References are provided in the accompanying `paper.bib` file. 


