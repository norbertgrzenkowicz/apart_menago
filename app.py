from flask import Flask, render_template
import pandas as pd
import src.interface
app = Flask(__name__)

scrapper = src.interface.Interface()
scrapper.scrap_data()
combined_df = pd.concat(scrapper.scrapped_data, ignore_index=True)
@app.route('/')
def index():
    # Convert DataFrame to HTML
    table_html = combined_df.to_html(classes='data', header="true", index=False)
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run(debug=True)
