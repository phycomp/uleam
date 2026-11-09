import sys, os, importlib.util
sys.path.insert(0, "/home/sam/代理人")

spec = importlib.util.spec_from_file_location("greeter", "/home/sam/代理人/generated_skills/greeter/greeter.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
Greeter = m.Greeter

def test_greet():
    g = Greeter()
    assert g.greet("World") == "Hello, World!"

def test_greet_custom_prefix():
    g = Greeter("Hi")
    assert g.greet("Sam") == "Hi, Sam!"

def test_greet_many():
    g = Greeter()
    assert g.greet_many(["A", "B"]) == ["Hello, A!", "Hello, B!"]