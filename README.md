# RO-Optimization

# Worker scheduling problem

## Implementing linear programming  algorithm to solve the NP-hard worker scheduling problem. 


## General constraints and assumptions:

* Each day is divided into multiple shifts(usually 1-2).

* There are a number of required worker for each of the shift. 

* A worker is off on a specific day if no shift is assigned 

* The planning length is flexible (1-4 weeks, or more). 
    
* worker will only work at most one shift per day.

* A worker who works on a late nigth shift will take the next day off.

* Avoid 4 continuous day or afternoon shift. If any, assign 2 days off

* Avoid 3 continuous night shift. If any, assign 2 days off

* Avoid shift without at least one skilled member

* Avoid long blank

* Avoid pairs of concerns

* preserve weekend off duty at least one per months for each member

## Model:

* Essential idea is to introduce a binary variable x_ns in order to linearize the model

* Constraints and objective function can be represented as equality and inequality equations.

   x_ns = 0 when worker n will not work on shift s;   1 when worker n will work on shift s
      
* s: each shift

* n: each worker

* r: list storing the required worker in each day.

* daily_shift: [0, 1, 2, ...] in this case. The last element is late night shift.

* planning_length: planning_length is flexible. 

* Objective: minimize the numbers of scheduled worker after satisfying all constraints. 

* Implementing linear programming with pulp python package to find the solution of this constrained optimization problem. 


# ChangeLog
```
- V.1.0.0 : Release intiale
```

# Installations

- install more libs with'requirements.txt' in 'venv', lunch in command line : 
```
pip install -e .
```

## Utilisation

- run optimization in command line:
```
python3 -m src
```

## Result:

![Alt text](/data/worker_scheduling.png?raw=true "Optional Title")

* Horizontal: work shifts from week1 Monday to week4 Friday.
* Vertical: Worker_id
* orange: late night shift
* pink:  worker is working on that shift
* gray: worker is off work on that shift. 

## scheduling.py
A more general case in python file

## data
contain output figs of the scheduling

## utils
1. output the scheduling into csv
2. re

# Arborescence du projet

- classique :
    - [config](https://github.com/cheumeni-commit/URL-Classification/tree/main/config)
    - [data](https://github.com/cheumeni-commit/URL-Classification/tree/main/data)
    - [src](https://github.com/cheumeni-commit/URL-Classification/tree/main/src)


# Citing RO-Optimiszation

Si vous utilisez ce projet pour faire des travaux de recherche et pour résoudre d'autres problèmes, merci de me citer comme suit.

```BibTeX
@misc{jmc2022ML-RO-Optimiszation,
  author =       {Jean-Michel Cheumeni},
  title =        {RO-Optimiszation},
  howpublished = {\url{git@github.com:cheumeni-commit/RO-Optimization.git}},
  year =         {2022}
}
```