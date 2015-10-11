import libsedml
import roadrunner

from roadrunner import RoadRunner

def openDoc(file):
  '''Opens a SED-ML file'''
  return SedMLDoc.fromFile(file)

class SedMLRunner(object):
  def __init__(self):
    pass

class SedMLDoc(object):
  def __init__(self):
    self.doc = None

  @classmethod
  def fromFile(cls, file):
    r = SedMLDoc()
    r.doc = libsedml.readSedML(file)
    if ( r.doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_ERROR) > 0):
      raise RuntimeError(r.doc.getErrorLog().toString())
    return r

  def run(self):
    return self.runAll()

  def runAll(self):
    for i in range(0, self.doc.getNumSimulations()):
      current = self.doc.getSimulation(i)
      if (current.getTypeCode() == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE):
        tc = current;
        kisaoid="none"
        if tc.isSetAlgorithm():
		  kisaoid=tc.getAlgorithm().getKisaoID()
        print "Timecourse id=", tc.getId()," start=",tc.getOutputStartTime()," end=",tc.getOutputEndTime()," numPoints=",tc.getNumberOfPoints()," kisao=",kisaoid,"\n";
      else:
	    print "Encountered unknown simulation. ",current.getId(),"\n";
