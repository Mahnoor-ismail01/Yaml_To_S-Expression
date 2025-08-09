import unittest
from IR import to_ir, to_sexpr, convert_to_sexpr, IRScalar, IRMapping, IRSequence
from datetime import date
import yaml
import tempfile
import os

class TestIRToSexpr(unittest.TestCase):
    def test_scalar(self):
        ir = IRScalar("value")
        self.assertEqual(to_sexpr(ir), '"value"')
    
    def test_date_string(self):
        ir = IRScalar("2012-09-06", is_date=True)
        self.assertEqual(to_sexpr(ir), "(make-date 2012 09 06)")
    
    def test_date_object(self):
        ir = to_ir(date(2012, 9, 6))
        self.assertEqual(to_sexpr(ir), "(make-date 2012 09 06)")
    
    def test_mapping(self):
        ir = IRMapping({"key": IRScalar("value")})
        self.assertEqual(to_sexpr(ir), '(yaml:key "value")')
    
    def test_boolean(self):
        ir = IRScalar(True)
        self.assertEqual(to_sexpr(ir), "true")
    
    def test_yaml_to_ir(self):
        yaml_str = "key: value"
        ir = to_ir(yaml.safe_load(yaml_str))
        self.assertIsInstance(ir, IRMapping)
        self.assertEqual(to_sexpr(ir), '(yaml:key "value")')
    
    def test_empty_yaml_file(self):
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")  
            temp_file = f.name
        try:
            result = convert_to_sexpr(temp_file)
            self.assertEqual(result, "null")
        finally:
            os.unlink(temp_file)  # Clean up

if __name__ == '__main__':
    unittest.main()