"""
DataGenerator via formula
"""
from __future__ import print_function
import tellurium as te
import os

antimonyStr = '''
model case_05()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''

phrasedmlStr = '''
  mod1 = model "case_05"
  sim1 = simulate uniform(0, 10, 100)
  task1 = run sim1 on mod1
  plot "Example plot" task1.time vs task1.S1, task1.S2, task1.S1/task1.S2
  report task1.time vs task1.S1, task1.S2, task1.S1/task1.S2
  plot "Normalized plot" task1.S1/max(task1.S1) vs task1.S2/max(task1.S2)
  report task1.S1/max(task1.S1) vs task1.S2/max(task1.S2)
'''

# phrasedml experiment
exp = te.experiment(antimonyStr, phrasedmlStr)

# write python code
realPath = os.path.realpath(__file__)
workingDir = os.path.dirname(realPath)
with open(realPath + 'code.py', 'w') as f:
    f.write(exp._toPython(phrasedmlStr, workingDir=workingDir))

# execute python
exp.execute(phrasedmlStr, workingDir=workingDir)

# remove sedx (not hashable due to timestamp)
os.remove(os.path.join(workingDir, 'case_05.sedx'))
