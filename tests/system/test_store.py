from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')

                expected = {'id': 1, 'name': 'test', 'items': []}
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')
                resp = client.post('/store/test')

                self.assertEqual(resp.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.delete('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'},
                                     json.loads(resp.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')

                expected = {'id': 1, 'name': 'test', 'items': []}

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test')

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                     json.loads(resp.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                expected = {'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}
                resp = client.get('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(expected,
                                     json.loads(resp.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                expected = {'stores': [{'id': 1, 'name': 'test', 'items': []}]}
                resp = client.get('/stores')
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                expected = {'stores': [{'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}]}
                resp = client.get('/stores')
                self.assertDictEqual(expected, json.loads(resp.data))
