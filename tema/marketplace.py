"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, currentThread
import unittest

class TestMarketplace(unittest.TestCase):
    """
    Class that represents the unitTest for Marketplace.
    """

    def setUp(self):
        """
        Set up a instance of the marketplace
        """
        self.marketplace = Marketplace(5)

    def test_register_producer(self):
        """
        Register a new producer
        """
        producer_id = self.marketplace.register_producer()
        self.assertEqual(producer_id, 0)

    def test_publish(self):
        """
        Publish a new product
        """
        producer_id = self.marketplace.register_producer()
        self.assertTrue(self.marketplace.publish(producer_id, "Coffee"))

    def test_new_cart(self):
        """
        Create a new cart
        """
        cart_id = self.marketplace.new_cart()
        self.assertEqual(cart_id, 0)

    def test_add_to_cart(self):
        """
        Add a product to a cart
        """
        cart_id = self.marketplace.new_cart()
        self.assertTrue(self.marketplace.add_to_cart(cart_id, "Coffee"))

    def test_remove_from_cart(self):
        """
        Remove a product from a cart
        """
        cart_id = self.marketplace.new_cart()
        self.assertTrue(self.marketplace.remove_from_cart(cart_id, "Coffee"))

    def test_place_order(self):
        """
        Test that the marketplace can place an order.
        """
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, "Coffee")
        order = self.marketplace.place_order(cart_id)
        self.assertEqual(order[0], "Coffee")

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        self.producer_id = -1 # number of producers
        self.cart_id = -1 # number of carts

        self.mutex = Lock() # 1 mutex to for critical sections

        self.producers_items = [] # items of a single producers
        self.all_products = [] # all products from all producers
        self.carts_dictionary = {} # key = product, values = producers
        self.products_dictionary = {} # key = cart_id, values = products

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        #
        self.mutex.acquire()
        # increment the producer_id
        self.producer_id += 1
        self.producers_items.append(0)
        self.mutex.release()

        return self.producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.mutex.acquire()
        # if it is enough space to public another product
        if self.queue_size_per_producer >= self.producers_items[producer_id]:
            self.all_products.append(product)
            self.producers_items[producer_id] += 1
            self.products_dictionary[product] = producer_id
            self.mutex.release()
            return True

        self.mutex.release()
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.mutex.acquire()
        # incremenent the cart_id and create a new empty cart
        self.cart_id += 1
        cart = []
        self.carts_dictionary[self.cart_id] = cart
        self.mutex.release()

        return self.cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.mutex.acquire()
        # iterate to all products to find the given product
        for prod in self.all_products:
            if prod == product:
                self.all_products.remove(product)
                producer_id = self.products_dictionary[product]
                self.producers_items[producer_id] -= 1
                self.carts_dictionary[cart_id].append(product)
                self.mutex.release()
                return True

        self.mutex.release()
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.mutex.acquire()
        # remove prodcut from the cart
        self.carts_dictionary[cart_id].remove(product)
        # put the product back to the list with all products
        self.all_products.append(product)
        producer_id = self.products_dictionary[product]
        self.producers_items[producer_id] += 1
        self.mutex.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        prod_list = self.carts_dictionary.get(cart_id)

        # print products
        for product in prod_list:
            self.mutex.acquire()
            print(currentThread().getName(), "bought", product)
            self.mutex.release()
        return prod_list
