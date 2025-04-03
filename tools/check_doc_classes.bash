#!/usr/bin/env bash

# Save GameClasses.odg as a flat file (GameClasses.fodg)
# this file will the contain plain text class names
#
# The following script identifies which classes are not documented
# Enums are filtered. the generated help file param_types.html covers them.

# does not exclude enum classes
#classes=`grep -Eho "^class [A-Za-z0-9_]+" src/*py src/*pyw | sed s/class//`

classes=`grep -Eh "^class" src/*py src/*pyw | sed /Enum/d | sed -Ee "s/^class ([A-Za-z0-9]+).*$/\1/"`

for c in $classes; do
	if [[ -z `grep $c docs/GameClasses.fodg` ]]; then
		echo "$c   missing"
	fi
done

