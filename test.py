import coverage
cov = coverage.coverage()
cov.start()

def CodeUnderTest():
  print 'do stuff'
  return True

assert CodeUnderTest()

cov.stop()
cov.save()
cov.report()