
# 4. WEBHOOK HANDLER
from flowService import SubscriptionService
class WebhookHandler:
    def __init__(self):
        self.subscription_service = SubscriptionService()

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle various subscription webhooks"""
        
        event_type = webhook_data.get("type")
        
        if event_type == "SUBSCRIPTION_PAYMENT_FAILED":
            # Handle failed payment
            sub_reference_id = webhook_data.get("data", {}).get("subReferenceId")
            
            # Automatically retry failed payment
            retry_result = self.subscription_service.handle_failed_payment_retry(sub_reference_id)
            
            return {
                "event": "payment_failed_handled",
                "retry_result": retry_result
            }
        
        elif event_type == "SUBSCRIPTION_PAYMENT_SUCCESS":
            # Handle successful payment
            return {
                "event": "payment_success",
                "message": "Payment processed successfully"
            }
        
        elif event_type == "SUBSCRIPTION_ACTIVATED":
            # Handle subscription activation
            return {
                "event": "subscription_activated",
                "message": "Subscription is now active"
            }
        
        return {"event": "unhandled", "type": event_type}
