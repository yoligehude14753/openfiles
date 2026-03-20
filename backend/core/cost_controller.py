from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.core.database import CostTracking
from src.core.config import settings

class CostController:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.daily_budget = settings.daily_budget_usd
        self.monthly_budget = settings.monthly_budget_usd

    def get_daily_cost(self) -> float:
        """Get total cost for today."""
        today = datetime.utcnow().date()
        cost = self.db_session.query(func.sum(CostTracking.cost_usd)).filter(
            func.date(CostTracking.date) == today
        ).scalar()
        return cost or 0.0

    def get_monthly_cost(self) -> float:
        """Get total cost for current month."""
        now = datetime.utcnow()
        month_start = datetime(now.year, now.month, 1)
        cost = self.db_session.query(func.sum(CostTracking.cost_usd)).filter(
            CostTracking.date >= month_start
        ).scalar()
        return cost or 0.0

    def can_process(self) -> tuple[bool, str]:
        """Check if we can process more files within budget."""
        daily_cost = self.get_daily_cost()
        monthly_cost = self.get_monthly_cost()

        if daily_cost >= self.daily_budget:
            return False, f"Daily budget exceeded: ${daily_cost:.2f} / ${self.daily_budget:.2f}"

        if monthly_cost >= self.monthly_budget:
            return False, f"Monthly budget exceeded: ${monthly_cost:.2f} / ${self.monthly_budget:.2f}"

        return True, "OK"

    def get_budget_status(self) -> dict:
        """Get current budget status."""
        daily_cost = self.get_daily_cost()
        monthly_cost = self.get_monthly_cost()

        return {
            'daily_cost': daily_cost,
            'daily_budget': self.daily_budget,
            'daily_remaining': max(0, self.daily_budget - daily_cost),
            'daily_percent': (daily_cost / self.daily_budget * 100) if self.daily_budget > 0 else 0,
            'monthly_cost': monthly_cost,
            'monthly_budget': self.monthly_budget,
            'monthly_remaining': max(0, self.monthly_budget - monthly_cost),
            'monthly_percent': (monthly_cost / self.monthly_budget * 100) if self.monthly_budget > 0 else 0,
        }
