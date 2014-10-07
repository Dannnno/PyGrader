PyGrader
========

Repository demonstrating how python can be used to auto-grade homework assignments.  Does not contain any specific assignments or their tests, but does contain the basic building blocks used. Basic functionality is complete, advanced funcitonality is planned

## Planned functionality:
Will implement a sandbox  
Will implement a parser to fix submissions that don't use `if __name__ == "__main__":`

===

## How to use:

auto_grader.auto_grader  is the base auto_grader class.  It has all of the built in functionality to run the majority of desired tests.  It is a subclass of `unittest.TestCase` so normal unit testing methods (such as `self.assertEqual()`) will work in this    class.

Grader is asked to subclass this with their own desired functionality.  If    capturing printed statements is desired then just use the context manager    `autograder.capture()` like so
    
        def test_my_func(self):
            my_func = my_subclass.black_magic(func_name)
            
            with self.capture() as (out, err):
                map(self.assertEqual,
                    map(my_func,
                        arglist),
                    out)
                    
If this doesn't do exactly you want then just override capture with the     desired functionality.  When implementing your test functions you can just do

        def test_some_func(self, args):
            some_func = my_subclass.black_magic(func_name)
            map(self.assertEqual,
                map(some_func,
                    arglist),
                expected_value_list)

To actually run your tests just call

        test_assignment(subclass, good_names, student_name,
                        module_name, mod_path, grade_path)

With all of the appropriate arguments.  Loops are ideal.  For example:

        for submission in submissions:
            test_assignment(subclass, my_names, submission[0],
                            submission[1], submission[2], submission[3])

Where submission has all of the data you need and submissions contains every piece of data
