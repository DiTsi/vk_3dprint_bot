#!/bin/bash

export_file=./requirements.txt

pip freeze > $export_file

exit 0
