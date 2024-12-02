def sortAndGetCorrectIdForQuery(query,index):
      sortedQuery = sorted(query,key=lambda x:int(x[1].split(" ")[0]))
      i = 1
      for query in sortedQuery:
        if(query[0] == int(index)): break
        i+=1
      return sortedQuery,i

def addSubmit(endpoint,queryList):
  querys = """
  <form method =post action=/"""
  querys += endpoint + '>'

  for query in queryList:
    querys += query +'\n'

  querys += "<input class=\"submit-button\" type=submit name=save value=Submit>" + "</form>"

  return querys

def addQuerySelector(label,data,id):
  querys = "<div class=\"custom-select\"><label for=\""
  querys += label + "\">""""</label>
  <select name="""
  querys +=  '"' +label + "\" id =\"" + label + "\">"


  selected : int = int(id) - 1

  info = None
  querys +="<option value=\"0\">NULL</option>"
  
  for values in data:
    if(selected == 0):
      info = values[1]
      querys +="<option value=\""+str(values[0])+"\" selected>"+str(values[1])+"</option>"
    
    else: 
      querys +="<option value=\""+str(values[0])+"\">"+str(values[1])+"</option>"

    selected -= 1    
  querys += """
  </select></div>
    """

  return querys,info