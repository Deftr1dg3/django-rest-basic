from copy import deepcopy

from rest_framework.response import Response
from rest_framework import status 

import pytest 
from model_bakery import baker

from store.models import Collection, Product


PRODUCT = {
    "title": "Test",
    "slug": "test-test",
    "description": "Test descritpion",
    "unit_price": 199.99,
    "inventory": 42,
}
  

@pytest.fixture 
def collection():
    return baker.make(Collection) 
  
  
@pytest.fixture
def create_product(api_client):
    def do_create_product(product) -> Response:
        response = api_client.post('/store/products/', product)
        return response 
    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:
    
    def test_if_user_anonimus_return_401(self, create_product):
        response = create_product(product={})
 
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_not_admin_return_403(self, authenticate, create_product):
        authenticate(is_staff=False)
        
        response = create_product(product={})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN 
    
    def test_id_data_is_invalid_return_400(self, authenticate, create_product, collection):
        authenticate(is_staff=True)
        product = deepcopy(PRODUCT)
        product['title'] = ''
        product['collection'] = collection.id
        
        response = create_product(product=product)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_if_data_is_valid_return_201(self, authenticate, create_product, collection):
        authenticate(is_staff=True)
        product = deepcopy(PRODUCT)
        product['collection'] = collection.id
        
        response = create_product(product=product)
        
        assert response.status_code == status.HTTP_201_CREATED 
        
 
 
@pytest.mark.django_db 
class TestRetriveProduct:
    
    def test_if_product_exists_return_200(self, api_client):
        
        product = baker.make(Product)
        
        response = api_client.get(f'/store/products/{product.id}/') # type: ignore
        
        assert response.status_code == status.HTTP_200_OK
        
    
    def test_if_collection_does_not_exist_return_404(self, api_client):
        
        response = api_client.get('/store/products/0/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND 
        


@pytest.mark.django_db
class TestEndToEndProduct:
    
    def test_product_lifecycle(self, authenticate, api_client, collection):
        # Create  
        authenticate(is_staff=True)
        
        product = deepcopy(PRODUCT)
        product['collection'] = collection.id
        
        response = api_client.post(f'/store/products/', product)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Retrive 
        product_id = response.data['id']
        
        response = api_client.get(f'/store/products/{product_id}/')
        assert response.status_code == status.HTTP_200_OK

        # Update PATCH 
        response = api_client.patch(f'/store/products/{product_id}/', {'title': 'New Title PATCH'})
        assert response.status_code == status.HTTP_200_OK
        
        # Update PUT 
        product['title'] = 'New Title PUT'
        response = api_client.put(f'/store/products/{product_id}/', product)
        assert response.status_code == status.HTTP_200_OK
        
        # Delete 
        response = api_client.delete(f'/store/products/{product_id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Validate Deletion 
        response = api_client.get(f'/store/products/{product_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        
        
        
                