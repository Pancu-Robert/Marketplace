"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()

        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        Thread.__init__(self, **kwargs)

    def process_prod(self, action_type, id_prod, quantity, cart_id):
        """
        process the product to add or remove it from the cart
        """
        # 2 operations to handle

        if action_type == "add":
            for _ in range(quantity):
                # add the product as many time as needed
                while self.marketplace.add_to_cart(cart_id, id_prod) is False:
                    time.sleep(self.retry_wait_time)
        elif action_type == "remove":
            for _ in range(quantity):
                self.marketplace.remove_from_cart(cart_id, id_prod)

    def run(self):
        # iterate through carts
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            #iterate through cart operation
            for command in cart:
                action_type = command.get("type")
                id_prod = command.get("product")
                quantity = command.get("quantity")
                # process the current product
                self.process_prod(action_type, id_prod, quantity, cart_id)

            self.marketplace.place_order(cart_id)
