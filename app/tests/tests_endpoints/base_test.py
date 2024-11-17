# import unittest
# from app import create_app

# class BaseTestClass(unittest.TestCase):
    
#     @classmethod
#     def setUpClass(cls):
#         cls.app = create_app()
#         cls.client = cls.app.test_client()

#         # Create a shared user to use as owner for all places and reviews
#         response = cls.client.post('/api/v1/users/', json={
#             "first_name": "John",
#             "last_name": "Doe",
#             "email": "john.doe@gmail.com"
#         })
#         cls.owner_id = response.get_json()['id']

#         # Create some shared amenities
#         response1 = cls.client.post('/api/v1/amenities/', json={"name": "Pool"})
#         cls.amenity1_id = response1.get_json()['id']

#         response2 = cls.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
#         cls.amenity2_id = response2.get_json()['id']

#         # Create a shared place to use for reviews
#         response = cls.client.post('/api/v1/places/', json={
#             "title": "Test Place",
#             "description": "A nice test place",
#             "price": 100.0,
#             "latitude": 40.7128,
#             "longitude": -74.0060,
#             "owner_id": cls.owner_id,
#             "amenities": [cls.amenity1_id, cls.amenity2_id]
#         })
#         cls.place_id = response.get_json()['id']