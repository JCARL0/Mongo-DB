from flask import Flask, render_template, request
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", neighborhoods=db.get_neighborhood_list())

@app.route("/result", methods=["POST"])
def result():
    data = request.form
    neighborhood, date = data["neighborhood"], int(data["date"])
    results = db.search_results(neighborhood, date)

    if results:
        stats = db.calculate_statistics(results)
        image_path = db.generate_chart(stats, neighborhood)
        return render_template("result.html", parameters={"neighborhood": neighborhood, "date": date}, results=results, stats=stats, image_path=image_path)
    else:
        return render_template("index.html", neighborhoods=db.get_neighborhood_list(), error_message="No results found, please try again with different data")

app.run(host='localhost', port=5069, debug=True)
