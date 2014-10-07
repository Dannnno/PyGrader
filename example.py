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

import auto_grader
import glob
import os
import sys


saved = sys.stdout


class example_test_class(auto_grader.auto_grader): 
    """An example grader for a certain homework"""
    
    def setUp(self): 
        """Not implemented - Sets up the program"""
        self.test_out = auto_grader.test_std_out()
        sys.stdout = self.test_out
        #pass
    
    def tearDown(self): 
        """Not implemented - 'tears down' the program"""
        sys.stdout = saved
        #pass
    
    def test_func1(self):
        """Tests func1"""
        func1 = example_test_class.black_magic("func1")
        map(self.assertEqual,
            map(func1,
                [0, 1, 2, 3, 4]),
            [1, 2, 3, 4, 5])
            
    def test_func2(self):
        """Tests func2"""
        func2 = example_test_class.black_magic("func2")
        map(self.assertEqual,
            map(func2,
                ["Hi", "My", "Name", "Is"]),
            ["iH", "yM", "emaN", "sI"])
            
    def test_printing(self):
        """Tests func3"""
        printing_function = example_test_class.black_magic("printer")
        
        #self.test_out.write(self.test_out.written)
        #self.test_out.write(self.test_out.written[-1:-4])
        sys.stdout = saved
        print self.test_out
        print self.test_out.written
        print self.test_out.written[len(self.test_out.written)-4:]    
        sys.stdout = self.test_out
        map(self.assertEqual,
            map(printing_function,
                ["Hi", "My", "Name", "Is"]),
            #self.test_out.written[len(self.test_out.written)-4:])
            ["Hi", "My", "Name", "Is"])
        sys.stdout = saved
        print self.test_out
        print self.test_out.written
        print self.test_out.written[len(self.test_out.written)-4:]    
        sys.stdout = self.test_out
    
                   
if __name__ == "__main__":
    os.chdir(os.getcwd() + "\\example_assignments" )
    student_names = ["Alice", "Bob", "Dan"]
    module_names = ["ps3alice","ps3bob", "ps3dan"]
    writepaths = [name[:-2]+"txt" 
                  for name in [filename for filename in glob.glob("*.py")]]
    
    submissions = zip(student_names, module_names, [os.getcwd()]*3, writepaths)
    
    for submission in submissions:
        auto_grader.test_assignment(example_test_class, 
                                    ["func1", "func2", "printer"], 
                                    submission[0],
                                    submission[1], 
                                    submission[2], 
                                    submission[3])
                                    