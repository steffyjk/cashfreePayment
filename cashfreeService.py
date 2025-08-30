# 2. Core Subscription Manager Class
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class CashfreeSubscriptionManager:
    def __init__(self):
        self.client_id = os.getenv('CASHFREE_CLIENT_ID')
        self.client_secret = os.getenv('CASHFREE_CLIENT_SECRET')
        self.base_url = os.getenv('CASHFREE_BASE_URL')
        self.headers = {
            'X-Client-Id': self.client_id,
            'X-Client-Secret': self.client_secret,
            'Content-Type': 'application/json'
        }

    # 1. CREATE SUBSCRIPTION PLAN
    def create_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a subscription plan"""
        url = f"{self.base_url}/api/v2/subscription-plans"
        response = requests.post(url, json=plan_data, headers=self.headers)
        return response.json()

    # 2. CREATE SUBSCRIPTION
    def create_subscription(self, subscription_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a subscription"""
        url = f"{self.base_url}/api/v2/subscriptions/nonSeamless/subscription"
        response = requests.post(url, json=subscription_data, headers=self.headers)
        return response.json()

    # 3. CHARGE SUBSCRIPTION (Manual)
    def charge_subscription(self, sub_reference_id: int, charge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manually charge a subscription"""
        url = f"{self.base_url}/api/v2/subscriptions/{sub_reference_id}/charge"
        response = requests.post(url, json=charge_data, headers=self.headers)
        return response.json()

    # 4. RETRY FAILED PAYMENT
    def retry_subscription_charge(self, sub_reference_id: int, retry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retry failed subscription payment"""
        url = f"{self.base_url}/api/v2/subscriptions/{sub_reference_id}/charge-retry"
        response = requests.post(url, json=retry_data, headers=self.headers)
        return response.json()

    # 5. ACTIVATE/RESUME PAUSED SUBSCRIPTION
    def activate_subscription(self, sub_reference_id: int, next_charge_date: str) -> Dict[str, Any]:
        """Activate/Resume a paused subscription"""
        url = f"{self.base_url}/api/v2/subscriptions/{sub_reference_id}/activate"
        data = {"nextScheduledOn": next_charge_date}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    # 6. MANAGE SUBSCRIPTION (Pause/Cancel/Change Plan)
    def manage_subscription(self, subscription_id: str, action: str, **kwargs) -> Dict[str, Any]:
        """Manage subscription - pause, cancel, activate, change plan"""
        url = f"{self.base_url}/subscriptions/{subscription_id}/manage"
        
        data = {"action": action}
        if action == "CHANGE_PLAN" and "plan_id" in kwargs:
            data["plan_id"] = kwargs["plan_id"]
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
