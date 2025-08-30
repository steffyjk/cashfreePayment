# Usage Examples
from flowService import SubscriptionService
# Example usage
if __name__ == "__main__":
    service = SubscriptionService()
    
    # Create subscription
    customer = {
        "customer_id": "CUST001",
        "name": "John Doe",
        "phone": "9999999999",
        "email": "john@example.com",
        "monthly_amount": 500,
        "return_url": "https://yourapp.com/success"
    }
    
    # Setup subscription
    result = service.setup_monthly_subscription(customer)
    print("Subscription created:", result)
    
    # Handle failed payment retry
    retry_result = service.handle_failed_payment_retry(123456)
    print("Retry result:", retry_result)
    
    # Pause and resume
    pause_result = service.handle_subscription_pause_resume("sub_123", "PAUSE")
    resume_result = service.handle_subscription_pause_resume("sub_123", "RESUME")