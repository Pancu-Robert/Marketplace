"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        Thread.__init__(self, **kwargs)

    def publish_prod(self, id_product, quantity, wait_time):
        """
        function that publish a product into marketplace
        """
        producer_id = self.marketplace.register_producer()
        # publish the product as many time as required
        for _ in range(quantity):
            if self.marketplace.publish(producer_id, id_product) is False:
                time.sleep(self.republish_wait_time)
            else:
                time.sleep(wait_time)

    def run(self):
        while True:
            # iterate through products
            for product in self.products:
                id_prod = product[0]
                quantity = product[1]
                wait_time = product[2]
                # try to publish the current product
                self.publish_prod(id_prod, quantity, wait_time)
