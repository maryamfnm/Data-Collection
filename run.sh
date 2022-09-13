cmd="python data_collection.py --start_id $1 --end_id $2"
#!/bin/bash
$cmd
while [ $? -ne 0 ]; do
    $cmd
done
