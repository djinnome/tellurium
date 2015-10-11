import libsedml
import roadrunner

from roadrunner import RoadRunner

def openDoc(file):
  '''Opens a SED-ML file'''
  return SedMLDoc.fromFile(file)

# ** Results **

class SimulationResult(object):
  def __init__(self):
    pass

class RoadRunnerResult(SimulationResult):
  def __init__(self, result):
    self.result = result

  def __repr__(self):
    return repr(self.result)

  def __str__(self):
    return str(self.result)

# ** Runners **

class SedMLRunner(object):
  def __init__(self):
    pass

class SedMLRunnerRoadRunnerGillespie(SedMLRunner):
  def __init__(self, sim, model, selections):
    print('SedMLRunnerRoadRunnerGillespie model = {}'.format(model))
    self.rr = RoadRunner(model)
    self.start = sim.getOutputStartTime()
    self.end = sim.getOutputEndTime()
    self.n = sim.getNumberOfPoints()
    self.selections = selections

  def run(self):
    return RoadRunnerResult(self.rr.simulate(self.start, self.end, self.n, selections))

# ** Symbol resolver **

class SymbolResolver(object):
  def __init__(self, datagen):
    self.datagen = datagen

  def resolve(self, id):
    for i in range(0, self.datagen.getNumVariables()):
      var = self.datagen.getVariable(i)
      if var.getId() == id:
        return var.getName()

# ** SED-ML document **

class SedMLDoc(object):
  def __init__(self):
    self.doc = None
    self.runnerfac = {
    'KISAO:0000029': SedMLRunnerRoadRunnerGillespie
    }
    self.runners = []

  @classmethod
  def fromFile(cls, file):
    r = SedMLDoc()
    r.doc = libsedml.readSedML(file)
    if ( r.doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_ERROR) > 0):
      raise RuntimeError(r.doc.getErrorLog().toString())
    return r

  def run(self):
    return self.runAll()

  def getSimulation(self, id):
    for i in range(0, self.doc.getNumSimulations()):
      x = self.doc.getSimulation(i)
      if x.getId() == id:
        return x
    raise RuntimeError('No such simulation: {}'.format(id))

  def getModel(self, id):
    for i in range(0, self.doc.getNumModels()):
      x = self.doc.getModel(i)
      if x.getId() == id:
        return x
    raise RuntimeError('No such model: {}'.format(id))

  def getTask(self, id):
    for i in range(0, self.doc.getNumTasks()):
      x = self.doc.getTask(i)
      if x.getId() == id:
        return x
    raise RuntimeError('No such task: {}'.format(id))

  def makeRunner(self, kisao, sim, model, selections):
    r =  self.runnerfac[kisao](sim,model.getSource(), selections)
    return r

  def addRunner(self, task, selections):
    sim = self.getSimulation(task.getSimulationReference())
    model = self.getModel(task.getModelReference())
    if sim.getTypeCode() == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
      if sim.isSetAlgorithm():
        kisao = sim.getAlgorithm().getKisaoID()
        self.runners.append(self.makeRunner(kisao, sim, model, selections))

  def gatherSymbols(self):
    result = []
    for i in range(0, self.doc.getNumDataGenerators()):
      gen = self.doc.getDataGenerator(i)
      math = gen.getMath()

      resolver = SymbolResolver(gen)

      #print(dir(math))
      varid = math.getName()
      resolved_name = resolver.resolve(varid)
      #print('{} resolved to {}'.format(varid, resolved_name))
      result.append(resolved_name)
    return result

  def runAll(self):
    '''Runs all tasks'''
    # figure out selections
    selections = self.gatherSymbols()
    for i in range(0, self.doc.getNumTasks()):
      task = self.doc.getTask(i)
      self.addRunner(task, selections)
