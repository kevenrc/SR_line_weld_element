# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import os
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

class Inp2Analysis():

    def __init__(self, inp_filename):
        self.inp_filename = inp_filename
        self.model_name = os.path.splitext(os.path.basename(inp_filename))[0]

    def import_inp(self):
        mdb.ModelFromInputFile(name=self.model_name, inputFileName=self.inp_filename)

    def define_bcs(self, boundary_conditions):
        a = mdb.models[self.model_name].rootAssembly
        for bc in boundary_conditions:
            region = a.instances['PART-DEFAULT_1'].sets[bc[0]]
            mdb.models[self.model_name].DisplacementBC(name=bc[0],
                createStepName='DefaultSet', region=region, u1=bc[1], u2=bc[2], u3=bc[3],
                ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF,
                distributionType=UNIFORM, fieldName='', localCsys=None)

    def run_analysis(self, job_name, numCpus=4, numGPUs=0):
        mdb.Job(name=job_name, model=self.model_name, description='',
            type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
            memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=numCpus,
            numDomains=4, numGPUs=numGPUs)
        mdb.jobs[job_name].submit(consistencyChecking=OFF)

if __name__ == "__main__":

    inp_filename = os.path.join('C:/Users/Keven Carlson/Desktop/Sandia/cubit/standard_channel_L10_0.inp')
    # l-loading-positive
    boundary_conditions = [('NS1', 0.0, UNSET, UNSET), ('NS2', UNSET, 0.0, UNSET), ('NS5', UNSET, UNSET, 0.0),
        ('NS50', UNSET, UNSET, 0.0), ('NS4', 0.00118, UNSET, UNSET)]
    l_load_pos = Inp2Analysis(inp_filename)
    l_load_pos.import_inp()
    l_load_pos.define_bcs(boundary_conditions)
    l_load_pos.run_analysis('l-load-pos')

    # l-loading-negative
    boundary_conditions = [('NS1', 0.0, UNSET, UNSET), ('NS2', UNSET, 0.0, UNSET), ('NS5', UNSET, UNSET, 0.0),
        ('NS50', UNSET, UNSET, 0.0), ('NS4', 0.00118, UNSET, UNSET)]
    l_load_neg = Inp2Analysis(inp_filename)
    l_load_neg.import_inp()
    l_load_neg.define_bcs(boundary_conditions)
    l_load_neg.run_analysis('l-load-neg')
    # # r-loading
    # boundary_conditions = [('NS1', 0.0, UNSET, UNSET), ('NS2', UNSET, 0.0, UNSET), ('NS5', UNSET, UNSET, 0.0),
    #     ('NS50', UNSET, UNSET, 0.0), ('NS6', UNSET, UNSET, 0.1), ('NS60', UNSET, UNSET, 0.1)]
    # z_axial = Inp2Analysis(inp_filename)
    # z_axial.import_inp()
    # z_axial.define_bcs(boundary_conditions)
    # z_axial.run_analysis('r-load')
    #
    # # s-loading
    # boundary_conditions = [('NS1', 0.0, UNSET, UNSET), ('NS2', UNSET, 0.0, UNSET), ('NS5', UNSET, UNSET, 0.0),
    #     ('NS50', UNSET, UNSET, 0.0), ('NS3', 0.07992, UNSET, UNSET)]
    # s_load = Inp2Analysis(inp_filename)
    # s_load.import_inp()
    # s_load.define_bcs(boundary_conditions)
    # s_load.run_analysis('s-load')
    #
    # # t-loading
    # boundary_conditions = [('NS1', 0.0, UNSET, UNSET), ('NS2', UNSET, 0.0, UNSET), ('NS5', UNSET, UNSET, 0.0),
    #     ('NS50', UNSET, UNSET, 0.0), ('NS4', UNSET, 0.02, UNSET), ('NS40', UNSET, 0.02, UNSET)]
    # t_load = Inp2Analysis(inp_filename)
    # t_load.import_inp()
    # t_load.define_bcs(boundary_conditions)
    # t_load.run_analysis('t-load')
