from models.item import ItemModel
from models.user import UserModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                expected = {'message': 'Item not found'}
                self.assertEqual(404, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                expected = {'name': 'test', 'price': 19.99}
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                expected = {'name': 'test', 'price': 17.99}
                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                expected = {'message': 'Item deleted'}
                resp = client.delete('/item/test')

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                expected = {'message': "An item with name \'test\' already exists."}
                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(400, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})
                expected = {'name': 'test', 'price': 17.99}

                self.assertEqual(200, resp.status_code)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)

                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})
                expected = {'name': 'test', 'price': 17.99}

                self.assertEqual(200, resp.status_code)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                expected = {'items': [{'name': 'test', 'price': 5.99}]}

                resp = client.get('/items')

                self.assertDictEqual(expected, json.loads(resp.data))


