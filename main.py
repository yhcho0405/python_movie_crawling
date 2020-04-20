from flask import Flask, render_template, request, redirect
from scrapper import setting

app = Flask("scrapper")

db = {}

@app.route("/")
def home():
  return render_template("main.html")

@app.route("/report")
def report():
  try:
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    page = int(request.args.get('page'))
  except:
    print("input type error")
    return redirect("/")

  if (start or end or page):
    if(start < 1 or end < start or page < 0 or page > 10):
      print("condition error")
      return redirect("/")
    else:
      movies = setting(start, end, page)
  else:
    print("None vallue error")
    return redirect("/")

  end = movies[-1].get('rank')

  if(start == 1):
    rstart = "1st"
  elif(start == 2):
    rstart = "2nd"
  else:
    rstart = f"{start}th"
      
  if(end == 1):
    rend = "1st"
  elif(end == 2):
    rend = "2nd"
  else:
    rend = f"{end}th"

  return render_template("report.html", start=rstart, end=rend, page=page, movies = movies)


app.run()