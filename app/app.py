from flask import Flask, render_template, request, send_file, jsonify
import csv,io
from crawl import crawling, crawled_data  # Import your crawler function


app = Flask(__name__)

session={}
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route("/download")
def download_csv():
    items = crawled_data

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
    
    session['crawled_items'] = items
    # print(items)
    # print(jsonify(items))
    return jsonify(items)


@app.route("/all-items")
def all_items():
    
    return render_template("all_items.html")

@app.route('/get-crawled-items', methods=['GET'])
def get_crawled_items():
    items = session.get('crawled_items', [])
    filtered_items = []

    for item in items:
        try:
            if item['image_url'] != 'https://minecraft.wikiNo image found':
                filtered_items.append(item)
        except KeyError:
            # Handle the case where 'image_url' is missing
            print(f"Item missing 'image_url': {item}")  # Optional: Log the item for debugging

    return jsonify(filtered_items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


# test

