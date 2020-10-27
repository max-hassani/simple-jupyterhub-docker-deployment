# Modifying jupyterhub configuration to include central pyiron repositories

## Creating a central pyiron repository
1) Before creating a central repository, we should first create a group including repository owner (here I call the user: repoadmin) and root:
```
sudo groupadd repomanagers 
```
Then add the repoadmin and root to the group:
```
sudo chmod -a -G repomanagers repoadmin
sudo chmod -a -G repomanagers root
```  

2) Now create the central repositories via the following commands:

```
sudo mkdir /opt/studentRepo/
sudo mkdir /opt/studentRepo/pyiron/
sudo mkdir /opt/studentRepo/pyiron_contrib/
sudo mkdir /opt/studentRepo/custom_code/
sudo chown -R repoadmin:repomanagers /opt/studentRepo/
sudo chmod -R 775 /opt/studentRepo/
```

## Modifying the jupyterhub configurations  

1) Before applying any changes to your current setup, please back up the current working version.  
2) Clone the repository in a new folder, via
```
git clone https://github.com/muh-hassani/simple-jupyterhub-docker-deployment modified-server-setup/
```  
Then checkout to the `withCentralRepo` branch via,  
```
cd modified-server-setup/
git checkout withCentralRepo
```  
3) Now we need to build some new docker images:  
```
sudo make notebook_image1
sudo make notebook_image2
```
These two commands create two new docker images: pyiron-base:latest and pyiron-md:latest.  

4) Stop the running containers:
```
sudo docker kill jupyterhub
sudo docker kill jupyterhub-db
```  

5) We need to edit the old jupyterhub_config.py. You can copy the new lines from the newly cloned repository (modified-server-setup/jupyterhub_config.py)

in the old jupyterhub_config.py, the line: 
```
c.DockerSpawner.image_whitelist = {'pyiron-base':'muhhassani/pyiron-base-image','pyiron-md':'muhhassani/pyiron-lammps-image'}
```
should be changed to:
```
c.DockerSpawner.image_whitelist = {'pyiron-base':'pyiron-base:latest','pyiron-md':'pyiron-md:latest'}
```
Additionally, the line:
```
c.DockerSpawner.volumes = { '/home/{username}/pyiron_docker_workspace/': notebook_dir }
```  
should be changed to:
```
c.DockerSpawner.volumes = {
                       '/home/{username}/pyiron_docker_workspace/': { 'bind': notebook_dir , 'mode': 'rw'},
                       '/opt/studentRepo/pyiron/': { 'bind': '/home/pyiron/studentRepo/pyiron/', 'mode': 'ro'},
                       '/opt/studentRepo/pyiron_contrib/': { 'bind': '/home/pyiron/studentRepo/pyiron_contrib/', 'mode': 'ro'},
                       '/opt/studentRepo/custom_code/': { 'bind': '/home/pyiron/studentRepo/custom_code/', 'mode': 'ro'},
}
```
6) Now you can restart the jupyterhub server. First go to the old working repository and then run:

```
sudo docker-compose up --build -d
```