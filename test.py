from interfaces.base import BaseApp
from models.sis import SIS
import unittest


class TestModule(unittest.TestCase):

    def testOverwriteConfiguration(self):
        base = BaseApp()
        base.mainloop()
        base.addDefaultSISConfiguration()
        defaultConfiguration = SIS("IoT-SIS: Default Configuration", 1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8,
                                   50, 0.75, 864000, 0.5, 12, False)
        base.overwriteConfiguration(-1, defaultConfiguration)
        errorMessage = "This configuration is not present in the configuration list for the base application."
        self.assertTrue(base.configurations[-1] == defaultConfiguration, errorMessage)

    def testRemoveConfiguration(self):
        base = BaseApp()
        base.mainloop()
        originalLength = len(base.configurations)
        base.removeConfiguration(-1)
        newLength = len(base.configurations)
        errorMessage = "The configurations list are the same length."
        self.assertFalse(originalLength == newLength, errorMessage)

    def testAddDefaultConfiguration(self):
        base = BaseApp()
        base.mainloop()
        originalLength = len(base.configurations)
        base.addDefaultSISConfiguration()
        newLength = len(base.configurations)
        errorMessage = "The configurations list are the same length."
        self.assertFalse(originalLength == newLength, errorMessage)

    def testAddConfiguration(self):
        base = BaseApp()
        base.mainloop()
        originalLength = len(base.configurations)
        newConfiguration = SIS("IoT-SIS: New Configuration", 1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8,
                               50, 0.75, 864000, 0.5, 12, True)
        base.addConfiguration(newConfiguration)
        newLength = len(base.configurations)
        errorMessage = "The configurations list are the same length."
        self.assertFalse(originalLength == newLength, errorMessage)

    def testNewActiveConfiguration(self):
        base = BaseApp()
        base.mainloop()
        originalActiveConfiguration = base.activeConfiguration
        base.setActiveConfiguration(2)
        newActiveConfiguration = base.activeConfiguration
        errorMessage = "The configurations are the same."
        self.assertFalse(originalActiveConfiguration == newActiveConfiguration, errorMessage)

    def testCheckValid(self):
        base = BaseApp()
        base.mainloop()
        errorMessage = "The configuration is valid."
        self.assertTrue(base.interfaces["SISControlInterface"].checkValid(base.configurations[6]) == False, errorMessage)

    def testScore(self):
        configuration = SIS("IoT-SIS: New Configuration", 1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8,
                               50, 0.75, 864000, 0.5, 12, True)
        configuration.runSimulation()
        results = configuration.calculateScores()
        errorMessage = "The calculateScores function has not returned 24 values."
        self.assertTrue(len(results) == 24, errorMessage)

    def testRunSimulation(self):
        configuration = SIS("IoT-SIS: New Configuration", 1000, 1, 10, 50, 10, 10, 27, 0.01, 0.02, 0.1, 0.8,
                               50, 0.75, 864000, 0.5, 12, True)
        results = configuration.runSimulation()
        errorMessage = "The runSimulation function has not returned 4 values."
        self.assertTrue(len(results) == 4, errorMessage)