import time


def print_time_to_work(tell_me_about_you):
    """
    decorator with parameter
    :param tell_me_about_you: I guess to see where are we going from (main or module)
    :return: link to real_decorator func
    """

    def real_decorator(function):
        """
        I am real decorator, but I can use parameter from above decorator
        :param function: our function which we need to decorate
        :return: link to wrapper
        """

        # print("I know everything about you. Where are you going from? ", tell_me_about_you)
        def wrapper(*args):
            """ I  only decorator inside other decorator. I'm going to wrap your function"""
            print("I see you come from", tell_me_about_you)
            print("start reading file", *args)
            start_time = time.perf_counter()
            res = function(*args)  # it's our function with they arguments, and it must be returned
            end_time = time.perf_counter()
            print(f"Time taken for file open is {end_time - start_time}")
            return res

        return wrapper

    return real_decorator


def light_print_time_to_work(function):
    """
    I am light decorator
    :param function: our function which we need to decorate
    :return: link to wrapper
    """

    def wrapper(*args, **kwargs):
        """ I  just easy decorator. I am going to wrap your function"""
        # print(f"start function {function}")      # for debug use aslo    , *args)
        start_time = time.perf_counter()

        # it's our function with they arguments, and it must be returned
        res = function(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"time taken for operation is {end_time - start_time}")
        return res

    return wrapper
