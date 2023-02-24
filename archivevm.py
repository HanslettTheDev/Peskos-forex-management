import os
import xml.etree.ElementTree as etree
from datetime import datetime as dt

is_active = True

while is_active:
    all_current_vm = os.popen('sudo virsh list --all --name').read().strip()
    print("Here is a list of all the VM users available on this system:")
    print(all_current_vm)

    vm_name = input("Please enter a VM name: ")

    for vm in all_current_vm.split("\n"):
        if vm == vm_name:
            # Setup the xml file name and then call the os module to execute the command in the command line and store
            # the xml file in the current working directory

            xml_file_name = vm_name + '.xml'
            xml_cmd_command = 'sudo virsh dumpxml '+ vm_name + ' > ' + xml_file_name
            os.system(xml_file_name)


            # now use the xml module to analyze the xml file and extract the qcow2 image file
            # first we parse the xml file. get the root tree which returns a key, value pair and
            # we can use the find method to access the devices -> disk -> source location
            qcow2_image = etree.parse(xml_file_name).getroot().find('devices').find('disk').find('source').attrib['file']
    
            # add the file name of the archive and the files to be added which is the xml and qcow2_image file
            backup_file_name = vm_name + '-' + dt.today().strftime('%Y%m%d') + '.tar.gz'

            #  create archive command and run
            archiveCommand='tar -zcvf ' + backup_file_name + ' ' + xml_file_name + ' ' + qcow2_image
            print("Backing Up................")
            os.system(archiveCommand)
            print(f'Backup Completed! Check {backup_file_name} in current directory')
            is_active = False
    
    print(f"The VM Computer [{vm_name}] doesn't exist, please enter a valid name:")
