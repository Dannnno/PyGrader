"""
Copyright (c) 2014 Dan Obermiller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

You should have received a copy of the MIT License along with this program.
If not, see <http://opensource.org/licenses/MIT>
"""

from difflib import get_close_matches as gcm
import abc
import sys
import types
import unittest


class auto_grader(unittest.TestCase):
    """The base auto_grader class.  It has all of the built in functionality to
    run the majority of desired tests.  Is a subclass of unittest.TestCase so 
    normal unit testing methods (such as self.assertEqual()) will work in this
    class.  
    
    Grader is asked to subclass this with their own desired functionality.  If 
    capturing printed statements is desired create the class with
    
        grader = my_subclass(write=True)
        
    and make sure `my_subclass` has the write method implemented appropriately
    (however you're going to be checking for values).  Is implemented as an 
    abstract method, so all subclasses will have to implement it, however
    implementing it with `pass` will suffice.
    
    After creating your test you're going to have to get the so-called "good"
    function names - that is the names used by your API.  If you don't want to
    allow for API flexibility then you should override black_magic such that 
    self.student_functions[func_name]() calls the API named-function.  Assuming
    you allow for API flexibility then call
    
        my_subclass.good_func_names(list_of_function_names)
        
    That is a @classmethod so make sure you call it on my_subclass and not your
    instance.
    
    The auto_grader is intended to be a single instance per student assignment.
    Loops are ideal for this.  In order to run the tests do something like
    
        grader = my_subclass(write=True)
        grader.get_names(student_name, module_name, filepath)
    
    and all of your functions will be callable as 
    
        self.student_functions[func_name](*args, **kwargs)
    
    When implementing your test functions you can just do 
    
        def test_some_func(self, args):
            map(self.assertEqual, 
                map(self.student_functions[func_name],
                    arglist),
                expected_value_list)
                    
    When you've finished using an instance for a test you should call
     
        grader.print_results(filepath)
    
    And you'll be good. If you'd like to print all results to the same file then
    make sure you call
    
        grader.print_results(filepath, shared=True)
        
    And all results will be printed into the shared filepath
    """
    good_functions = []
    
    def __init__(self, write=False, **kwargs): 
        super(unittest.TestCase, self).__init__(**kwargs)
        self.student_functions = {}
        self.names = []
        sys.path.insert(0, [])
        if write:
            self.saved = sys.stdout
            sys.stdout = self
        
    def __str__(self): 
        return "Base class for autograding Python homework"
        
    def __repr__(self): 
        return str(self)
    
    def __unicode__(self): 
        return unicode(str(self))
    
    @abc.abstractmethod
    def setUp(self):
        """What should happen in the setup of the tests"""
        
    @abc.abstractmethod
    def tearDown(self):
        """What should happen while tearing down the tests""" 
        
    @abc.abstractmethod
    def write(self, string):
        """This replaces your sys.stdout as necessary.  If you don't need to 
        catch values in print then just have this method pass"""
        
    @classmethod
    def good_func_names(cls, names):
        """Stores the desired function names in a class attribute"""
        cls.good_functions = names[:]      
        
    def get_names(self, student_name, mod_name, filepath):
        """Gets the function names the student used"""
        sys.path[0] = filepath
        globals()["Student"] = __import__(mod_name)
        self.names = [globals()["Student"].__dict__.get(var).__name__
                      for var in dir(globals()["Student"])
                      if (isinstance(globals()["Student"].__dict__.get(var),
                                     types.FunctionType) or
                          isinstance(globals()["Student"].__dict__.get(var),
                                     types.ClassType))]
                                
        for func in auto_grader.good_functions:
            match = gcm(func, self.names)
            if match:
                self.student_functions[func] = self.black_magic(match[0])
            else:
                self.student_functions[func] = self.black_magic(func)
    
    def black_magic(self, func_name): 
        """Warning - black magic ahead (all functions)
        We're executing a string.  
        
        It assigns the name value to the output of the following expresson.  The
        `globals()[\"homework\"].` part of it accesses the current homework 
        assignment and then uses a fuzzy comparison method (look at 
        `get_functions()`) to get the actual name used by the assignment (gives us
        API flexibility).  It then store this function in 
        self.student_functions[func_name] so it is callable, ie we could do 
        
            self.student_functions[func_name](*args, **kwargs)
        
        """
        try:
            exec(''.join(["value = globals()[student_name].", 
                           self.student_functions[func_name]]),
                           globals(),
                           locals())
            
            self.student_functions[func_name] = value
        except AttributeError as e:
            print e
            return 
    
            
if __name__ == "__main__":
    pass
    