#!/bin/sh

web_dir=$(cd `dirname $0` && cd .. && pwd )
export PYTHONPATH=$web_dir
pytest $web_dir/pgadmin --json=test_result.json --resultlog=regression.log
