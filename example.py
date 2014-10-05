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
import os

class example_test_class(auto_grader.auto_grader): 
    
    def setUp(self): 
        self.written = []
    
    def tearDown(self): pass
    
    def write(self, string): 
        string = string.replace(' ', '')
        if string: self.written.append(string)
    
    def test_func1(self):
        func1 = example_test_class.black_magic("func1")
        map(self.assertEqual,
            map(func1,
                [0, 1, 2, 3, 4]),
            [1, 2, 3, 4, 5])
            
    def test_func2(self):
        func2 = example_test_class.black_magic("func2")
        map(self.assertEqual,
            map(func2,
                ["Hi", "My", "Name", "Is"]),
            ["iH", "yM", "emaN", "sI"])
            
    def test_printing(self):
        printing_function = example_test_class.black_magic("printer")
        map(self.assertEqual,
            map(printing_function,
                ["Hi", "My", "Name", "Is"]),
            self.written[-1:-4])
     
                   
if __name__ == "__main__":
    os.chdir(os.getcwd() + "\\example_assignments" )
    student_names = ["Alice", "Bob", "Dan"]
    module_names = ["ps3alice","ps3bob", "ps3dan"]
    filepaths = [filename 
                 for filename in os.listdir(os.getcwd())]
    writepaths = [filepath[:-3]+".txt" for filepath in filepaths]
    
    submissions = zip(student_names, module_names, filepaths, writepaths)
    
    for submission in submissions:
        globals()["test"] = __import__("ps3alice")
        auto_grader.test_assignment(example_test_class, 
                                    ["func1", "func2", "printer"], 
                                    submission[0],
                                    submission[1], 
                                    submission[2], 
                                    submission[3])
                                    