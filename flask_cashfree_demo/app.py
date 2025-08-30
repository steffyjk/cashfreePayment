from flask import Flask, request, jsonify
import requests
import config
import uuid

app = Flask(__name__)

headers = {
    "x-client-id": config.CASHFREE_APP_ID,
    "x-client-secret": config.CASHFREE_SECRET_KEY,
    "x-api-version": "2023-08-01",   # Update if docs mention a newer version
    "Content-Type": "application/json"
}

# ---------------------------
# Create Plan API
# ---------------------------
@app.route("/create-plan", methods=["POST"])
def create_plan():
    data = request.json
    body = {
        "plan_id": data.get("plan_id", f"plan_{uuid.uuid4().hex[:8]}"),
        "plan_name": data.get("plan_name", "Loan EMI Plan"),
        "plan_type": data.get("plan_type", "PERIODIC"),
        "plan_currency": data.get("plan_currency", "INR"),
        "plan_recurring_amount": data.get("plan_recurring_amount", 5000),
        "plan_max_amount": data.get("plan_max_amount", 5000),
        "plan_max_cycles": data.get("plan_max_cycles", 12),
        "plan_intervals": data.get("plan_intervals", 1),
        "plan_interval_type": data.get("plan_interval_type", "MONTH"),
        "plan_note": data.get("plan_note", "Loan EMI Plan")
    }

    url = f"{config.CASHFREE_BASE_URL}/plans"
    response = requests.post(url, headers=headers, json=body)
    return jsonify(response.json()), response.status_code


# ---------------------------
# Create Subscription API
# ---------------------------
@app.route("/create-subscription", methods=["POST"])
def create_subscription():
    data = request.json
    body = {
        "subscription_id": data.get("subscription_id", f"sub_{uuid.uuid4().hex[:8]}"),
        "plan_id": data["plan_id"],
        "subscription_name": data.get("subscription_name", "Loan Subscription"),
        "subscription_amount": data.get("subscription_amount", 5000),
        "subscription_currency": data.get("subscription_currency", "INR"),
        "customer_details": {
            "customer_id": data["customer_id"],
            "customer_email": data.get("customer_email", "test@example.com"),
            "customer_phone": data.get("customer_phone", "9999999999")
        },
        "first_charge_amount": data.get("first_charge_amount", 5000),
        "return_url": "https://yourdomain.com/subscription/callback"
    }

    url = f"{config.CASHFREE_BASE_URL}/subscriptions"
    response = requests.post(url, headers=headers, json=body)
    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(debug=True)
