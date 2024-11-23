
# from django.contrib.auth.models import User

# from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status 

import pytest 
from model_bakery import baker

from store.models import Collection, Product



@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection) -> Response:
        response = api_client.post('/store/collections/', collection)
        return response 
    return do_create_collection




@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip
    def test_if_user_anonimus_returns_401(self, create_collection):
        # AAA - (Arrange, Act, Assert)
        # Arrange
        # Nothing, since we creating the object 
        
        # Act
        # api_client is a fixture that comes from conftest.py file.
        # client = APIClient()
        # Always add forward slash to the end of the path, otherwise
        # you'll get an error
        response = create_collection({'title': 'Test Title'})
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self, authenticate, create_collection):
        # Arrange
        authenticate()
        # Act
        response = create_collection({'title': 'Test Title'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff=True)
        
        response = create_collection({'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None # type: ignore
        
    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):
        authenticate(is_staff=True)
        
        response = create_collection({'title': 'Test Title'})
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0 # type: ignore
         
      
@pytest.mark.django_db   
class TestRetriveCollection:
    
    def test_if_collection_exists_returns_200(self, api_client):
        # Arrange 
        # First create collection 
        # collection = Collection.objects.create(title='Test')
        # we can use model_bakery to avoid fullfilling all fields in the model
        collection = baker.make(Collection)
        
        # # example, creating 10 products in the same collection
        # products = baker.make(Product, collection=collection, _quantity=10)
        # Act
        response = api_client.get(f'/store/collections/{collection.id}/') # type: ignore
        # Assert 
        assert response.status_code == status.HTTP_200_OK
        # assert response.data['id'] == collection.id # type: ignore
        # assert response.data['title'] == collection.title # type: ignore
        # better way to compare 
        assert response.data == {
            'id': collection.id, # type: ignore
            'title': collection.title,
            'products_count': 0
        }
    
    def test_if_collection_does_not_exist_return_404(self, api_client):
        response = api_client.get(f'/store/collection/0/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND