
from pytest import raises
from flexx.util.testing import run_tests_if_main

from flexx.pyscript import js, JSError, py2js, evaljs, evalpy


def nowhitespace(s):
    return s.replace('\n', '').replace('\t', '').replace(' ', '')


class TestBuildins:
    
    def test_isinstance(self):
        # The resulting code is not particularly pretty, so we just
        # test outcome
        
        assert evalpy('isinstance(3.0, list) == True') == 'false'
        assert evalpy('isinstance(3.0, float) == True') == 'true'
        
        assert evalpy('x={}; isinstance(x.foo, "undefined")') == 'true'
        
        assert evalpy('isinstance(None, "null")') == 'true'
        assert evalpy('isinstance(undefined, "undefined")') == 'true'
        #
        assert evalpy('isinstance(None, "undefined")') == 'false'
        assert evalpy('isinstance(undefined, "null")') == 'false'
        
        assert evalpy('isinstance(3, float)') == 'true'
        assert evalpy('isinstance(3, "number")') == 'true'
        #
        #assert evalpy('isinstance(3, int)') == 'false'  # int is not defined
        
        assert evalpy('isinstance("", str)') == 'true'
        assert evalpy('isinstance("", "string")') == 'true'
        #
        assert evalpy('isinstance("", list)') == 'false'
        
        assert evalpy('isinstance(True, bool)') == 'true'
        assert evalpy('isinstance(True, "boolean")') == 'true'
        #
        assert evalpy('isinstance(True, float)') == 'false'
        
        assert evalpy('isinstance([], list)') == 'true'
        assert evalpy('isinstance([], "array")') == 'true'
        #
        assert evalpy('isinstance([], "object")') == 'false'
        assert evalpy('isinstance([], "Object")') == 'false'
        assert evalpy('isinstance([], dict)') == 'false'
        
        assert evalpy('isinstance({}, dict)') == 'true'
        assert evalpy('isinstance({}, "object")') == 'true'
        #
        assert evalpy('isinstance({}, list)') == 'false'
        assert evalpy('isinstance({}, "array")') == 'false'
        
        # own class
        code = 'function MyClass () {return this;}\nx = new MyClass();\n'
        assert evaljs(code + py2js('isinstance(x, "object")')) == 'true'
        assert evaljs(code + py2js('isinstance(x, "Object")')) == 'true'
        assert evaljs(code + py2js('isinstance(x, "MyClass")')) == 'true'
        assert evaljs(code + py2js('isinstance(x, MyClass)')) == 'true'
    
    def test_max(self):
        assert py2js('max(3, 4)') == 'max(3, 4);'
    
    def test_print(self):
        # Test code
        assert py2js('print()') == 'console.log();'
        assert py2js('print(3)') == 'console.log(3);'
        assert py2js('foo.print()') == 'foo.print();'
        
        # Test single
        assert evalpy('print(3)') == '3'
        assert evalpy('print(3); print(3)') == '3\n3'
        assert evalpy('print(); print(3)') == '\n3'  # Test \n
        assert evalpy('print("hello world")') == 'hello world'
        # Test multiple args
        assert evalpy('print(3, "hello")') == '3 hello'
        assert evalpy('print(3+1, "hello", 3+1)') == '4 hello 4'
        # Test sep and end
        assert evalpy('print(3, 4, 5)') == '3 4 5'
        assert evalpy('print(3, 4, 5, sep="")') == '345'
        assert evalpy('print(3, 4, 5, sep="\\n")') == '3\n4\n5'
        assert evalpy('print(3, 4, 5, sep="--")') == '3--4--5'
        assert evalpy('print(3, 4, 5, end="-")') == '3 4 5-'
        assert evalpy('print(3, 4, 5, end="\\n\\n-")') == '3 4 5\n\n-'
        
        raises(JSError, py2js, 'print(foo, file=x)')
        raises(JSError, py2js, 'print(foo, bar=x)')
    
    def test_len(self):
        assert py2js('len(a)') == 'a.length;'
        assert py2js('len(a, b)') == 'len(a, b);'


class TestListMethods:
    
    def test_append(self):
        assert nowhitespace(evalpy('a = [2]; a.append(3); a')) == '[2,3]'
    
    def test_remove(self):
        assert nowhitespace(evalpy('a = [2, 3]; a.remove(3); a')) == '[2]'
        assert nowhitespace(evalpy('a = [2, 3]; a.remove(2); a')) == '[3]'


run_tests_if_main()
