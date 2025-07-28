def makeLegalString(s):
 t = ''
 return solve(s, t)

def solve(charsToPlace, solution):
 print(solution, charsToPlace)
 if charsToPlace == '':
  return solution
 else:
  for i in range(len(charsToPlace)):
     if isLegal(solution, charsToPlace[0]):
       solution += charsToPlace[0]
       print('sol', solution, charsToPlace[1:])
       result = solve(charsToPlace[1:], solution)
       if result != None:
          return result
       remander = solution[-1]
       solution = solution[:-1]
       charsToPlace += remander
  return None
 
def isLegal(solution, c):
   if solution == '': return True
   else:
     return abs(ord(c) - ord(solution[-1])) > 1

 




def testMakeLegalString():
 # Your function only needs to return one of the strings in each of these sets
 assert(makeLegalString('abcd') in {'bdac', 'cadb'})
 assert(makeLegalString('cabs') in {'bsac', 'acsb', 'bsca', 'casb'})
 assert(makeLegalString('aah') in {'aah', 'aha', 'haa'})
 assert(makeLegalString('higgs') in {'hsigg', 'hsgig', 'gigsh',
 'ggish', 'iggsh', 'hsggi'})
 assert(makeLegalString('x') in {'x'})
 assert(makeLegalString('') in {''})
 # These tests have no valid result string and should return None
 assert(makeLegalString('abba') == None)
 assert(makeLegalString('xyzzy') == None)

testMakeLegalString()