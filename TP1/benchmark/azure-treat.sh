#!/bin/bash

#~ Const declaration



dns_name=""
image_ubuntu="b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-16_04-LTS-amd64-server-20170202-en-us-30GB"
vm_username=""
vm_pass=""
vm_location="\"WEST US 2\""
vm_size=""
vm_name=""

#~ remarque
#~ ajouter deux fonction start and term

function AZ_Install_library() {

	sudo apt-get update
	sudo apt-get install nodejs-legacy
	Y
	sudo apt-get install npm

}

function AZ_init() {

	azure login

}
function AZ_term() {

	azure logout $1

}
function AZ_create_VM() {
	

	azure vm create $1 $2 -g $3 -p "P@ssw0rd!" -l "WEST US 2" -z $4 -n $5 -e 22
	
	
	
}
function AZ_Get_info_VM() {
	azure vm show amine-pc | grep "$dns_name"
}

function AZ_Get_Status_VM() {
	if azure vm list | grep "$1" | grep "ReadyRole"; then
		echo work
	else
		echo notwork
	fi
	
}

function AZ_Connect_VM() {
	echo "ssh $1@$2.cloudapp.net"
	sudo ssh $1@$2.cloudapp.net
}



function AZ_Shutdown_VM() {
	
	azure vm shutdown $1 -d $2
}

function AZ_Start_VM() {
	azure vm start $1 -d $2
}

function AZ_Delete_VM() {
	azure vm delete $1 -q -b -d $2
}
function AZ_Run-Bensh() {
	echo run
}

function main() {
dns_name="tyihhjest"
vm_username="amrvme"
#~ vm_pass="\"P@ssw0rd!\""

vm_size_A1="Basic_A1"
vm_size_A8="Standard_A8_v2"
vm_size_D5="Standard_D5_v2"
vm_name="amine-pc"
mail="aminebarrak@live.com"

#~ pour installer les library necessaire 
#~ AZ_Install_library

#~ pour faire login sur ton compte azure: suivez direction sur terminal
#~ AZ_init

if AZ_create_VM $dns_name $image_ubuntu $vm_username $vm_size_A1 $vm_name | grep "OK"; then
	echo "votre machine virtuelle a ete cree avec succes"
	stat=0
	cmp=0
	while [ "$stat" -eq 0 ] || [ "$cmp" -eq 10 ]; do
		AZ_Get_Status_VM $dns_name
		status=$(AZ_Get_Status_VM $dns_name | grep "work")
		echo "in while"
		echo "status est :$status"
		if [ "$status" = "work" ]; then
			echo "in if"
			stat=1
		fi
		sleep 5s
		cmp=$((cmp+1))
	done


	echo "it works ?!"
	AZ_Connect_VM $vm_username $dns_name
	sleep 1s
else
	echo "refaire votre machine et verifier probleme dans terminal"
fi

#~ pour se connecter a une machine existante
#~ AZ_Start_VM $vm_name $dns_name

#~ Pour supprimer la machine virtuelle cree
#~ AZ_Delete_VM $vm_name $dns_name

#~ se deconnecter de la copte azure
#~ AZ_term $mail



}



	main
