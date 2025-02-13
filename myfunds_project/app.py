from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# ici je doit mettre mon chqrgement depui json
def load_funds():
    with open("funds.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return {fund["name"]: set(fund["stocks"]) for fund in data["funds"]}

# le calcule du recouvre;ent
def calculate_overlap(current_funds, new_fund, available_funds):
    if new_fund not in available_funds:
        return "FOND_NON_TROUVE"
    
    new_stocks = available_funds[new_fund]
    results = []
    
    for fund in current_funds:
        if fund in available_funds:
            existing_stocks = available_funds[fund]
            common_stocks = new_stocks.intersection(existing_stocks)
            total_stocks = len(new_stocks) + len(existing_stocks)
            overlap = (2 * len(common_stocks)) / total_stocks * 100 if total_stocks > 0 else 0
            results.append(f"{new_fund} - {fund} : {overlap:.2f}%")
    
    return results if results else "Aucun recouvrement trouvé."

# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# API pour le calcul
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.form
    current_funds = data.get("current_funds", "").split()
    new_fund = data.get("new_fund", "").strip()
    
    available_funds = load_funds()
    
    if not current_funds or not new_fund:
        return jsonify({"error": "Veuillez entrer des fonds valides."})
    
    result = calculate_overlap(current_funds, new_fund, available_funds)
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)