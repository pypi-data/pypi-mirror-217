================================
`jafdecs`: Just A Few Decorators
================================

Pretty useful decorators for Python functions, classes, and class methods.


Write Once, Read Many on Class Properties
=========================================

If a class property takes a long time to compute and is referenced many times, it is useful to lazily compute it once (when it is first referenced) and cache the result for later references.
This is where the ``worm`` submodule comes in.

::

    class SlowExample:
        @property
        def hard_property(self):
            import time
            time.sleep(5)
            print('This took a long time to compute!')
            return 5

    ex = SlowExample()
    print(ex.hard_property)
    print(ex.hard_property)


In the example above, the code will take around 10 seconds to run.
But it only needs to take 5 seconds if the property's value is cached, like in the example below.

::

    from jafdecs import worm

    @worm.onproperties
    class QuickerExample:
        @property
        def hard_property(self):
            import time
            time.sleep(5)
            print('This took a long time to compute!')
            return 5

    ex = QuickerExample()
    print(ex.hard_property)
    print(ex.hard_property)


Prime a function by executing something before
==============================================

Consider a function that takes a long time to compute a value, but once it is computed it may be used over and over again.
Exploiting this reusability is the idea behind memoization.
The Python standard library offers the ``functools.cache()`` and ``functools.lru_cache()`` decorators.
However, two limitations come to mind in use cases where memoization applies:

* The returned value is very big and cannot feasibly be cached in memory
* Programmatic control over when to pull from cache or recompute is not available

For either situation, the ``jafdecs.initialize.by(...)`` decorator can help.
Consider the examples below.

::

    def naive_function(path: pathlib.Path):
        # This code is somewhat complicated in that it initializes an asset before using it, unless the asset already exists.
        if not path.exists():
            print(f'File at {path} does not exist, so we will generate it before calling the actual function that needs it')
            generated_value = {}
            n = 18
            for i in range(10):
                key = str(i)
                value = i
                generated_value[key] = value

            print('Sleeping to simulate a hard-to-compute function.')
            time.sleep(2)
            with path.open('w') as file:
                json.dump(generated_value, file)

        print(f'File at {path} now exists, so we can get its data.')
        with path.open() as file:
            value = json.load(file)
        
        pprint(value)
    
    naive_function(path=pathlib.Path('example.json'))


In the example above, the code initializes an asset if it doesn't exist, and then uses that asset when it does.
If the asset already existed, it skips the initialization entirely.
For the sake of code cleanliness and ease of reading, the ``jafdecs.initialize.by(...)`` decorator allows these two distinct code blocks to be separated.

::

    from jafdecs import initialize, utilities

    import pathlib
    import time
    import json
    from pprint import pprint


    def priming_function(path: pathlib.Path):
        print(f'File at {path} does not exist, so we will generate it before calling the actual function that needs it')
        generated_value = {}
        for i in range(10):
            key = str(i)
            value = i
            generated_value[key] = value

        print('Sleeping to simulate a hard-to-compute function.')
        time.sleep(2)
        with path.open('w') as file:
            json.dump(generated_value, file)


    @initialize.by(func=priming_function, condition=utilities.filenotfound)
    def actual_function(path: pathlib.Path):
        print(f'File at {path} now exists, so we can get its data.')
        with path.open() as file:
            value = json.load(file)
        
        pprint(value)


    actual_function(path=pathlib.Path('example.json'))
    actual_function(path=pathlib.Path('example.json'))


In the example above, the initializing code is separated in its own function, reducing the clutter in the actual function to only the code that is needed to speed things up.
The first execution is primed by the initializing function.
When the second execution is called, no priming is needed.
The assets produced by the first priming are reused.
