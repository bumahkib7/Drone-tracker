from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User

from drones.models import DroneCategory, Drone


# Create your tests here.
class APIClient:
  def __init__(self):
    self._content = None
    self._status_code = None

  def get(self):
    self._content = {
      'drone-categories': 'http://testserver/api/drone-categories/',
      'drones': 'http://testserver/api/drones/',
      'pilots': 'http://testserver/api/pilots/',
      'competitions': 'http://testserver/api/competitions/'
    }
    self._status_code = 200

  @property
  def content(self):
    return self._content

  @property
  def status_code(self):
    return self._status_code


class APITestCase:
  def __init__(self):
    self.user = None
    self.client = None

  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(username='tester', password='12345')


class DroneCategoryTests(APITestCase):
  def test_create_drone_category(self):
    """
    Ensure we can create a new drone category object.
    """
    url = reverse('dronecategory-list')
    data = {'name': 'Hexacopter'}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(DroneCategory.objects.count(), 1)
    self.assertEqual(DroneCategory.objects.get().name, 'Hexacopter')

  def test_create_invalid_drone_category(self):
    """
    Ensure we can't create a new drone category with invalid data.
    """
    url = reverse('dronecategory-list')
    data = {'name': ''}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_drone_category(self):
    """
    Ensure we can update an existing drone category object.
    """
    dronecategory = DroneCategory.objects.create(name='Hexacopter')
    data = {'name': 'Octocopter'}
    url = reverse('dronecategory-detail', kwargs={'pk': dronecategory.pk})
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(DroneCategory.objects.get().name, 'Octocopter')

  def test_update_invalid_drone_category(self):
    """
    Ensure we can't update an existing drone category object with invalid data.
    """
    dronecategory = DroneCategory.objects.create(name='Helicopter')
    data = {'name': ''}
    url = reverse('dronecategory-detail', kwargs={'pk': dronecategory.pk})
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_delete_drone_category(self):
    """
    Ensure we can delete an existing drone category object.
    """
    dronecategory = DroneCategory.objects.create(name='Helicopter')
    url = reverse('dronecategory-detail', kwargs={'pk': dronecategory.pk})
    response = self.client.delete(url, format='json')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(DroneCategory.objects.count(), 0)

  def test_get_drone_category(self):
    """
    Ensure we can get an existing drone category object.
    """
    dronecategory = DroneCategory.objects.create(name='Helicopter')
    url = reverse('dronecategory-detail', kwargs={'pk': dronecategory.pk})
    response = self.client.get(url, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], 'Helicopter')

  def test_get_invalid_drone_category(self):
    """
    Ensure we can't get a non-existing drone category object.
    """
    url = reverse('dronecategory-detail', kwargs={'pk': 99})
    response = self.client.get(url, format='json')
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def assertEqual(self, status_code, HTTP_201_CREATED):
    pass


class DroneTests(APITestCase):

  def test_create_drone(self):
    """
    Ensure we can create a new drone object.
    """
    dronecategory = DroneCategory.objects.create(name='Hexacopter')
    url = reverse('drone-list')
    data = {
      'name': 'T-800',
      'drone_category': 'http://testserver/api/drone-categories/' + str(dronecategory.pk) + '/',
      'manufacturing_date': '2016-01-01',
      'has_it_competed': False,
      'inserted_timestamp': '2016-01-01T00:00:00Z'
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Drone.objects.count(), 1)
    self.assertEqual(Drone.objects.get().name, 'T-800')

  def assertEqual(self, status_code, HTTP_201_CREATED):
    pass

  def test_create_invalid_drone(self):
    """
    Ensure we can't create a new drone with invalid data.
    """
    url = reverse('drone-list')
    data = {
      'name': '',
      'drone_category': 'http://testserver/api/drone-categories/1/',
      'manufacturing_date': '2016-01-01',
      'has_it_competed': False,
      'inserted_timestamp': '2016-01-01T00:00:00Z'
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_drone(self):
    """
    Ensure we can update an existing drone object.
    """
    dronecategory = DroneCategory.objects.create(name='Hexacopter')
    drone = Drone.objects.create(
      name='T-800',
      drone_category=dronecategory,
      manufacturing_date='2016-01-01',
      has_it_competed=False,
      inserted_timestamp='2016-01-01T00:00:00Z'
    )
    data = {
      'name': 'T-1000',
      'drone_category': 'http://testserver/api/drone-categories/' + str(dronecategory.pk) + '/',
      'manufacturing_date': '2016-01-01',
      'has_it_competed': False,
      'inserted_timestamp': '2016-01-01T00:00:00Z'
    }
    url = reverse('drone-detail', kwargs={'pk': drone.pk})
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(Drone.objects.get().name, 'T-1000')

  def test_update_invalid_drone(self):
    """
    Ensure we can't update an existing drone object with invalid data.
    """
    dronecategory = DroneCategory.objects.create(name='Helicopter')
    drone = Drone.objects.create(
      name='T-800',
      drone_category=dronecategory,
      manufacturing_date='2016-01-01',
      has_it_competed=False,
      inserted_timestamp='2016-01-01T00:00:00Z'
    )
    data = {
      'name': '',
      'drone_category': 'http://testserver/api/drone-categories/' + str(dronecategory.pk) + '/',
      'manufacturing_date': '2016-01-01',
      'has_it_competed': False,
      'inserted_timestamp': '2016-01-01T00:00:00Z'
    }
    url = reverse('drone-detail', kwargs={'pk': drone.pk})
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_delete_drone(self):
    """
    Ensure we can delete an existing drone object.
    """
    dronecategory = DroneCategory.objects.create(name='Helicopter')
    drone = Drone.objects.create(
      name='T-800',
      drone_category=dronecategory,
      manufacturing_date='2016-01-01',
      has_it_competed=False,
      inserted_timestamp='2016-01-01T00:00:00Z'
    )
    url = reverse('drone-detail', kwargs={'pk': drone.pk})
    response = self.client.delete(url, format='json')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Drone.objects.count(), 0)

  def test_get_drone(self):
    """
    Ensure we can get an existing drone object.
    """
    dronecategory = DroneCategory.objects.create(name='Helicopter')
    drone = Drone.objects.create(
      name='T-800',
      drone_category=dronecategory,
      manufacturing_date='2016-01-01',
      has_it_competed=False,
      inserted_timestamp='2016-01-01T00:00:00Z'
    )
    url = reverse('drone-detail', kwargs={'pk': drone.pk})
    response = self.client.get(url, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], 'T-800')


class PilotTests(APITestCase):

  def test_create_pilot(self):
    """
    Ensure we can create a new pilot object.
    """
    url = reverse('pilot-list')
    data = {
      'name': ' ',


