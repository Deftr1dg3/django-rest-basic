from locust import HttpUser, task, between
from random import randint



# Comment 'debug_toolbar.middleware.DebugToolbarMiddleware' in settings.MIDDLEWARE
# bacause it can make a mess with performance report

# User scenarios
class WebsiteUser(HttpUser):
    # Time between tasks
    # between(1, 5) = 1 to 5 seconds break between operations
    wait_time = between(1, 5)
    # Viewing products
    # Giving the task a proper weight @task(weight) based on 
    # user most commeon behaviour
    @task(2)
    def view_products(self):
        # print('View products')
        collection_id = randint(2, 6)
        # Name argument to group all URLs of the same kind
        self.client.get(
            f'/store/products/?collection_id={collection_id}', 
            name='/store/products'
            )
        
    # Viewing product details
    @task(4)
    def view_product(self):
        # print('View product by ID')
        product_id = randint(600, 700)  
        self.client.get(f'/store/products/{product_id}/', name='/store/products/:id')
    
    # Adding product to cart 
    @task(1)
    def add_product_to_cart(self):
        # print('Add product to cart')
        product_id = randint(600, 610)
        # Json argumens to send data to the server
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items',
            json={'product_id': product_id, 'quantity': 1}
            )
        
    @task
    def caching_example(self):
        self.client.get('/demo/caching/')
    
        
    # Its a lifecycle hooke. It called every time user starts browsing the website
    def on_start(self):
        response = self.client.post('/store/carts/')
        self.cart_id = response.json()['id']
        