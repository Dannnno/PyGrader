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

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from difflib import get_close_matches as gcm
import abc
import contextlib
import sys
import types
import unittest


sys.path.insert(0, "")
        

class auto_grader(unittest.TestCase):
    """The base auto_grader class.  It has all of the built in functionality to
    run the majority of desired tests.  Is a subclass of unittest.TestCase so
    normal unit testing methods (such as self.assertEqual()) will work in this
    class.

    Grader is asked to subclass this with their own desired functionality.  If
    capturing printed statements is desired then just use the context manager
    autograder.capture() like so
    
        def test_my_func(self):
            my_func = my_subclass.black_magic(func_name)
            
            with self.capture() as (out, err):
                map(self.assertEqual,
                    map(my_func,
                        arglist),
                    out)
                    
    If if this doesn't do exactly you want then just override capture with the 
    desired functionality.
    
    When implementing your test functions you can just do

        def test_some_func(self, args):
            some_func = my_subclass.black_magic(func_name)
            map(self.assertEqual,
                map(some_func,
                    arglist),
                expected_value_list)

    Actually testing:

    Just call

        test_assignment(subclass, good_names, student_name,
                        module_name, mod_path, grade_path)

    With all of the appropriate arguments.  Loops are ideal.  For example:

        for submission in submissions:
            test_assignment(subclass, my_names, submission[0],
                            submission[1], submission[2], submission[3])

    Where submission has all of the data you need.
    """
    good_functions = []
    student_functions = {}
    names = []

    @abc.abstractmethod
    def setUp(self):
        """What should happen in the setup of the tests"""

    @abc.abstractmethod
    def tearDown(self):
        """What should happen while tearing down the tests"""

    @classmethod
    def __str__(cls):
        return "Base class for autograding Python homework"

    @classmethod
    def __repr__(cls):
        return str(cls)

    @classmethod
    def __unicode__(cls):
        return unicode(str(cls))

    @classmethod
    def good_func_names(cls, names):
        """Stores the desired function names in a class attribute"""
        cls.good_functions = names[:]

    @classmethod
    def get_names(cls, student_name, mod_name, filepath):
        """Gets the function names the student used"""

        sys.path[0] = filepath
        globals()["Student"] = __import__(mod_name, globals(), locals())
        cls.names = [globals()["Student"].__dict__.get(var).__name__
                      for var in dir(globals()["Student"])
                      if (isinstance(globals()["Student"].__dict__.get(var),
                                     types.FunctionType) or
                          isinstance(globals()["Student"].__dict__.get(var),
                                     types.ClassType))]

        for name in cls.good_functions:
            match = gcm(name, cls.names)
            if match:
                cls.student_functions[name] = match[0]
            else:
                cls.student_functions[name] = name
            

    @classmethod
    def black_magic(cls, func_name):
        """Warning - black magic ahead
        We're executing a string.

        It assigns the name value to the output of the following expresson.  The
        `globals()[\"homework\"].` part of it accesses the current homework
        assignment and then uses a fuzzy comparison method (look at
        `get_functions()`) to get the actual name used by the assignment (gives us
        API flexibility).  It then returns the function so it can be called.  For example

            def test_my_function(self):
                my_function = sub_class.black_magic("Some_Func_Name")
                self.assertEqual(my_function(*args), test_value)
                self.assertEqual(my_function(*otherargs), next_value)

        etc
        """

        try:
            exec(''.join(["value = globals()['Student'].", func_name]), globals(), locals())

            return value
        except AttributeError as e:
            print "Black magic error:"
            print "\t", e
            return
            
    @contextlib.contextmanager
    def capture(self):
        oldout, olderr = sys.stdout, sys.stderr
        
        try:
            out=[StringIO(), StringIO()]
            sys.stdout, sys.stderr = out
            yield out
            
        finally:
            sys.stdout, sys.stderr = oldout, olderr
            out[0] = out[0].getvalue()
            out[1] = out[1].getvalue()


def test_assignment(subclass, good_names, stud_name,
                     module_name, mod_path, grade_path):
    global student_name
    student_name = stud_name
    
    try:
        subclass.good_func_names(good_names)
        subclass.get_names(student_name, module_name, mod_path)
        
        with open(grade_path, "w") as f:
            f.write(student_name)
            f.write("\n")
            suite = unittest.TestLoader().loadTestsFromTestCase(subclass)
            unittest.TextTestRunner(f, verbosity=2).run(suite)
            f.write("\n")

    except Exception as e:
        print "Test of student {}'s homework failed".format(student_name)
        print e


if __name__ == "__main__":
    pass

