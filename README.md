# Deployment of jupyterhub using docker-compose  

## Initial configuration and installations  
In the first step, one need to install docker and docker-compose.  
1) To install docker on a linux machine:  
```
$ sudo apt-get update  
$ sudo apt-get install \  
        apt-transport-https \  
        ca-certificates \  
        curl \  
        gnupg-agent \  
        software-properties-common  
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  
$ sudo add-apt-repository \  
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \  
   $(lsb_release -cs) \  
   stable"  
$ sudo apt-get update    
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```   
2) In the second step, one needs to install docker-compose:  
```
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose    
$ sudo chmod +x /usr/local/bin/docker-compose
```
3) At the third step download this repository.  
```
git clone https://github.com/muh-hassani/simple-jupyterhub-docker-deployment
```  
The repository includes:
```
Dockerfile.jupyterhub  Makefile  README.md  docker-compose.yml  jupyterhub_config.py  secrets  userlist
```

## Preparing the configuration for the deployment  
1) Building the jupyterhub + postgres docker image, plus creating the additional docker volumes.  
To do so, from within the directory of the repository:  
```
sudo make build
```  
2) **Create the user accounts.**  
For creating the user account, I use the following bash script. The first argument passed in is the username.  
```
#!/bin/bash
sudo useradd -m -s /bin/bash "$1"
sudo mkdir /home/"$1"/pyiron_docker_workspace/
sudo chown -R "$1" /home/"$1"/pyiron_docker_workspace/
sudo chown :100 /home/"$1"/pyiron_docker_workspace/
sudo chmod g+rws /home/"$1"/pyiron_docker_workspace/
sudo setfacl -d -m g::rwx /home/"$1"/pyiron_docker_workspace/
sudo passwd "$1"
sudo passwd --expire "$1"
```  
For example `./bash_file hassani`.  
Here, I assume that the admin sets an initial password for the user, which is already expired and the user upon the first ssh, will be required to set up a new password.   

In `/home/<username>/pyiron_docker_workspace` the data from the containers will be saved. The permissions are set in such a way that the docker container, running by the root, can write the data into this directory.

Since this might open some security issues, you can drop the lines for creating the directory and its permissions above, and as an alternative way use docker-volumes. For this purpose in `jupyterhub_config.py`, you can comment this line:    
```
c.DockerSpawner.volumes = { '/home/{username}/pyiron_docker_workspace/': notebook_dir }  
```
and uncomment this line:
```  
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
```  
The downside, here is that the users can not access their data via ssh, since the docker-volumes belong to root, under `/var/lib/docker/volume/`. In this case, the only way to download/upload data is through the jupyter notebooks/lab interface.  
3) **Making a userlist**  
Having all the accounts created, add the names to the file userlist.  
```
usernam1  admin
username2
...
```
If any of the username corresponds to the admin, please specify that in the file like:  
`<username> admin`  

4) **Specifying the path to the ssl certificate and private key**   
In the docker-compose.yml, give the path to the certificate and key:  
```
-<path to the certificate>:/srv/jupyterhub/secrets/jupyterhub.crt  
-<path to the key>:/srv/jupyterhub/secrets/jupyterhub.key
```  
5) Jupyterhub spawns containers for each users based on the specified docker images in the `jupyterhub_config.py`. To pull the necessary images, you can simply use:  
```
sudo make notebook_image
```  
or   
```
sudo docker pull muhhassani/pyiron-base-image
sudo docker pull muhhassani/pyiron-lammps-image 
```
If you want to edit the list of the images available to spawn. In the `jupyterhub_config.py`, edit the line:
```
c.DockerSpawner.image_whitelist = {'pyiron-base':'muhhassani/pyiron-base-image','pyiron-md':'muhhassani/pyiron-lammps-image'}
```   
6) **Setting users' resources**  
In the `jupyterhub_config.py`, one can specify the amount of RAM and cpu to be used for each user. As an example, here we specify 2 cpu and 10GB of RAM for the user.
```
c.Spawner.cpu_limit = 2
c.Spawner.mem_limit = '10G'
```
## Starting the jupyterhub server
To start the server, you need to just insert the following command from the directory where you have `docker-compose.yml` file:
```
sudo docker-compose up --build -d
``` 

