# hello-heroku
trying out heroku

Add codecov and build stickers here.

## Projects / Microservices / Components
### [Vault](docs/vault.md)
Data Collection :bank:
### [Garden](docs/garden.md)
Infrastructure :deciduous_tree:
### [Gothic](docs/gothic.md)
Synchronization :european_castle:
###### [Fabric](fabfile/README.md)
Our build, provision, and shell tool :construction:

## Bootstrap Development Environment
###### [techstack](docs/tech_stack.md):
Our local development environments assume the following
* This repository (olympus)
* Python 2.7
* pip 9.0
* tox 2.9.1
* Postgres
* RabbitMQ

### 1. Python
```
which python
python --version
```

### 2. Pip
```
$ wget https://bootstrap.pypa.io/get-pip.py
```
OR
```
$ curl -O https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py
```

### 3. tox
Install tox
```
$ sudo pip install tox
```

### 4. RabbitMQ
```
brew install rabbitmq
brew services start rabbitmq
```

### 5. Postgres
##### Homebrew:
```
# Install postgres db
$ brew install postgres
-
# Starts postgres db
$ brew services start postgres
-
# Postgres requires a default db with user's name
$ createdb
```
##### Alternatively using Postgres.app:

1. Follow instructions 1 and 2 [here](https://postgresapp.com/).
2. Add the following to ~/.bashrc or equivalent: \
 `export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"`

### 6. gcloud
##### gcloud cli
TODO add install notes

###### gcloud environments
You will need to set up three different environments, *production*, *sandbox*, and *greenhouse* (but you may end up only using one or two)

For help on the general gcloud commands use:
```gcloud config configurations --help```


You will need to create a new configuration on your machine to point to each of our projects
```gcloud config configurations create {env}```

Once it is created you can switch between them with ```gcloud config configurations activate {env}```


To populate the configuration with
```
gcloud init

Re-initialize this configuration [env] with new settings

Choose the account you would like to use to perform operations for
this configuration:
 [1] *.*@staydomio.com


 Pick cloud project to use:
 [1] domio-greenhouse
 [2] domio-prod
 [3] domio-sandbox

To setup
 [1] us-east1-b
```


You can then use the following to switch between environments (and fabric uses the following internally to switch)

I have two aliases set to help me on the command line

``` alias gcl-activate='gcloud config configurations activate' ```

``` alias gcl-ssh='gcloud compute ssh ' ```

#### SSH agent
gcloud should manage our SSH keys for us, and fabric should handle forwarding
those keys downstream, but just in case you may need to explicitly tell your
local ssh agent what to forward


```
Host *
 AddKeysToAgent yes
 UseKeychain yes
 IdentityFile ~/.ssh/id_rsa
 ForwardAgent yes

Host github.com
 AddKeysToAgent yes
 UseKeychain yes
 IdentityFile ~/.ssh/id_rsa
 ForwardAgent yes
 Hostname github.com
 User git
```

You will need to log in to one of the boxes on the new environment to propogate your SSH key  onto the project  ```gcloud compute ssh {VM}```

### Using the local development environment
Run tox in the olympus root.
```
tox
```
tox will now install all listed dependencies, run all unit tests and lint all app code.  Since you have downloaded a clean repo, all tests should pass.  If any fail it could indicate a problem with your local environment.  You can now activate the virtualenvironment created by tox
```
$ source env/bin/activate
```

##### Bootsrapping with Fabric
Next bootstrap the development database for use.
```
$ fab bootstrap
$ fab bootstrap.database
$ fab bootstrap.database:fixtures=true
```

From here please run ``` fab ``` to get a list of available commands


##### Alternatively using Conda:
```
# Install Conda if not installed system wide.
-
# create olympus environment from a environment file
$ conda env create -f config/conda_env.yml

$ source activate olympus
$ source deactivate
-
# To export current environment to a environment file
$ conda env export | grep -v "^prefix: \|^  - olympus" > config/conda_env.yml
-
# Alternatively, create a fresh conda env with python 2.7
$ conda create --name olympus python=2.7
# Then, we need to install fabric and fab boostrap
```


## Running locally
Run a local server
```
$ fab serve
```
There is now an HTTP serving traffic on localhost:5000

```
fab celery_beat
fab celery_worker
```

To run a specific type of celery worker, do
```
fab celery_worker:name
```
Where name is one of the queue names in olympus.constants.celery_queues

To add a new queue, specify it in constants.celery_queues and celery_tasks.tasks_routes_config.
To add tasks to existing queues, add the tasks to the right file under celery_tasks folder.

## Fabric and CLI
Fab commands use the following syntax:
```
fab environment:location verb
```
e.g. ```fab stage:remote=True deploy```

Fab commands are of the form
```
fab [environment:remote?] command:args
```
Environment can be test, dev, stage, or prod. The default is dev.

Note that ```fab test``` is an exception which does not follow the above format.

Check out the fabfile.py for all runnable commands.
We also use manage.py as a hook for heroku commands, especially migrations.

### NOTE:
To use the 'production' environment, you will need a local file at /var/log/olympus.log with permissions for your user.

```
sudo mkdir -p /var/log
sudo touch /var/log/olympus.log
sudo chown $(whoami):$(groups | cut -d ' ' -f 1) /var/log/olympus.log
```

## Celery Worker Deployment:
`$ fab production:true deploy:true`

Other deployment guides found in confluence -> Runbooks

## Migrations
```
# Auto generate alembic migration scripts
$ alembic revision --autogen -m 'describe this change'
```
[Caveat](http://alembic.zzzcomputing.com/en/latest/autogenerate.html).
Always proof read the auto-generated migration script. \
Autogenerate can not handle correctly: changes of table name, changes of column name, etc.
```
# Migrate to head:
$ fab bootstrap.migrate:'upgrade head'
# Upgrade +X revisions.
$ fab bootstrap.migrate:'upgrade +1'
# Downgrade -X revisions.
$ fab bootstrap.migrate:'downgrade -1'
```

Backrefs cheat sheet:
```
other_table_name = db.relationship(
    OtherTableClass, backref='this_table_name', lazy='dynamic'
)
```


# Style Guide

http://i0.kym-cdn.com/photos/images/original/000/797/853/72e.jpg

### If your line is > 100 characters:

Break at parens `()`\
ensure that sibling parens are on the same indentation level

In cases where parens are not currently present on this line: DON'T use backslashes. Instead ADD parens to this line so you can break on them

### Dictionaries:

Always leave a comma at the end!

right:

`{'thing1': 'hat', 'thing2': 'cat', 'thing3': 5,}`

wrong:

`{'thing1': 'hat', 'thing2': 'cat', 'thing3': 5}`


# Common Problems:

## My test_patch is broken after adding a new foreignkey field to my model!

- This means you probably added a subfactory to the model whose test broke.
- You need to take this field from the record and pass it into the expected so that they match.

e.g.

```
record = self.model_factory()
expected = self.model_factory.build(new_field=record.new_field)
```

## My new db relationship is broken!

There are two options:
### backref
```
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child = relationship("Child", backref="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
```


## wkhtmltopdf

https://wkhtmltopdf.org/downloads.html
Requires > 0.12.4 (previous versions need xvfb)

Installation: Unzip, move wkhtmltopdf binary to /usr/bin

#### NOTE: This is needed on both worker boxes (when apply\_async'd) and on api boxes (when GET /invoice\_pdfs/generate)

# Tableau - Python Integration
```
# Make sure that tabpy-server is in virtual environment
$ pip install tabpy-server
# Navigate to venv/lib/python2.7/site-packages/tabpy_server.
$ sh startup.sh 9004

# In tableau, go to Help -> Settings and Performance -> Manage External Service Connection.  Fill in Server: localhost; Port:9004.  Click OK.
```
