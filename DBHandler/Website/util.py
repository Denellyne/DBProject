def addSubmit(endpoint,queryList):
  querys = """
  <form method =post action=/"""
  querys += endpoint + '>'

  for query in queryList:
    querys += query +'\n'

  querys += "<input type=submit name=save value=Submit>" + "</form>"

  return querys

def addQuerySelector(label,string,data,id):
  querys = "<label for=\""
  querys += label + "\">" + string + """</label>
  <select name="""
  querys +=  '"' +label + "\" id =\"" + label + "\">"

  selected : int = int(id) - 1

  info = None

  for values in data:
    if(selected == 0):
      info = values[1]
      querys +="<option value=\""+str(values[0])+"\" selected>"+str(values[1])+"</option>"
    
    else: 
      querys +="<option value=\""+str(values[0])+"\">"+str(values[1])+"</option>"

    selected -= 1    
  querys += """
  </select><br>
    """

  return querys,info