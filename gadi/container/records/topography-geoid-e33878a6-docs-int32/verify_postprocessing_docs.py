import ast, inspect, json, sys
from pathlib import Path
from dataclasses import fields, is_dataclass
from petsc4py import PETSc
import numpy as np
import underworld3 as uw
installed=Path(sys.argv[1]).resolve()
source=Path(sys.argv[2]).resolve()
assert Path(uw.__file__).is_relative_to(installed)
assert np.dtype(PETSc.IntType).itemsize*8==32
functions=[]; classes=[]
for module in (uw.postprocessing.geoid,uw.postprocessing.cylindrical_potential,uw.postprocessing.spherical_interface_load,uw.postprocessing.spherical_potential):
 for name in module.__all__:
  obj=getattr(module,name);d=inspect.getdoc(obj) or ''
  if inspect.isfunction(obj):
   assert all(section in d for section in ['Parameters\n----------','Returns\n-------','Raises\n------']),name
   section=d.split('Parameters\n----------',1)[1].split('\nReturns\n',1)[0];documented=set()
   for line in section.splitlines():
    if line and not line.startswith(' ') and ' : ' in line:documented.update(s.strip().lstrip('*') for s in line.split(' : ',1)[0].split(','))
   arguments=list(inspect.signature(obj).parameters)
   assert set(arguments)<=documented,name
   functions.append(dict(module=module.__name__,name=name,arguments=arguments))
  elif inspect.isclass(obj) and is_dataclass(obj):
   assert 'Attributes\n----------' in d,name
   section=d.split('Attributes\n----------',1)[1].split('\nNotes\n',1)[0];documented=set()
   for line in section.splitlines():
    if line and not line.startswith(' ') and ' : ' in line:documented.update(s.strip() for s in line.split(' : ',1)[0].split(','))
   assert {f.name for f in fields(obj)}<=documented,name
   classes.append(name)
assert len(functions)==20 and len(classes)==8
for name in ('postprocessing/geoid.py','postprocessing/cylindrical_potential.py','postprocessing/spherical_interface_load.py','postprocessing/spherical_potential.py','postprocessing/_spherical_solver_contract.py','analytic/spherical/gravity.py','analytic/cylindrical/gravity.py'):
 assert (installed/'underworld3'/name).read_bytes()==(source/'src/underworld3'/name).read_bytes(),name
record=dict(passed=True,petsc_integer_bits=32,package_origin=uw.__file__,function_count=len(functions),argument_count=sum(len(f['arguments']) for f in functions),response_classes=classes,source_package_match=True,functions=functions)
Path(sys.argv[3]).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='functions'},indent=2))
