# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os
import docker

c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
#c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
#c.DockerSpawner.image_whitelist = {'pyiron-base':'muhhassani/pyiron-base-image','pyiron-atomistic':'muhhassani/pyiron-image'}
c.DockerSpawner.image_whitelist = {'tensorflow':'muhhassani/nonroot_tensorflow:2021-11-09', 
			           'temp1':'muhhassani/nonroot_tensorflow:2021-10-18'}
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
#spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
#c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
spawn_cmd = "start-singleuser.sh --SingleUserNotebookApp.default_url=/lab"
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/docker_user/'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { '/home/{username}/docker_workspace/': notebook_dir }
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            count=-1,
            capabilities=[["gpu"]],
        ),
    ],
}

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Authenticate users with GitHub OAuth
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
#c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

#c.DockerSpawner.mem_limit='10G'
#c.DockerSpawner.cpu_limit=2
#c.Spawner.mem_limit = '10G'
#c.Spawner.cpu_limit = 2
# Other stuff
#c.Spawner.cpu_limit = 2
#c.Spawner.mem_limit = '10G'

# Whitlelist users and admins
c.Authenticator.whitelist = whitelist = set()
#c.Authenticator.admin_users = admin = set()
c.Authenticator.admin_users = {'localadmin'}
c.JupyterHub.admin_access = True
