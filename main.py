
# 5. FLASK APP EXAMPLE
from flowService import SubscriptionService
from webhookHandler import WebhookHandler
from flask import Flask, request, jsonify

app = Flask(__name__)
subscription_service = SubscriptionService()
webhook_handler = WebhookHandler()

@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    customer_data = request.json
    result = subscription_service.setup_monthly_subscription(customer_data)
    return jsonify(result)

@app.route('/pause-subscription', methods=['POST'])
def pause_subscription():
    data = request.json
    result = subscription_service.handle_subscription_pause_resume(
        data['subscription_id'], 'PAUSE'
    )
    return jsonify(result)

@app.route('/resume-subscription', methods=['POST'])
def resume_subscription():
    data = request.json
    result = subscription_service.handle_subscription_pause_resume(
        data['subscription_id'], 'RESUME'
    )
    return jsonify(result)

@app.route('/manual-charge', methods=['POST'])
def manual_charge():
    data = request.json
    result = subscription_service.manual_charge_subscription(
        data['sub_reference_id'], 
        data['amount'], 
        data.get('reason', 'Manual charge')
    )
    return jsonify(result)

@app.route('/webhook', methods=['POST'])
def webhook():
    webhook_data = request.json
    result = webhook_handler.handle_webhook(webhook_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
