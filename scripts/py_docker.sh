#!/bin/bash
#Инициализация проекта, запуск команд системы
comm=$1
#echo "Command: $comm"
shift
case "$comm" in
	serve) # Serve catalog webserver
		echo "Serve catalog webserver"
		cd /usr/projects/danc
		python3 serve.py
	;;
	pip) # Run PIP command
		echo "Run PIP command" 
		pip "$@"
	;;
	svg) # Generate svg for diagram
		echo "Generate svg for diagram"
		#cd "$PROJECTNAME"
		cd /usr/projects/danc
		python3 view_file.py "$@"
	;;
	url) # Generate URL for diagram
		echo "Generate URL for diagram"
		#cd "$PROJECTNAME"
		cd /usr/projects/danc
		python3 view_file.py -u "$@"
	;;
	git) 
		echo "Execute git command in project folder"
		cd /usr/projects/danc
		git $*
	;;
	sh) 
		echo "Execute any shell (sh) command"
		/bin/sh -c "$*"
	;;
	*) echo "No command specified" 
		echo "Use: serve | url | svg | pip | git | sh" 
	;;
esac
