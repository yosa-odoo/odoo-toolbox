#!/bin/bash

function show_help {
  echo "Usage: b [OPTIONS] NAME"
  echo ""
  echo "Based on NAME, the script sets up the Odoo environment. It sets:"
  echo "- The OC/OE branch"
  echo "- The PY environment"
  echo "- The DB name"
  echo ""
  echo "Options:"
  echo "  -h, --help              Show help"
  echo "  -o, --odoo VERSION      Set Odoo version"
  echo "  -d, --database DB       Set database name"
  echo "  -f, --fetch             If NAME is considered as a branch and if that branch"
  echo "                          is not found locally, try to find it on remote"
  echo "                          repositories"
  echo "  -r, --reset             If the script finds a branch NAME, reset it with the"
  echo "                          remote one"
  echo "  -n, --no-init           Avoid DB initialization"
  echo ""
  echo "If NAME starts with '<version>-', the script will consider NAME as a potential"
  echo "branch name. It will therefore check in the local repositories to find and use"
  echo "it. Options -f and -r are only relevant in such situation."
  echo ""
  echo "If -d is not defined, the script will define the DB name itself:"
  echo "- If NAME is a branch and contains an OPW number, the DB name will be:"
  echo "  <opw number>-<version>[-fw]"
  echo "  (The part '-fw' is defined when the branch's author is fw-bot)"
  echo "- Else, NAME will be used as DB name"
  echo ""
  echo "If -o is not specified, the script will try to extract the odoo version from"
  echo "NAME. Without any identified version, the execution is interrupted."
  echo ""
  echo "Notes: "
  echo "  - If Odoo version is master, the DB initialization is automatically skipped."
}



odoo=""
database=""
name=""
fetch=false
reset=false
init=true



while [[ "$#" -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      exit 0
      ;;
    -o|--odoo)
      odoo="$2"
      shift
      ;;
    -d|--database)
      database="$2"
      shift
      ;;
    -f|--fetch)
      fetch=true
      ;;
    -r|--reset)
      reset=true
      ;;
    -n|--no-init)
      init=false
      ;;
    *)
      if [ -z "$name" ]
      then
        name="$1"
      else
        >&2 echo "Incorrect options/arguments"
        >&2 echo ""
        >&2 show_help
        exit 1
      fi
      ;;
  esac
  shift
done



if [[ -z "$name" ]]; then
  >&2 echo "Missing argument."
  exit 1
fi



odoo=${odoo:-$name}
odoo=$(echo "$odoo" | grep -oE 'master|(saas-)?[0-9]{2}\.[0-9]' | head -1)

if [ -z "$odoo" ]
then
  >&2 echo "Missing version (or incorrect version format)."
  exit 1
fi



switch_branch() {
  repo="$1"
  branch_name="$2"
  fetch="$3"
  must_reset="$4"
  cd "$HOME"/src/all/"$repo" || (>&2 echo "Repo $repo not found"; exit 1)

  branch=$(git branch | grep -E "$branch_name\$" >/dev/null && echo "$branch_name")
  if [ "$fetch" = true ] && [ -z "$branch" ]
  then
    echo "[$repo side] Nothing found. Looking on remote repo..."
    branch=$(git ls-remote --exit-code --heads "$repo"-dev "$branch_name" >/dev/null 2>&1 && git fetch "$repo"-dev "$branch_name" && echo "$branch_name")
  fi

  if [ "$branch" ]
  then
    git checkout -q "$branch"
    if [ "$must_reset" = true ]
    then
      echo "[$repo side] Resetting branch..."
      git reset --hard "$repo"-dev/"$branch_name" >/dev/null 2>&1 || echo "[$repo side] Reset failed."
    fi
    return 0
  fi
  return 1
}



ostate "Previous configuration"


echo
echo "Switching Odoo version..."
cv "$odoo" > /dev/null

if echo "$name" | grep -oEq 'master|(saas-)?[0-9]{2}\.[0-9]-'
then
  echo
  echo "Looking for specific branch..."
  switch_branch odoo "$name" "$fetch" "$reset" &
  oc_process=$!
  switch_branch enterprise "$name" "$fetch" "$reset" &
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
if [ -z "$database" ]
then
  opw=$(echo "$name" | grep -oE '([0-9]{7})' | head -1)
  if [ "$is_branch" = true ] && [ "$opw" ]
  then
    fw=$(echo "$name" | grep -Eo '\-fw$' || echo "")
    database=$opw-$odoo$fw
  else
    database=$name
  fi
fi
setdb "$database"

if [ "$odoo" != "master" ] && [ "$init" = true ] && ! ldb | grep -Eq "^$database$"
then
  template="${odoo}__init"
  if ldb -a | grep -Eq "^$template$"
  then
    echo
    echo "Initializing DB & Filestore..."
    createdb -T "$template" "$database"
    mkdir -p ~/.local/share/Odoo/filestore/"$database"
    cp -rf ~/.local/share/Odoo/filestore/"$odoo"/* ~/.local/share/Odoo/filestore/"$database"/
    savedb init
  fi
fi



echo
ostate "New configuration"
