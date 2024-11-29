from flask import Flask,render_template,request
from DBHandler import DBHandler
from Website.util import addSubmit,addQuerySelector

app = Flask(__name__)

@app.post("/search")
def search():
  sqlCommand = request.form["sql"]
  handler = DBHandler.DBHandler()
  data = handler.queryForHTML(sqlCommand)
  return render_template('search.html',sql=data)

@app.post("/institutions")
@app.route("/institutions")
def institutions():
  institutionId = 1
  if(request.method == 'POST'):
    institutionId = request.form["region"]
  handler = DBHandler.DBHandler()

  sqlCommand = "SELECT institutions.name as Institution,regions.name as Region FROM institutions inner join regions on institutions.regionId = regions.id WHERE regionId ="
  sqlCommand += str(institutionId)


  data = handler.queryForHTML(sqlCommand)
  query,info = addQuerySelector("region",handler.query("Select * FROM regions"),institutionId)
  queryList = [query]
  querys = addSubmit("institutions",queryList)

  info = "Institutions in the Region of: " + info

  return render_template('search.html',sql=data,querys=querys,info=info)

@app.post("/diagnosticsByInstitution")
@app.route("/diagnosticsByInstitution")
def diagnosticsByInstitution():
  institutionId = 1
  month = 1
  year = 2020
  if(request.method == 'POST'):
    institutionId = request.form["institution"]
    month = request.form["month"]
    year = request.form["year"] 

  handler = DBHandler.DBHandler()
  sqlCommand = "SELECT d.description as Description,a.minimumAge,a.maximumAge,i.name as Institution,r.name as Region,p.month as Month,p.year as Year,hR.gender as Gender,hR.hospitalizations as Hospitalizations,hR.daysOfHospitalization as 'Days of Hospitalization',hR.outpatient as Outpatient,hR.deaths as Deaths FROM healthRegistries hR inner join institutions i on hR.institutionId = i.id inner join periods p on hR.periodId = p.id inner join regions r on i.regionId = r.id inner join diagnosticGroups d on hR.diagnosticGroupId = d.id inner join ageGroups a on hR.ageGroupId = a.id WHERE p.month ="
  sqlCommand += str(month) + " and p.year=" + str(year) + " and i.id=" + str(institutionId) + " ORDER BY d.code,a.minimumAge desc,hR.gender desc"

  data = handler.queryForHTML(sqlCommand)
  query,institutions = addQuerySelector("institution",handler.query("Select i.id,i.name FROM institutions i"),institutionId)
  queryList = [query]

  query,_ = addQuerySelector("month",handler.query("Select p.month,p.month FROM periods p Group by p.month"),month)
  queryList.append(query)
  query,_ = addQuerySelector("year",handler.query("Select p.year,p.year FROM periods p Group by p.year"),int(year)-2015)
  queryList.append(query)


  querys = addSubmit("diagnosticsByInstitution",queryList)
  info = "Diagnostics of the Institution: " + institutions + ", in the date of: " + str(month) + '-' + str(year)

  return render_template('search.html',sql=data,querys=querys,info=info)

@app.route("/institutionsByDeaths")
def institutionsByDeaths():
  handler = DBHandler.DBHandler()

  sqlCommand = """
  select i.name as Institution, r.name as Region, sum(hr.deaths) as 'Total Deaths'
  from institutions i join regions r on i.regionId = r.id
  join healthRegistries hr on hr.institutionId = i.id
  group by i.name, r.name
  order by sum(hr.deaths) desc;
  """

  data = handler.queryForHTML(sqlCommand)

  info = "Institutions Ordered by Total Deaths"

  return render_template('search.html',sql=data,info=info)

@app.route("/regionsByDeaths")
def regionsByDeath():
  handler = DBHandler.DBHandler()

  sqlCommand = """
  select r.name, sum(hr.deaths) as 'TotalDeaths'
  from institutions i join regions r on i.regionId = r.id
  join healthRegistries hr on hr.institutionId = i.id
  group by r.name
  order by sum(hr.deaths) desc;
  """

  data = handler.queryForHTML(sqlCommand)

  info = "Regions Ordered by Total Deaths"

  return render_template('search.html',sql=data,info=info)


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


