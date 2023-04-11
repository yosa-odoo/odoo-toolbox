#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: script_name <string_to_find> <module:optional> <filetype:optional(default:py)>"
    exit 1
fi

to_find=$1
module=${2:-**}
file_type=${3:-py}

path_number=$(rg --line-number "$to_find" -g "**/${module}/**/*.${file_type}" | fzf -e | cut -d ':' -f 1,2)

path_to_file=$( echo "$path_number" | cut -d ':' -f 1)
line_number=$( echo "$path_number" | cut -d ':' -f 2)

if [ -n "$path_to_file" ]; then
   echo "$path_to_file --line $line_number"
   pycharm --line "$line_number" "$path_to_file"
   exit 0
fi
