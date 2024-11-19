from flask import Flask,render_template,request
from DBHandler import DBHandler

app = Flask(__name__)

def addQuerySelector(string,data):
  querys = """
  <form method=post action=/institutions>
  <label for="region">"""
  querys += string

  querys += """</label>
  <select name="region">
  """

  for values in data:
    querys +="<option value=\""+str(values[0])+"\">"+str(values[1])+"</option>"
  querys += """
  </select>
       <input type=submit name=save value=Submeter>
  </form>
    """

  return querys

@app.post("/search")
def search():
  sqlCommand = request.form["sql"]
  handler = DBHandler.DBHandler()
  data = handler.queryForHTML(sqlCommand)
  return render_template('search.html',sql=data,sqlCommand=sqlCommand)

@app.post("/institutions")
@app.route("/institutions")
def institutions():
  institutionId = 1
  if(request.method == 'POST'):
    institutionId = request.form["region"]
  handler = DBHandler.DBHandler()
  sqlCommand = "SELECT * FROM institutions WHERE regionId ="
  sqlCommand += str(institutionId)

  data = handler.queryForHTML(sqlCommand)
  querys = addQuerySelector("Escolha uma região",handler.query("Select * FROM regions"))

  return render_template('search.html',sql=data,sqlCommand=sqlCommand,querys=querys)

@app.route("/")
def index():
  handler = DBHandler.DBHandler()
  stats = handler._cursor.execute('''
      SELECT * FROM
        (SELECT COUNT(*) numberAgeGroups FROM ageGroups)
      JOIN
        (SELECT COUNT(*) numberInstitutions FROM institutions)
      JOIN
        (SELECT COUNT(*) numberRegions FROM regions)
      JOIN
        (SELECT COUNT(*) numberDiagnostics FROM diagnosticGroups)
      JOIN
        (SELECT COUNT(*) numberPeriods FROM periods)
      JOIN
        (SELECT COUNT(*) numberHealthRegistries FROM healthRegistries)
                                  ''').fetchone()
 

  return render_template('index.html',stats=stats)


