import datetime as dt

from django.urls import reverse_lazy
from model_bakery import baker
from pluck import pluck

from timeline.events.models import Event
from timeline.testcase import TestCase


class EventTestCase(TestCase):
    def test_generates_thumbnail(self):
        event = baker.make(Event)
        self.create_image(event=event)
        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event.id}))
        self.assertIn(".jpg", response.json()["thumbnail"])

    def test_tells_if_images_exist(self):
        event = baker.make(Event)
        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event.id}))
        self.assertFalse(response.json()["has_images"])

        self.create_image(event=event)
        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event.id}))
        self.assertTrue(response.json()["has_images"])

    def test_retrieves_relations_from_both_sides(self):
        event_a = baker.make(Event)
        event_b = baker.make(Event)
        event_a.relations.set([event_b])

        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event_a.id}))
        self.assertEqual([event_b.id], pluck(response.json()["relations"], "id"))

        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event_b.id}))
        self.assertEqual([event_a.id], pluck(response.json()["relations"], "id"))

        event_b.relations.set([event_a])

        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event_a.id}))
        self.assertEqual([event_b.id], pluck(response.json()["relations"], "id"))

        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event_b.id}))
        self.assertEqual([event_a.id], pluck(response.json()["relations"], "id"))

    def test_serializes_html_representation_of_the_description(self):
        event = baker.make(
            Event,
            description={
                "time": 1676127168130,
                "blocks": [{"id": "JksHTqcYVk", "data": {"text": "test"}, "type": "paragraph"}],
                "version": "2.26.4",
            },
        )
        response = self.client.get(reverse_lazy("event-detail", kwargs={"pk": event.id}))
        self.assertEqual("<p>test</p>", response.json()["description_html"])

    def test_creates_event_with_images(self):
        image = self.create_uploaded_image()
        response = self.client.post(
            reverse_lazy("event-list"),
            {"title": "Title", "date": dt.datetime(2000, 1, 1), "images": [image]},
        )
        self.assertEqual(201, response.status_code, response.json())
