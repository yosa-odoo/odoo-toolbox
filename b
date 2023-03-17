#!/bin/bash

if [ $# -ne 1 ]; then
    >&2 echo "Needs 1 parameter (branch/db name)"
    exit 1
fi

opw=$(echo "$1" | grep -oE '([0-9]{7})' | head -1)
version=$(echo "$1" | grep -oE '(master|(saas-)?[0-9]{2}\.[0-9])' | head -1)
fw=$(echo "$1" | grep -o '\-fw' || echo "")
is_branch=false

if [ -z "$version" ]
then
  >&2 echo "No version identified"
  exit 1
fi

switch_branch() {
  repo="$1"
  name="$2"
  cd "$HOME"/src/all/"$repo" || (>&2 echo "Repo $repo not found"; exit 1)

  branch=$(git branch | grep -E "$name\$" >/dev/null && echo "$name")
  if [ -z "$branch" ]
  then
    branch=$(git ls-remote --exit-code --heads "$repo"-dev "$name" >/dev/null 2>&1 && git fetch "$repo"-dev "$name" && echo $name)
  fi

  if [ "$branch" ]
  then
    git checkout -q "$branch" && return 0
  fi
  return 1
}



ostate "Previous configuration"



echo
echo "Switching version..."
cv "$version" > /dev/null


if echo $1 | grep -Eqo "^$version.{1,}"
then
  echo
  echo "Looking for specific branch..."
  switch_branch odoo "$1" &
  oc_process=$!
  switch_branch enterprise "$1" &
  oe_process=$!

  wait $oc_process
  is_oc_branch=$?
  wait $oe_process
  is_oe_branch=$?

  if [ $is_oc_branch = 0 ] || [ $is_oe_branch = 0 ]
  then
    is_branch=true
  fi
fi



echo
echo "Specifying DB..."
if [ $is_branch = true ] && [ "$opw" ]
then
  db=$opw-$version$fw
else
  db=$1
fi

setdb "$db"




if ! $( ldb | grep -Eq "^$db$" ); then
  template="${version}__init"
  if $( ldb -a | grep -Eq "^$template$" ); then
    echo
    echo "Initialising DB & Filestore..."
    createdb -T $template $db
    mkdir -p ~/.local/share/Odoo/filestore/$db
    cp -rf ~/.local/share/Odoo/filestore/$version/* ~/.local/share/Odoo/filestore/$db/
    savedb init
  fi
fi



echo
ostate "New Configuration"

