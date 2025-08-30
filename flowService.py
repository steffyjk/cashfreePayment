#  Complete Implementation with All Scenarios
from cashfreeService import CashfreeSubscriptionManager
class SubscriptionService:
    def __init__(self):
        self.cf_manager = CashfreeSubscriptionManager()

    def setup_monthly_subscription(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete setup for monthly subscription"""
        
        # Step 1: Create Plan
        plan_data = {
            "planId": f"monthly_plan_{int(datetime.now().timestamp())}",
            "planName": "Monthly Subscription Plan",
            "type": "PERIODIC",
            "recurringAmount": customer_data["monthly_amount"],
            "maxAmount": customer_data["monthly_amount"] * 2,  # Allow some flexibility
            "intervals": 1,
            "intervalType": "month"
        }
        
        plan_response = self.cf_manager.create_plan(plan_data)
            
        if plan_response.get("status") != 200:
            return {"error": "Failed to create plan", "details": plan_response}

        # Step 2: Create Subscription
        subscription_data = {
            "subscriptionId": f"sub_{customer_data['customer_id']}_{int(datetime.now().timestamp())}",
            "customerName": customer_data["name"],
            "customerPhone": customer_data["phone"],
            "customerEmail": customer_data["email"],
            "returnUrl": customer_data.get("return_url", "https://yourapp.com/success"),
            "authAmount": customer_data["monthly_amount"],
            "expiresOn": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S"),
            "planId": plan_data["planId"],
            "notificationChannels": ["EMAIL", "SMS"]
        }
        
        subscription_response = self.cf_manager.create_subscription(subscription_data)
        
        return {
            "plan": plan_response,
            "subscription": subscription_response,
            "auth_link": subscription_response.get("data", {}).get("authLink"),
            "sub_reference_id": subscription_response.get("data", {}).get("subReferenceId")
        }

    def handle_failed_payment_retry(self, sub_reference_id: int, max_retries: int = 3) -> Dict[str, Any]:
        """Handle failed payment with retry logic"""
        
        retry_results = []
        
        for attempt in range(1, max_retries + 1):
            print(f"Retry attempt {attempt} for subscription {sub_reference_id}")
            
            # Calculate next retry date (next day)
            next_retry_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            retry_data = {
                "nextScheduledOn": next_retry_date
            }
            
            result = self.cf_manager.retry_subscription_charge(sub_reference_id, retry_data)
            retry_results.append({
                "attempt": attempt,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            # If successful, break
            if result.get("status") == 200:
                break
                
            # Wait before next retry (in production, implement proper scheduling)
            import time
            time.sleep(60)  # Wait 1 minute between retries
        
        return {
            "sub_reference_id": sub_reference_id,
            "retry_attempts": retry_results,
            "final_status": "success" if retry_results[-1]["result"].get("status") == 200 else "failed"
        }

    def handle_subscription_pause_resume(self, subscription_id: str, action: str) -> Dict[str, Any]:
        """Handle subscription pause and resume scenarios"""
        
        if action == "PAUSE":
            # Pause subscription
            result = self.cf_manager.manage_subscription(subscription_id, "PAUSE")
            return {
                "action": "paused",
                "subscription_id": subscription_id,
                "result": result,
                "message": "Subscription paused. No charges will occur until resumed."
            }
        
        elif action == "RESUME":
            # Calculate next charge date for next cycle
            next_charge_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Get sub_reference_id (you'd store this when creating subscription)
            sub_reference_id = self.get_sub_reference_id(subscription_id)
            
            result = self.cf_manager.activate_subscription(sub_reference_id, next_charge_date)
            return {
                "action": "resumed",
                "subscription_id": subscription_id,
                "next_charge_date": next_charge_date,
                "result": result,
                "message": f"Subscription resumed. Next charge on {next_charge_date}. Missed period is skipped."
            }

    def manual_charge_subscription(self, sub_reference_id: int, amount: float, reason: str = "Manual charge") -> Dict[str, Any]:
        """Manually charge a subscription (for missed payments or on-demand)"""
        
        charge_data = {
            "amount": amount,
            "scheduledOn": datetime.now().strftime("%Y-%m-%d"),
            "remarks": reason,
            "merchantTxnId": f"manual_charge_{int(datetime.now().timestamp())}"
        }
        
        result = self.cf_manager.charge_subscription(sub_reference_id, charge_data)
        
        return {
            "sub_reference_id": sub_reference_id,
            "charge_amount": amount,
            "charge_result": result,
            "timestamp": datetime.now().isoformat()
        }

    def get_sub_reference_id(self, subscription_id: str) -> int:
        """Get sub_reference_id from subscription_id (implement based on your storage)"""
        # This should query your database to get sub_reference_id
        # For demo purposes, returning a dummy value
        return 123456
