from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static-visualizations')
def static_visualizations():
    return render_template('static_visualizations.html')

@app.route('/dynamic-visualizations')
def dynamic_visualizations():
    return render_template('dynamic_visualizations.html')

if __name__ == "__main__":
    app.run(debug=True)