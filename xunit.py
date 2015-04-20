import traceback

class TestCase:
	def __init__(self, name):
		self.name = name
		
	def setUp(self):
		pass
		
	def run(self, result):
		result.testStarted()
		try:
			self.setUp()
			method = getattr(self, self.name)
			method()
		except Exception as e:
			result.testFailed(self.name, traceback.format_exc())
		finally:
			self.tearDown()

	def tearDown(self):
		pass
		
class WasRun(TestCase):
	def __init__(self, name):
		TestCase.__init__(self, name)
		
	def setUp(self):
		self.log = "setUp "
		
	def testMethod(self):
		self.log = self.log + "testMethod "

	def testBrokenMethod(self):
		raise Exception

	def tearDown(self):
		self.log = self.log + "tearDown "
		
class ExceptionInSetup(TestCase):
	def __init__(self, name):
		TestCase.__init__(self, name)
		
	def setUp(self):
		raise Exception()
		
	def testMethod(self):
		pass

	def tearDown(self):
		pass
		
class TestResult:
	def __init__(self):
		self.runCount = 0
		self.errorCount = 0
		self.failedTests = {}
		
	def testStarted(self):
		self.runCount = self.runCount + 1
		
	def testFailed(self, name, error):
		self.errorCount = self.errorCount + 1
		self.failedTests[name] = error
		
	def summary(self):
		summary = "%d run, %d failed" % (self.runCount, self.errorCount)
		for name in self.failedTests.keys():
			summary += "\n" + "-"*60
			summary += "\n%s\n%s" % (name, self.failedTests[name]) 
			summary += "\n" + "-"*60
		return summary
		
class TestSuite:
	def __init__(self):
		self.tests = []
		
	def add(self, test):
		self.tests.append(test)
		
	def run(self, result):
		for test in self.tests:
			test.run(result)
		
class TestCaseTest(TestCase):
	def setUp(self):		
		self.result = TestResult()

	def testTemplateMethod(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("setUp testMethod tearDown " == test.log)
		
	def testResult(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("1 run, 0 failed" == self.result.summary())
	
	def testFailedResult(self):
		test = WasRun("testBrokenMethod")
		test.run(self.result)
		assert(self.result.summary().startswith("1 run, 1 failed"))
	
	def testFailedResultFormatting(self):
		result = TestResult()
		result.testStarted()
		result.testFailed("failed", "message")
		assert(result.summary().startswith("1 run, 1 failed"))
	
	def testFailedInSetupResult(self):
		test = ExceptionInSetup("testMethod")
		test.run(self.result)
		assert(self.result.summary().startswith("1 run, 1 failed"))
		
	def testFailedCallsTearDown(self):
		test = WasRun("testBrokenMethod")
		test.run(self.result)
		assert("setUp tearDown " == test.log)
		
	def testSuite(self):
		suite = TestSuite()
		suite.add(WasRun("testMethod"))
		suite.add(WasRun("testBrokenMethod"))
		suite.run(self.result)
		assert(self.result.summary().startswith("2 run, 1 failed"))
		
suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testFailedInSetupResult"))
suite.add(TestCaseTest("testFailedCallsTearDown"))
suite.add(TestCaseTest("testSuite"))
result = TestResult()
suite.run(result)
print(result.summary())