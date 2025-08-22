from datetime import UTC, datetime, timedelta

import pytest
from rest_framework.test import APIClient

from models.models import Campaign

pytestmark = pytest.mark.django_db


class TestCampaignCreatedFilters:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.url = "/api/v1/agency/campaigns/"

        now = datetime.now(tz=UTC)
        self.today = now.date()
        self.yesterday = (now - timedelta(days=1)).date()
        self.tomorrow = (now + timedelta(days=1)).date()

        self.campaign_today = Campaign.objects.create(
            name="Today Campaign",
        )
        Campaign.objects.filter(id=self.campaign_today.id).update(created_at=self.today)

        self.campaign_yesterday = Campaign.objects.create(
            name="Yesterday Campaign",
        )
        Campaign.objects.filter(id=self.campaign_yesterday.id).update(created_at=self.yesterday)

        self.campaign_tomorrow = Campaign.objects.create(
            name="Tomorrow Campaign",
        )
        Campaign.objects.filter(id=self.campaign_tomorrow.id).update(created_at=self.tomorrow)

    def test_filter_created_after(self):
        response = self.client.get(self.url, {"created_after": self.today}, format="json")
        assert response.status_code == 200  # noqa: PLR2004
        data = response.json()

        assert data["results"][0]["id"] == self.campaign_today.id
        assert data["results"][1]["id"] == self.campaign_tomorrow.id

    def test_filter_created_before(self):
        response = self.client.get(self.url, {"created_before": self.today.isoformat()}, format="json")

        assert response.status_code == 200  # noqa: PLR2004
        data = response.json()

        assert data["results"][0]["id"] == self.campaign_today.id
        assert data["results"][1]["id"] == self.campaign_yesterday.id

    def test_filter_combined_date_range(self):
        response = self.client.get(self.url, {"created_after": self.yesterday, "created_before": self.today}, format="json")

        assert response.status_code == 200  # noqa: PLR2004
        data = response.json()

        ids = {r["id"] for r in data["results"]}
        assert self.campaign_yesterday.id in ids
        assert self.campaign_today.id in ids

    def test_filter_with_invalid_date_format(self):
        """Тестирует обработку невалидного формата даты."""
        response = self.client.get(self.url, {"created_after": "invalid-date"}, format="json")

        assert response.status_code == 400  # noqa: PLR2004
        assert "created_after" in response.json()
