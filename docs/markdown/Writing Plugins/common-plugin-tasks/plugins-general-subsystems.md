---
title: "Common subsystem tasks"
slug: "plugins-common-subsystem"
excerpt: "Common tasks for Subsystems"
hidden: false
createdAt: "2023-11-22T17:00:00.000Z"
---
Skipping individual targets
---------------------------

Many subsystems allow skipping specific targets. For example, you might have Python files that you want to not typecheck with mypy. In Pants, this is achieved with a `skip_*` field on the target. This is simple to implement.

1. Create a field for skipping your tool

```python
from pants.engine.target import BoolField

class SkipFortranLintField(BoolField):
	alias = "skip_fortran_lint"
	default = False
	help = "If true, don't run fortran-lint on this target's code."
```

2. Register this field on the appropriate targets.

```python
def rules():
	return [
		FortranSourceTarget.register_plugin_field(SkipFortranLintField),
	]
```

3. Add this field as part of your subsystems `opt_out` method:

```python
from dataclasses import dataclass

from pants.engine.target import FieldSet, Target


@dataclass
class FortranLintFieldSet(FieldSet):
    required_fields = (FortranSourceField,)

    source: FortranSourceField
    
    @classmethod
    def opt_out(cls, tgt: Target) -> bool:
        return tgt.get(SkipFortranLintField).value
```