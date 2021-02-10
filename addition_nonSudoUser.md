# Modifying jupyterhub configuration to include central pyiron repositories with a non-sudo user adminstrator [without any ssh access to the terminal]
In this document, `nonSudoUser` is used as the username for the non-sudo manager of the students' central repositories. The idea is that the `nonSudoUser` has no access via terminal to the server and he/she can only access the server via jupyterhub web interface.  
Here, I have assumed that an account for `nonSudoUser` is created and `pyiron_docker_workspace` is added to his/her home directory.  
## Creating a central pyiron repository   
1) Create the central repositories via the following commands inside the home directory of `nonSudoUser`:

```
sudo mkdir /home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/
sudo mkdir /home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/pyiron/
sudo mkdir /home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/pyiron_contrib/
sudo mkdir /home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/custom_code/
sudo chown -R nonSudoUser:users /home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/
sudo chmod -R 775 /home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/
```

## Modifying the jupyterhub configurations  

2) Stop the running containers.
```
sudo docker stop $(sudo docker ps -q)
```  
3) `jupyterhub_config.py` file needs to be modified to mount correctly the created directories above to the users' docker containers.  

In the `jupyterhub_config.py`, the lines: 
```
c.DockerSpawner.volumes = {
                       '/home/{username}/pyiron_docker_workspace/': { 'bind': notebook_dir , 'mode': 'rw'},
                       '/opt/studentRepo/pyiron/': { 'bind': '/home/pyiron/studentRepo/pyiron/', 'mode': 'ro'},
                       '/opt/studentRepo/pyiron_contrib/': { 'bind': '/home/pyiron/studentRepo/pyiron_contrib/', 'mode': 'ro'},
                       '/opt/studentRepo/custom_code/': { 'bind': '/home/pyiron/studentRepo/custom_code/', 'mode': 'ro'},
}
```
should be changed to:
```
c.DockerSpawner.volumes = {
                       '/home/{username}/pyiron_docker_workspace/': { 'bind': notebook_dir , 'mode': 'rw'},
                       '/home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/pyiron/': { 'bind': '/home/pyiron/studentRepo/pyiron/', 'mode': 'ro'},
                       '/home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/pyiron_contrib/': { 'bind': '/home/pyiron/studentRepo/pyiron_contrib/', 'mode': 'ro'},
                       '/home/nonSudoUser/pyiron_docker_workspace/studentRepo_replica/custom_code/': { 'bind': '/home/pyiron/studentRepo/custom_code/', 'mode': 'ro'},
}
```
4) Now you can restart the jupyterhub server. Please keep in mind that the following command should be executed in the directory where `docker-compose.yml` file resides.  
```
sudo docker-compose up --build -d
```
