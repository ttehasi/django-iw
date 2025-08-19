import pytest
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from models.models import Campaign
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestCampaignCreatedFilters:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.url = "/api/v1/agency/campaigns/"
        
        # Создаем aware-даты с временной зоной
        now = make_aware(datetime.now())
        self.today = now.date()
        self.yesterday = (now - timedelta(days=1)).date()
        self.tomorrow = (now + timedelta(days=1)).date()
        
        # Создаем тестовые кампании с aware-датами
        self.campaign_today = Campaign.objects.create(
            name="Today Campaign",
        )
        # self.campaign_today.created_at = self.today
        Campaign.objects.filter(id=self.campaign_today.id).update(
            created_at=self.today)
        
        self.campaign_yesterday = Campaign.objects.create(
            name="Yesterday Campaign",
        )
        # self.campaign_yesterday.created_at = self.yesterday
        Campaign.objects.filter(id=self.campaign_yesterday.id).update(
            created_at=self.yesterday)
        
        self.campaign_tomorrow = Campaign.objects.create(
            name="Tomorrow Campaign",
        )
        # self.campaign_tomorrow.created_at = self.tomorrow
        Campaign.objects.filter(id=self.campaign_tomorrow.id).update(
            created_at=self.tomorrow)

    def test_filter_created_after(self):
        response = self.client.get(
            self.url,
            {"created_after": self.today},
            format="json"
        )
        assert response.status_code == 200
        data = response.json()
        
        assert data['results'][0]["id"] == self.campaign_today.id
        assert data['results'][1]["id"] == self.campaign_tomorrow.id

    def test_filter_created_before(self):
        response = self.client.get(
            self.url,
            {"created_before": self.today.isoformat()},
            format="json"
        )
        
        assert response.status_code == 200
        data = response.json()
            
        assert data['results'][0]["id"] == self.campaign_today.id    
        assert data['results'][1]["id"] == self.campaign_yesterday.id

    def test_filter_combined_date_range(self):
        response = self.client.get(
            self.url,
            {
                "created_after": self.yesterday,
                "created_before": self.today
            },
            format="json"
        )
        
        assert response.status_code == 200
        data = response.json()
    
        print(data)
        ids = {r["id"] for r in data['results']}
        assert self.campaign_yesterday.id in ids
        assert self.campaign_today.id in ids

    def test_filter_with_invalid_date_format(self):
        """Тестирует обработку невалидного формата даты"""
        response = self.client.get(
            self.url,
            {"created_after": "invalid-date"},
            format="json"
        )
        
        assert response.status_code == 400
        assert "created_after" in response.json()