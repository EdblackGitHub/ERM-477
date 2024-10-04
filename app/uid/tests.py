from django.test import TestCase
from unittest.mock import patch, MagicMock
from .models import CounterNode
from .models import Provider, LCVTerm
from .utils import generate_uid, issue_uid, send_notification

class TestCounterNode(TestCase):
    @patch('app.uid.models.CounterNode.save')
    @patch('app.uid.models.CounterNode.nodes.first_or_none')
    def test_get_creates_counter_node_if_none(self, mock_first_or_none, mock_save):
        mock_first_or_none.return_value = None
        counter_node = CounterNode.get()
        mock_first_or_none.assert_called_once()
        mock_save.assert_called_once()
        self.assertEqual(counter_node.counter, 0)

    @patch('app.uid.models.CounterNode.create_node')
    @patch('app.uid.models.CounterNode.nodes.first_or_none')
    def test_get_returns_counter_node(self, mock_first_or_none, mock_create_node):
        mock_counter_node = MagicMock()
        mock_counter_node.counter = 1
        mock_first_or_none.return_value = mock_counter_node

        counter_node = CounterNode.get()

        mock_first_or_none.assert_called_once()

        mock_create_node.assert_not_called()

        self.assertEqual(counter_node.counter, 1)
    
    
    @patch('app.uid.models.CounterNode.save')
    def test_create_node(self, mock_save):
        counter_node = CounterNode.create_node()
        mock_save.assert_called_once()
        self.assertEqual(counter_node.counter, 0)
    
    @patch('app.uid.models.CounterNode.save')
    @patch('app.uid.models.CounterNode.get')
    def test_increment(self, mock_get, mock_save):
        mock_counter_node = MagicMock()
        mock_counter_node.counter = 1
        mock_get.return_value = mock_counter_node

        counter_node = CounterNode.increment()

        mock_get.assert_called_once()
        self.assertEqual(counter_node.counter, 2)
        mock_save.assert_called_once()

class UIDGenerationTestCase(TestCase):

    def test_uid_generation_for_providers(self):
        provider = Provider.objects.create(name="Test Provider")
        uid = generate_uid(provider)
        self.assertIsNotNone(uid)
        self.assertEqual(len(uid), 10)  # Assuming UID length is 10
        self.assertNotIn(uid, [p.uid for p in Provider.objects.all() if p.uid])

    def test_uid_generation_for_lcv_terms(self):
        lcv_term = LCVTerm.objects.create(name="Test LCV Term")
        uid = generate_uid(lcv_term)
        self.assertIsNotNone(uid)
        self.assertEqual(len(uid), 10)  # Assuming UID length is 10
        self.assertNotIn(uid, [l.uid for l in LCVTerm.objects.all() if l.uid])

    def test_issuing_uid_to_providers(self):
        provider = Provider.objects.create(name="Test Provider")
        uid = issue_uid(provider)
        self.assertIsNotNone(uid)
        self.assertEqual(provider.uid, uid)

    def test_issuing_uid_to_lcv_terms(self):
        lcv_term = LCVTerm.objects.create(name="Test LCV Term")
        uid = issue_uid(lcv_term)
        self.assertIsNotNone(uid)
        self.assertEqual(lcv_term.uid, uid)

    def test_verification_of_uid_assignment(self):
        provider = Provider.objects.create(name="Test Provider")
        lcv_term = LCVTerm.objects.create(name="Test LCV Term")
        provider_uid = issue_uid(provider)
        lcv_term_uid = issue_uid(lcv_term)
        self.assertEqual(provider.uid, provider_uid)
        self.assertEqual(lcv_term.uid, lcv_term_uid)
        self.assertTrue(provider.uid.startswith("P-"))  # Assuming provider UIDs start with "P-"
        self.assertTrue(lcv_term.uid.startswith("L-"))  # Assuming LCV term UIDs start with "L-"

    def test_notification_on_successful_uid_issuance(self):
        provider = Provider.objects.create(name="Test Provider")
        lcv_term = LCVTerm.objects.create(name="Test LCV Term")
        provider_uid = issue_uid(provider)
        lcv_term_uid = issue_uid(lcv_term)

        # Assuming you have a function to send notifications
        self.assertTrue(send_notification(provider, provider_uid))
        self.assertTrue(send_notification(lcv_term, lcv_term_uid))
        #Test Changes