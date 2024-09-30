import csv
import io, jsonify

from crawl import crawling  # Import your crawler function
from flask import Flask, render_template, request, send_file


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download")
def download_csv():
    items = crawling()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Item Name"])
    for item in items:
        writer.writerow([item["name"]])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        download_name="items.csv",
        as_attachment=True,
    )


@app.route('/start-crawl', methods=['POST'])
def start_crawl():
    items = crawling()
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
