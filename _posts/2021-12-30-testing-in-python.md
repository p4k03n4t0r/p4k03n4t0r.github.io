---
layout: post
title:  "Testing in Python"
date:   2021-12-30
tags: [testing, python, unit-tests, service-tests, integration-tests]
---

_Testing is something which the more I program, the more I appreciate and learn about. Consequently this also leads to more discussions with teammates and other developers about what the best way is to write tests. I think having tests is almost always better than having no tests, even if they are just simple unit tests for only the happy flow. But there are plenty ways to test your code. So in my opinion you can write good tests and you can write better tests._

## Importance of tests

Tests are an essential part about software developing and as I said I appreciate them more and more, but why are they important? So from my experience this comes down to the following:

- They describe what the code should do. So without diving into the code, which someone else could have written, I can still understand what the code does.
- I can make changes to code without breaking anything, because tests give me certainty that everything still works as expected.
- Automated tests can be run in a pipeline, which gives me feedback about whether my code works in a real environment. If a test fails on an environment, the failed test tells me a direction where something is broken which allows me to fix it quickly.

## Types of tests

Often when people talk about testing one of the first things that comes up if the test pyramid. In [this article](https://martinfowler.com/articles/practical-test-pyramid.html) the following things can be taken away about the pyramid:

- If tests get more integrated they also get slower
- Write tests with different granularity
- The more high-level you get the fewer tests you should have

Although I agree with the first and second point, I don't totally agree with the third point. I think the higher the tests are integrated, the more valuable the tests are. There are also some other reasons, which I'll tell about when walking past the different types of tests. In every test pyramid the names of the levels are slightly different, but I think the level of integration of a test is more important than the name. So I'll be using the following levels:

1. Static tests
1. Unit tests
1. Service tests
1. Integration tests

## 1. Static tests

Static tests are tests where the code isn't run, but just the static code is analyzed in comparison to the other levels where the code is actually run. Although static testing often isn't part of the test pyramid, I still think it has some value. There are many different static tests, but for Python I think linting is the most important one. Since Python allows for [dynamic typing](https://realpython.com/python-type-checking/#dynamic-typing) and there is no go to editor (I prefer VS Code of course), this can lead to interesting code. I learned that you can use multiple linters as long as they don't focus on the same thing. In the next paragraphs I'll be talking about the different linters for Python that I think have value.

There are many linters which can be used to format your code. It's hard to say which one is the best, but I prefer [Black](https://github.com/psf/black). The goal of Black is to have (nearly) no configuration for your linter, preventing discussions about the formatting of code. On a project I used to have discussions about this with another teammate, while Black would take away these dicussions.

The linter [mypy](http://mypy-lang.org/) checks typing in Python. Before I programmed Python, I used to program in C# where typing was necessary. When I started with Python I created the habit to not use typing anymore, since it wasn't enforced. Although at first this made things easier, later on I noticed it made the quality of the code more poor. Still in my opinion typing should be seen as a way to help understand methods and not be to reliant on it, take for example the following code:

```python
def capitalize(name: str) -> int:
    # mypy error: Incompatible return value type (got "str", expected "int")
    return name.capitalize()

print(capitalize("abc"))
# although the return type indicates an int, the program still runs fine and prints "Abc"
```

The linter [prospector](http://prospector.landscape.io/en/master/) gives many usefull hints about improvements of the code, like unused variables. Although the hints are nice, they can be a bit too much. So far I haven't actually enforced prospector on a project, but I have just been using hints from prospector.

The linter [pydocstyle](https://github.com/PyCQA/pydocstyle/) forces documentation for methods and classes. This could be nice, although it forces you to also write documentation for methods which are self explanatory. I think this would depend on the type of the project, if the logic is difficult or the domain complex, enforcing documentation with pydocstyle could be nice.

## 2. Unit tests

Unit tests are written on the level of classes within a service, while calls to other classes or services are mocked. I think unit tests are a double edged sword: they can help you a lot, but they can also be misleading. Unit tests can help to quickly develop using test driven development (TDD), and I think it's something that the longer you program, the more you'll appreciate. Especially if you have isolated, complex logic it's perfect to write tests and wright your code around them.

But I think there is also a dark side of writing unit tests and that is when it's driven by test coverage. A famous tool for measering coverage in Python is, well not that suprising, [coverage](https://coverage.readthedocs.io/). It shows you even in a fancy HTML page the lines which your tests cover and the lines which still aren't covered with unit tests. A goal of some people or teams is to get that 100% coverage and celebrate you have fully covered the code with tests, hooray! I think this is often a waste, since there is a chance that a lot of the code and tests which are written weren't even necessary. When looking at the code coverage for unit tests, this could mislead you whether the code is actually called:

```python
def _divide(x, y):
    if y == 0:
        raise ZeroDivisionError()
    return x / y

def math(x, y, operation):
    if operation == "divide":
        if y == 0:
            raise ZeroDivisionError()
        return _divide(x, y)
    # .. other code

def test_divide_divide_by_zero():
    thrown_error = None
    try:
        _divide(1, 0)
    except ZeroDivisionError as e:
        thrown_error = e
    assert thrown_error and isinstance(thrown_error, ZeroDivisionError)

def test_math_divide_by_zero():
    thrown_error = None
    try:
        math(1, 0, "divide")
    except ZeroDivisionError as e:
        thrown_error = e
    assert thrown_error and isinstance(thrown_error, ZeroDivisionError)

# other tests to test the happy flow
```

Both the `_divide` (internal method) and `math` test whether the `y` value is a zero, since division by zero is not possible. By writing an unit test for both cases (including test cases for the other flows) will result in 100% code coverage, yay! Oh wait, is this actually a good thing? Our tests actually hide a flow which will never be executed. If we assume the `_divide` method is never called by another method within this module, the flow within the if check for zero never happens. Our code coverage hides this, but if we only wrote unit tests at the interface of this module, the `math` method, code coverage would show the flow never happens. This could be an indication that some code is not used and thus the code is more complex than necessary.

Another example of misleading code coverage is as follows:

```python
def square(x, y):
    return x + y

def test_square():
    assert square(2, 2) == 4
```

Although the test passes, the method by accident returns the right answer. The code coverage here is 100%, but the code doesn't do what it's supposed to do. To find these issues mutation testing could be the solution. With this type of tests the code is randomly 'mutated', for example replacing logical operators. If the test survives after it was mutated, this might indicate there is something wrong. In this case a mutation might change the plus operator to the actual square operator and the test still passes, which indicates we should take a look at this.

## 3. Service tests

Service tests are written on the level of a whole service. Here it depends whether calls to other services are mocked. I think it's important here to keep the microservice architecture in mind, where components like databases often aren't shared with other microservices. These components which belong to a microservice shouldn't be mocked, while calls to other services should be mocked. This way the code is tested in a much more realistic situation than unit tests.

I prefer to write theses tests using feature files, for example in Python using [behave](https://github.com/behave/behave). The tests describe in a textual scenario what the service functionally should do. I think this has two very big plus sides. The first is that it allows you to talk with people from the business about the functionality of a service, even if they don't have any techincal knowledge. I once made a mistake to describe an user without technical knowledge what the service did via unit tests. I can't recommend doing this, since the discussion was about a lot of things, but not about what the code should have done functionally.

The second advantage of feature files is that it acts as documentation for myself, the team and other developers within the organisation. I sometimes look at code with some unit tests which was written a few months ago and it's hard for me to understand what the code does without diving into it. If the functionality is described via feature files, it's really easy to understand what the code does without having to dive into it. This is even the same for other developers within the organization.

When I talked about unit tests I said that code coverage can be misleading, since it doesn't tell you whether all tests scenario's are realistic. In comparison to unit tests where calls to other classes within the services could be mocked, at service tests this isn't the case. Only calls to external services are mocked, where the service tests always call the interface or entrypoint of the service. If all the possible scenario's at the interface are covered via a service test (preferably via a feature file), code coverage can really be useful. Here uncovered code could tell you two things: this piece of code is not yet tested and should be tested or this piece of code will realistically be never called, why do we even have it?

## 4. Integration tests

Finally the integration tests cover the whole landscape without any mocks. Also called end to end tests or smoke tests, their definition is a bit different but their goal is the same: test a new version of a service within the whole landscape. In the previous level of tests a change could pass all tests within the service, but it could cause a failure in another microservice with which it communicates. Integration tests don't mock services, but are run in a production-like environment (or even production itself). Similar to service tests, a state can be prepared in the environment, for example injecting the right records into a database. Afterwards a call will be done on the interface of the landscape. After this call is processed in all services the response can be checked, but also the state of the rest of the environment. For example the call should have resulted in an additional record in a database or a message being put in a queue.
Of course features files also work for this and I really recommend this.

## Closing notes

Although I've said a lot of things about testing in Python, there's still a lot more to talk about. I hope all this information was usefull.
